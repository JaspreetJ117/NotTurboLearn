import os
import uuid
import torch
import whisper
import requests
import json
import sqlite3
from flask import Flask, render_template, request, jsonify, session

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
DATABASE_FILE = './data/turbonotes.db'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- AI Model Loading ---
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Whisper is using device: {device}")
try:
    whisper_model = whisper.load_model("base", device=device)
    print("Whisper model loaded successfully.")
except Exception as e:
    print(f"Error loading Whisper model: {e}")
    whisper_model = None

# --- Ollama Configuration ---
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
OLLAMA_CONFIG = {
    "model": "gpt-oss:20b",
    "stream": False,
    "options": {"temperature": 0.3, "top_p": 0.9}
}

NOTES_PROMPT_TEMPLATE = """You are an expert note-taker. 
Your task: Turn the following lecture transcript into **clear, exam-ready notes**.

Requirements:
- Format in **Markdown** with headings and bullet points.
- Start with a short **Title** and a **2–3 sentence TL;DR**.
- Include:
  ## Key Concepts
  - Short bullet points for the main ideas.
  
  ## Important Definitions
  - **Term** — short definition
  
  ## Step-by-Step Explanations
  - Break down processes or arguments in order.
  
  ## Equations / Formulas
  - Use LaTeX formatting inside ```math``` blocks if any appear.
  
  ## Code Examples / Snippets
  - Include any code examples mentioned in the lecture.
  - Use proper Markdown code blocks with syntax highlighting if language is specified:
    ```python
    # example
    print("Hello World")
    ```
  
  ## Examples (with timestamps if mentioned)
  
  ## 5 Sample Exam-Style Questions
  - Write questions that test understanding of key points.
  
  ## Action Items / Next Steps
  - Things to review, practice, or think about.

Guidelines:
- Be **concise but complete**.
- Use **bullet points** over long paragraphs.
- **Bold** key terms and ideas.
- Preserve any **code or formulas** exactly as shown in the transcript.
- Do not invent information not present in the transcript.
- Keep the whole output under ~600 words.

Transcript:
{transcript}
"""

CHAT_PROMPT_TEMPLATE = """You are a helpful AI assistant. Answer the user's question based ONLY on the provided lecture notes and conversation history. Your answer must be grounded in the context provided. If the answer is not in the notes, say "I can't answer that based on the provided notes."

--- Notes ---
{notes}

--- Conversation History ---
{history}

--- User's Question ---
{question}
"""

