"""
app.py

Server entry point for the LectureScribe application.

This module implements the web interface for the LectureScribe note-taking and transcript management system using Flask. It provides:

- Audio transcription using Whisper AI.
- Automated note generation from transcripts using Ollama LLM.
- Session management for multiple transcripts and notes.
- RESTful API endpoints for transcript, note, and chat history management.
- Interactive chat assistant grounded in user notes and transcripts.
- Secure upload and deletion of audio files and session data.
- Integration with database operations in database.py.
- Persistent, database-backed background transcription queue.
- Real-time queue status endpoint.

The architecture separates web presentation, business logic, and data access, supporting extensibility and robust error handling. Security features include session-based access control and file validation. The application is designed for deployment in a secure, internal environment.

Author: Jaspreet Jawanda
Email: jaspreetjawanda@proton.me
Version: 2.0
Status: Production
"""

import os
import uuid
import torch
import whisper
import requests
import json
import sqlite3
from flask import Flask, render_template, request, jsonify, session, send_from_directory
import threading
import time

# --- Configuration ---
UPLOAD_FOLDER = '../uploads'
DATABASE_FILE = '../data/lecturescribe.db'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Global variables for the background queue processor ---
queue_lock = threading.Lock()
new_job_event = threading.Event()

# --- Flask App Initialization ---
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, static_folder=STATIC_FOLDER)
app.secret_key = os.urandom(24)

# --- AI Model Management (Lazy Loading) ---
whisper_model = None
def get_whisper_model():
    """Loads the Whisper model on the first request and caches it globally."""
    global whisper_model
    if whisper_model is None:
        print("Loading Whisper model for the first time...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Whisper is using device: {device}")
        try:
            whisper_model = whisper.load_model("medium", device=device)
            print("Whisper model loaded successfully.")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            whisper_model = None
    return whisper_model

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
- Start with a short **Title** and a **2 to 3 sentence TL;DR**.
- Include:
  ## Key Concepts
  - Short bullet points for the main ideas.
  
  ## Important Definitions
  - **Term** — short definition
  
  ## Step-by-Step Explanations
  - Break down processes or arguments in order.
  
  ## Equations / Formulas (if any)
  - Use LaTeX formatting inside ```math``` blocks if any appear.
  
  ## Code Examples / Snippets (if applicable)
  - Include any code examples mentioned in the lecture.
  - Use proper Markdown code blocks with syntax highlighting if language is specified:
    ```python
    # example
    print("Hello World")
    ```
  ## Examples (with timestamps if mentioned)
    - Include any examples given in the lecture.

  ## Potential Exam Questions 
    - Make a section for potential questions that the professor referred to being on the exam in lecture (if any).

Guidelines:
- Be **concise but complete**.
- Use **bullet points** over long paragraphs.
- **Bold** key terms and ideas.
- Preserve any **code or formulas** exactly as shown in the transcript.
- Do not invent information not present in the transcript.
- Do not skip any sections of the transcript.
- Ensure the notes are **well-organized** and easy to review.
- Use proper Markdown syntax throughout.
- Make detailed notes yet easy to read.
- Create a section for potential questions that the professor referred to being on the exam in lecture (if any).

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

# --- AI Helper Functions ---
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

