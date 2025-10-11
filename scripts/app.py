"""
app.py

Server entry point for the LectureScribe application.

This module implements the web interface for the LectureScribe note-taking and transcript management system using FastAPI. It provides:

- Audio transcription using Whisper AI.
- Automated note generation from transcripts using Ollama LLM.
- Session management for multiple transcripts and notes stored in physical folders.
- RESTful API endpoints for transcript, note, and chat history management.
- Interactive chat assistant grounded in user notes and transcripts.
- Secure upload and deletion of audio files and session data.
- Integration with database operations in database.py.
- Persistent, database-backed background transcription queue.
- Real-time queue status endpoint.

The architecture separates web presentation, business logic, and data access, supporting extensibility and robust error handling. Security features include session-based access control and file validation. The application is designed for deployment in a secure, internal environment.

Author: Jaspreet Jawanda
Email: jaspreetjawanda@proton.me
Version: 2.1
Status: Production
"""

import os
import uuid
import torch
import whisper
import requests
import json
import sqlite3
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Response
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import threading
import time

# --- Configuration ---
UPLOAD_FOLDER = '../uploads'
DATA_FOLDER = '../data'
DATABASE_FILE = '../data/lecturescribe.db'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

# --- Global variables for the background queue processor ---
queue_lock = threading.Lock()
new_job_event = threading.Event()

# --- FastAPI App Initialization ---
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
TEMPLATES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = FastAPI()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory=TEMPLATES_FOLDER)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=os.urandom(24).hex())

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str

class FolderCreate(BaseModel):
    name: str

class SessionNameUpdate(BaseModel):
    name: str

class TranscriptMove(BaseModel):
    folder_id: Optional[int] = None


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
    "options": {
        "temperature": 0.2,
        "top_p": 0.9
    }
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

CHAT_PROMPT_TEMPLATE = """
You are a careful and precise assistant.

Rules:
- Use ONLY the information in the provided lecture notes and conversation history.
- Do NOT add, guess, or infer details that are not explicitly stated.
- If the information is missing or unclear, respond with: "I can't answer that based on the provided notes."
- Prefer bullet points and concise phrasing when summarizing.
- Maintain the original meaning of the notes without reinterpreting.

--- Lecture Notes ---
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

                    # Create a new directory for the session data
                    session_folder_name = f"{original_filename}_{str(uuid.uuid4())[:8]}"
                    session_folder_path = os.path.join(DATA_FOLDER, session_folder_name)
                    os.makedirs(session_folder_path, exist_ok=True)

                    # Save transcript, notes, and chat history to files
                    with open(os.path.join(session_folder_path, 'transcript.txt'), 'w', encoding='utf-8') as f:
                        f.write(transcript_text)
                    with open(os.path.join(session_folder_path, 'notes.md'), 'w', encoding='utf-8') as f:
                        f.write(notes_md)
                    with open(os.path.join(session_folder_path, 'chat_history.json'), 'w', encoding='utf-8') as f:
                        json.dump([], f) # Start with an empty chat history

                    cursor = db.cursor()
                    cursor.execute("INSERT INTO transcripts (filename, data_path, folder_id) VALUES (?, ?, ?)",
                                   (original_filename, session_folder_path, default_folder_id))
                    transcript_id = cursor.lastrowid
                    
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

# --- FastAPI Routes ---
@app.get("/")
async def index(request: Request):
    """Serve the main HTML page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/manifest.json")
async def get_manifest():
    """Serve the manifest.json file"""
    manifest_path = os.path.join(STATIC_FOLDER, 'manifest.json')
    if os.path.exists(manifest_path):
        return FileResponse(manifest_path, media_type="application/json")
    raise HTTPException(status_code=404, detail="Manifest not found")

@app.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """Upload audio file and queue it for transcription"""
    if not audio:
        raise HTTPException(status_code=400, detail="No audio file found")

    _, file_extension = os.path.splitext(audio.filename)
    safe_filename = str(uuid.uuid4()) + (file_extension or '.tmp')
    audio_path = os.path.join(UPLOAD_FOLDER, safe_filename)
    
    # Save uploaded file
    with open(audio_path, 'wb') as f:
        content = await audio.read()
        f.write(content)

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO transcription_queue (audio_path, original_filename) VALUES (?, ?)",
        (audio_path, audio.filename or "recording")
    )
    job_id = cursor.lastrowid
    db.commit()
    db.close()

    new_job_event.set()
    return {"job_id": job_id}

@app.get("/status/{job_id}")
async def get_status(job_id: int):
    """Get the status of a transcription job"""
    db = get_db()
    job = db.execute("SELECT status, transcript_id, error_message FROM transcription_queue WHERE id = ?", (job_id,)).fetchone()
    db.close()
    if job is None:
        return {"status": "completed"}
    return dict(job)

@app.get("/history")
async def get_history():
    """Get all folders and transcripts"""
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
    return {"folders": folder_data, "unfiled": unfiled_transcripts}

@app.get("/session/{transcript_id}")
async def get_session_data(transcript_id: int, request: Request):
    """Get session data for a specific transcript"""
    db = get_db()
    transcript_row = db.execute("SELECT data_path FROM transcripts WHERE id = ?", (transcript_id,)).fetchone()
    db.close()

    if not transcript_row:
        raise HTTPException(status_code=404, detail="Session data not found")

    data_path = transcript_row['data_path']
    try:
        with open(os.path.join(data_path, 'transcript.txt'), 'r', encoding='utf-8') as f:
            transcript_text = f.read()
        with open(os.path.join(data_path, 'notes.md'), 'r', encoding='utf-8') as f:
            notes_markdown = f.read()
        with open(os.path.join(data_path, 'chat_history.json'), 'r', encoding='utf-8') as f:
            chat_history = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Session files not found")

    # Store in session
    request.session['current_transcript_id'] = transcript_id
    request.session['current_data_path'] = data_path
    
    return {
        'transcript_text': transcript_text,
        'notes_markdown': notes_markdown,
        'chat_history': chat_history
    }
    