# --- Database Connection ---
def get_db():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# --- Helper Functions ---
def generate_notes_with_ollama(transcript):
    prompt = NOTES_PROMPT_TEMPLATE.format(transcript=transcript)
    try:
        response = requests.post(
            OLLAMA_ENDPOINT,
            data=json.dumps({"prompt": prompt, **OLLAMA_CONFIG}),
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return json.loads(response.text).get('response', "Error: Could not parse response.")
    except Exception as e:
        return f"## Error\nCould not connect to Ollama: {e}"

def get_chat_response(question, notes, history):
    history_str = "\n".join([f"{msg['sender'].title()}: {msg['message']}" for msg in history])
    prompt = CHAT_PROMPT_TEMPLATE.format(question=question, notes=notes, history=history_str)
    try:
        response = requests.post(
            OLLAMA_ENDPOINT,
            data=json.dumps({"prompt": prompt, **OLLAMA_CONFIG}),
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return json.loads(response.text).get('response', "Error: Could not parse chat response.")
    except Exception as e:
        return f"Error connecting to Ollama for chat: {e}"

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def get_history():
    db = get_db()
    items = db.execute("SELECT id, filename, created_at FROM transcripts ORDER BY created_at DESC").fetchall()
    db.close()
    return jsonify([dict(item) for item in items])

@app.route('/session/<int:transcript_id>')
def get_session_data(transcript_id):
    db = get_db()
    notes_row = db.execute("SELECT notes_text FROM notes WHERE transcript_id = ?", (transcript_id,)).fetchone()
    chat_rows = db.execute("SELECT sender, message FROM chat_history WHERE transcript_id = ? ORDER BY created_at ASC", (transcript_id,)).fetchall()
    db.close()

    if not notes_row:
        return jsonify({'error': 'Session data not found'}), 404

    session['current_transcript_id'] = transcript_id
    return jsonify({
        'notes_markdown': notes_row['notes_text'],
        'chat_history': [dict(row) for row in chat_rows]
    })

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file found'}), 400

    audio_file = request.files['audio']
    safe_filename = str(uuid.uuid4())
    audio_path = os.path.join(UPLOAD_FOLDER, f"{safe_filename}.wav")
    audio_file.save(audio_path)

    try:
        print("--- Starting Transcription ---")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = whisper.load_model("small").to(device)
        result = model.transcribe(audio_path, verbose=True)
        transcript_text = result['text']
        print("--- Transcription Finished ---")

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO transcripts (filename, transcript_text) VALUES (?, ?)", (audio_file.filename, transcript_text))
        transcript_id = cursor.lastrowid
        
        print("--- Generating Notes with Ollama ---")
        notes_md = generate_notes_with_ollama(transcript_text)
        print("--- Notes Generation Finished ---")
        
        cursor.execute("INSERT INTO notes (transcript_id, notes_text) VALUES (?, ?)", (transcript_id, notes_md))
        db.commit()
        db.close()
        
        session['current_transcript_id'] = transcript_id
        return jsonify({'notes_markdown': notes_md, 'transcript_id': transcript_id})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    transcript_id = session.get('current_transcript_id')

    if not user_message or not transcript_id:
        return jsonify({'error': 'Missing message or session context'}), 400

    db = get_db()
    notes_row = db.execute("SELECT notes_text FROM notes WHERE transcript_id = ?", (transcript_id,)).fetchone()
    history_rows = db.execute("SELECT sender, message FROM chat_history WHERE transcript_id = ? ORDER BY created_at DESC LIMIT 10", (transcript_id,)).fetchall()
    
    if not notes_row:
        db.close()
        return jsonify({'error': 'Could not retrieve notes for context'}), 404
    
    notes_context = notes_row['notes_text']
    chat_history = [dict(row) for row in reversed(history_rows)]

    ai_response = get_chat_response(user_message, notes_context, chat_history)
    
    cursor = db.cursor()
    cursor.execute("INSERT INTO chat_history (transcript_id, sender, message) VALUES (?, 'user', ?)", (transcript_id, user_message))
    cursor.execute("INSERT INTO chat_history (transcript_id, sender, message) VALUES (?, 'ai', ?)", (transcript_id, ai_response))
    db.commit()
    db.close()

    return jsonify({'response': ai_response})

# --- NEW: Route to edit session name ---
@app.route('/edit/<int:transcript_id>', methods=['POST'])
def edit_session_name(transcript_id):
    new_name = request.json.get('name')
    if not new_name:
        return jsonify({'error': 'New name not provided'}), 400
    
    db = get_db()
    db.execute("UPDATE transcripts SET filename = ? WHERE id = ?", (new_name, transcript_id))
    db.commit()
    db.close()
    return jsonify({'success': True})

# --- NEW: Route to delete a session ---
@app.route('/delete/<int:transcript_id>', methods=['POST'])
def delete_session(transcript_id):
    db = get_db()
    cursor = db.cursor()
    try:
        # Enforce foreign key constraints for this connection
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Delete from child tables first to respect foreign key constraints
        cursor.execute("DELETE FROM chat_history WHERE transcript_id = ?", (transcript_id,))
        cursor.execute("DELETE FROM notes WHERE transcript_id = ?", (transcript_id,))
        cursor.execute("DELETE FROM transcripts WHERE id = ?", (transcript_id,))
        
        db.commit()
        
        # Clear session if the deleted one was active
        if session.get('current_transcript_id') == transcript_id:
            session.pop('current_transcript_id', None)
            
        return jsonify({'success': True})
    except sqlite3.Error as e:
        # If an error occurs, roll back any changes
        db.rollback()
        print(f"Database error during delete: {e}")
        # Return a more specific error message
        return jsonify({'error': f'Database error: {e}'}), 500
    except Exception as e:
        db.rollback()
        print(f"An unexpected error occurred during delete: {e}")
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500
    finally:
        if db:
            db.close()

if __name__ == '__main__':
    from database import init_db
    init_db()
    app.run(host='0.0.0.0', debug=True, port=5000)