# --- Background Queue Processor ---
def queue_processor():
    """
    A worker function that runs in a background thread.
    It checks the database for queued transcription jobs and processes them one by one.
    """
    print("Queue processor thread started.")
    while True:
        new_job_event.wait()

        with queue_lock:
            print("Queue processor checking for a new job...")
            db = get_db()
            processing_job = db.execute("SELECT id FROM transcription_queue WHERE status = 'processing'").fetchone()

            if processing_job:
                print(f"Job {processing_job['id']} is already being processed. Worker will wait.")
                db.close()
                new_job_event.clear()
                continue

            job_row = db.execute("SELECT * FROM transcription_queue WHERE status = 'queued' ORDER BY created_at ASC LIMIT 1").fetchone()

            if job_row:
                job_id = job_row['id']
                audio_path = job_row['audio_path']
                original_filename = job_row['original_filename']

                print(f"Processing job {job_id}: {original_filename}")
                db.execute("UPDATE transcription_queue SET status = 'processing' WHERE id = ?", (job_id,))
                db.commit()
                db.close()

                model = get_whisper_model()
                if not model:
                    handle_transcription_failure(job_id, "Whisper model not available.")
                    continue

                try:
                    print(f"--- Starting Transcription for {audio_path} ---")
                    result = model.transcribe(audio_path, verbose=True)
                    transcript_text = result['text']
                    print("--- Transcription Finished ---")
                    
                    print("--- Generating Notes with Ollama ---")
                    notes_md = generate_notes_with_ollama(transcript_text)
                    print("--- Notes Generation Finished ---")

                    db = get_db()
                    default_folder = db.execute("SELECT id FROM folders WHERE name = 'Unorganized'").fetchone()
                    default_folder_id = default_folder['id'] if default_folder else None

                    cursor = db.cursor()
                    cursor.execute("INSERT INTO transcripts (filename, transcript_text, folder_id) VALUES (?, ?, ?)",
                                   (original_filename, transcript_text, default_folder_id))
                    transcript_id = cursor.lastrowid
                    
                    cursor.execute("INSERT INTO notes (transcript_id, notes_text) VALUES (?, ?)", (transcript_id, notes_md))
                    
                    db.commit()
                    
                    db.execute("UPDATE transcription_queue SET status = 'completed', transcript_id = ? WHERE id = ?", (transcript_id, job_id))
                    db.commit()
                    db.close()

                    if os.path.exists(audio_path):
                        os.remove(audio_path)

                    db = get_db()
                    db.execute("DELETE FROM transcription_queue WHERE id = ?", (job_id,))
                    db.commit()
                    db.close()
                    print(f"Job {job_id} finalized and removed from queue.")

                except Exception as e:
                    print(f"An error occurred during transcription for job {job_id}: {e}")
                    handle_transcription_failure(job_id, str(e))

            else:
                print("No queued jobs found. Worker is going to sleep.")
                new_job_event.clear()
                db.close()

def handle_transcription_failure(job_id, error_message):
    """Updates the queue with failure information."""
    db = get_db()
    db.execute("UPDATE transcription_queue SET status = 'failed', error_message = ? WHERE id = ?", (error_message, job_id))
    db.commit()
    db.close()

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file found'}), 400

    audio_file = request.files['audio']
    _, file_extension = os.path.splitext(audio_file.filename)
    safe_filename = str(uuid.uuid4()) + (file_extension or '.tmp')
    audio_path = os.path.join(UPLOAD_FOLDER, safe_filename)
    audio_file.save(audio_path)

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO transcription_queue (audio_path, original_filename) VALUES (?, ?)",
        (audio_path, audio_file.filename or "recording")
    )
    job_id = cursor.lastrowid
    db.commit()
    db.close()

    new_job_event.set()
    return jsonify({'job_id': job_id})

@app.route('/status/<int:job_id>')
def get_status(job_id):
    db = get_db()
    job = db.execute("SELECT status, transcript_id, error_message FROM transcription_queue WHERE id = ?", (job_id,)).fetchone()
    db.close()
    if job is None:
        return jsonify({'status': 'completed'})
    return jsonify(dict(job))

@app.route('/history')
def get_history():
    db = get_db()
    folders = db.execute("SELECT id, name FROM folders ORDER BY created_at DESC").fetchall()
    transcripts = db.execute("SELECT id, filename, created_at, folder_id FROM transcripts ORDER BY created_at DESC").fetchall()
    db.close()

    folder_data = []
    for folder in folders:
        folder_dict = dict(folder)
        folder_dict['transcripts'] = [dict(t) for t in transcripts if t['folder_id'] == folder['id']]
        folder_data.append(folder_dict)

    unfiled_transcripts = [dict(t) for t in transcripts if t['folder_id'] is None]
    return jsonify({'folders': folder_data, 'unfiled': unfiled_transcripts})