@app.post("/chat")
async def chat(chat_request: ChatRequest, request: Request):
    """Chat with the AI assistant about the notes"""
    user_message = chat_request.message
    transcript_id = request.session.get('current_transcript_id')
    data_path = request.session.get('current_data_path')

    if not user_message or not transcript_id or not data_path:
        raise HTTPException(status_code=400, detail="Missing message or session context")

    try:
        with open(os.path.join(data_path, 'notes.md'), 'r', encoding='utf-8') as f:
            notes_context = f.read()
        with open(os.path.join(data_path, 'chat_history.json'), 'r', encoding='utf-8') as f:
            chat_history = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Could not retrieve notes or chat history for context")

    ai_response = get_chat_response(user_message, notes_context, chat_history)
    
    chat_history.append({'sender': 'user', 'message': user_message})
    chat_history.append({'sender': 'ai', 'message': ai_response})

    with open(os.path.join(data_path, 'chat_history.json'), 'w', encoding='utf-8') as f:
        json.dump(chat_history, f)

    return {"response": ai_response}

@app.post("/edit/{transcript_id}")
async def edit_session_name(transcript_id: int, update: SessionNameUpdate):
    """Edit the name of a transcript session"""
    new_name = update.name
    if not new_name:
        raise HTTPException(status_code=400, detail="New name not provided")
    db = get_db()
    db.execute("UPDATE transcripts SET filename = ? WHERE id = ?", (new_name, transcript_id))
    db.commit()
    db.close()
    return {"success": True}

@app.post("/delete/{transcript_id}")
async def delete_session(transcript_id: int, request: Request):
    """Delete a transcript session"""
    db = get_db()
    transcript_row = db.execute("SELECT data_path FROM transcripts WHERE id = ?", (transcript_id,)).fetchone()
    
    if transcript_row:
        shutil.rmtree(transcript_row['data_path'], ignore_errors=True)

    db.execute("DELETE FROM transcripts WHERE id = ?", (transcript_id,))
    db.commit()
    db.close()
    
    if request.session.get('current_transcript_id') == transcript_id:
        request.session.pop('current_transcript_id', None)
        request.session.pop('current_data_path', None)
        
    return {"success": True}

@app.post("/folders")
async def create_folder(folder: FolderCreate):
    """Create a new folder"""
    folder_name = folder.name
    if not folder_name:
        raise HTTPException(status_code=400, detail="Folder name not provided")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO folders (name) VALUES (?)", (folder_name,))
    folder_id = cursor.lastrowid
    db.commit()
    db.close()
    return {"success": True, "folder_id": folder_id}

@app.delete("/folders/{folder_id}")
async def delete_folder(folder_id: int):
    """Delete a folder"""
    db = get_db()
    folder_to_delete = db.execute("SELECT name FROM folders WHERE id = ?", (folder_id,)).fetchone()
    if folder_to_delete and folder_to_delete['name'] == 'Unorganized':
        raise HTTPException(status_code=400, detail="Cannot delete the Unorganized folder.")

    unorganized_folder = db.execute("SELECT id FROM folders WHERE name = 'Unorganized'").fetchone()
    unorganized_folder_id = unorganized_folder['id'] if unorganized_folder else None

    db.execute("UPDATE transcripts SET folder_id = ? WHERE folder_id = ?", (unorganized_folder_id, folder_id,))
    db.execute("DELETE FROM folders WHERE id = ?", (folder_id,))
    db.commit()
    db.close()
    return {"success": True}

@app.post("/transcripts/{transcript_id}/move")
async def move_transcript(transcript_id: int, move_data: TranscriptMove):
    """Move a transcript to a different folder"""
    folder_id = move_data.folder_id
    db = get_db()
    db.execute("UPDATE transcripts SET folder_id = ? WHERE id = ?", (folder_id, transcript_id))
    db.commit()
    db.close()
    return {"success": True}

@app.get("/queue_status")
async def queue_status():
    """Get the current status of the transcription queue"""
    db = get_db()
    processing_row = db.execute("SELECT original_filename FROM transcription_queue WHERE status = 'processing' LIMIT 1").fetchone()
    queued_count_row = db.execute("SELECT COUNT(*) FROM transcription_queue WHERE status = 'queued'").fetchone()
    db.close()

    processing_file = processing_row['original_filename'] if processing_row else None
    queued_count = queued_count_row[0] if queued_count_row else 0
    return {"processing_file": processing_file, "queued_count": queued_count}

# Mount static files after all routes are defined
app.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="static")


if __name__ == '__main__':
    from database import init_db
    import uvicorn
    
    init_db()
    queue_processor_thread = threading.Thread(target=queue_processor, daemon=True)
    queue_processor_thread.start()
    new_job_event.set()
    
    # SSL certificate files
    cert_file = "jjawandas-pc.tailb4094d.ts.net.crt"
    key_file = "jjawandas-pc.tailb4094d.ts.net.key"

    # Use uvicorn to run the FastAPI app with SSL
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=443,
        ssl_certfile=cert_file,
        ssl_keyfile=key_file
    )
    # For development without SSL, use:
    # uvicorn.run(app, host="0.0.0.0", port=5000)