@app.route('/session/<int:transcript_id>')
def get_session_data(transcript_id):
    db = get_db()
    transcript_row = db.execute("SELECT transcript_text FROM transcripts WHERE id = ?", (transcript_id,)).fetchone()
    notes_row = db.execute("SELECT notes_text FROM notes WHERE transcript_id = ?", (transcript_id,)).fetchone()
    chat_rows = db.execute("SELECT sender, message FROM chat_history WHERE transcript_id = ? ORDER BY created_at ASC", (transcript_id,)).fetchall()
    db.close()

    if not transcript_row or not notes_row:
        return jsonify({'error': 'Session data not found'}), 404

    session['current_transcript_id'] = transcript_id
    return jsonify({
        'transcript_text': transcript_row['transcript_text'],
        'notes_markdown': notes_row['notes_text'],
        'chat_history': [dict(row) for row in chat_rows]
    })
    
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

@app.route('/delete/<int:transcript_id>', methods=['POST'])
def delete_session(transcript_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("DELETE FROM transcripts WHERE id = ?", (transcript_id,))
        db.commit()
        if session.get('current_transcript_id') == transcript_id:
            session.pop('current_transcript_id', None)
        return jsonify({'success': True})
    except sqlite3.Error as e:
        db.rollback()
        return jsonify({'error': f'Database error: {e}'}), 500
    finally:
        if db:
            db.close()

@app.route('/folders', methods=['POST'])
def create_folder():
    folder_name = request.json.get('name')
    if not folder_name:
        return jsonify({'error': 'Folder name not provided'}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO folders (name) VALUES (?)", (folder_name,))
    folder_id = cursor.lastrowid
    db.commit()
    db.close()
    return jsonify({'success': True, 'folder_id': folder_id})

@app.route('/folders/<int:folder_id>', methods=['DELETE'])
def delete_folder(folder_id):
    db = get_db()
    folder_to_delete = db.execute("SELECT name FROM folders WHERE id = ?", (folder_id,)).fetchone()
    if folder_to_delete and folder_to_delete['name'] == 'Unorganized':
        return jsonify({'error': 'Cannot delete the Unorganized folder.'}), 400

    unorganized_folder = db.execute("SELECT id FROM folders WHERE name = 'Unorganized'").fetchone()
    unorganized_folder_id = unorganized_folder['id'] if unorganized_folder else None

    db.execute("UPDATE transcripts SET folder_id = ? WHERE folder_id = ?", (unorganized_folder_id, folder_id,))
    db.execute("DELETE FROM folders WHERE id = ?", (folder_id,))
    db.commit()
    db.close()
    return jsonify({'success': True})

@app.route('/transcripts/<int:transcript_id>/move', methods=['POST'])
def move_transcript(transcript_id):
    folder_id = request.json.get('folder_id')
    folder_id = folder_id if folder_id else None
    db = get_db()
    db.execute("UPDATE transcripts SET folder_id = ? WHERE id = ?", (folder_id, transcript_id))
    db.commit()
    db.close()
    return jsonify({'success': True})

@app.route('/queue_status')
def queue_status():
    db = get_db()
    processing_row = db.execute("SELECT original_filename FROM transcription_queue WHERE status = 'processing' LIMIT 1").fetchone()
    queued_count_row = db.execute("SELECT COUNT(*) FROM transcription_queue WHERE status = 'queued'").fetchone()
    db.close()

    processing_file = processing_row['original_filename'] if processing_row else None
    queued_count = queued_count_row[0] if queued_count_row else 0
    return jsonify({'processing_file': processing_file, 'queued_count': queued_count})

if __name__ == '__main__':
    from database import init_db
    init_db()
    queue_processor_thread = threading.Thread(target=queue_processor, daemon=True)
    queue_processor_thread.start()
    new_job_event.set()
    # Corrected line: Use the variables, not strings
    cert_file = "jjawandas-pc.tailb4094d.ts.net.crt"
    key_file = "jjawandas-pc.tailb4094d.ts.net.key"

    # Use 0.0.0.0 so other devices on your Tailnet can access it
    app.run(host="0.0.0.0", port=443, ssl_context=(cert_file, key_file))