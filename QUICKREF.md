# Flask to FastAPI Migration - Quick Reference

## Installation Command Changes

### Before (Flask)
```bash
pip install flask torch requests whisper
```

### After (FastAPI)
```bash
pip install -r requirements.txt
# or
pip install fastapi uvicorn python-multipart jinja2 torch requests whisper
```

## Running the Application

### Before (Flask)
```bash
# Windows
scripts\start_flask.bat

# Python
python scripts/app.py
```

### After (FastAPI)
```bash
# Windows
scripts\start_server.bat

# Python
python scripts/app.py

# Or using uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 5000
```

## Code Patterns Comparison

### Route Definition

#### Flask
```python
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    return jsonify({'response': ai_response})
```

#### FastAPI
```python
@app.post("/chat")
async def chat(chat_request: ChatRequest):
    user_message = chat_request.message
    return {"response": ai_response}
```

### File Upload

#### Flask
```python
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    audio_file = request.files['audio']
    audio_file.save(audio_path)
```

#### FastAPI
```python
@app.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    with open(audio_path, 'wb') as f:
        content = await audio.read()
        f.write(content)
```

### Error Handling

#### Flask
```python
if not folder_name:
    return jsonify({'error': 'Folder name not provided'}), 400
```

#### FastAPI
```python
if not folder_name:
    raise HTTPException(status_code=400, detail="Folder name not provided")
```

### Session Access

#### Flask
```python
transcript_id = session.get('current_transcript_id')
session['current_transcript_id'] = transcript_id
```

#### FastAPI
```python
async def get_session_data(transcript_id: int, request: Request):
    transcript_id = request.session.get('current_transcript_id')
    request.session['current_transcript_id'] = transcript_id
```

### Template Rendering

#### Flask
```python
@app.route('/')
def index():
    return render_template('index.html')
```

#### FastAPI
```python
templates = Jinja2Templates(directory=TEMPLATES_FOLDER)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

## New Features Available

### 1. Automatic API Documentation
FastAPI automatically generates interactive API documentation:
- **Swagger UI**: Available at `http://localhost:5000/docs`
- **ReDoc**: Available at `http://localhost:5000/redoc`

### 2. Request Validation
Pydantic models provide automatic validation:
```python
class ChatRequest(BaseModel):
    message: str  # Automatically validated as required string
```

### 3. Type Hints
Better IDE support and type checking:
```python
async def get_status(job_id: int) -> dict:
    # IDE knows job_id is an int and return type is dict
```

### 4. Dependency Injection
FastAPI supports dependency injection (not used yet, but available):
```python
async def get_current_user(request: Request):
    return request.session.get('user')

@app.get("/protected")
async def protected_route(user = Depends(get_current_user)):
    # user is automatically injected
```

## Performance Improvements
- **ASGI vs WSGI**: FastAPI uses ASGI (asynchronous) instead of WSGI (synchronous)
- **Async/Await**: All routes are async, allowing better concurrency
- **uvicorn**: Production-ready ASGI server with better performance than Flask's dev server

## Compatibility Notes

### What Stayed the Same
✓ All API endpoints work with the same URLs
✓ Request/response formats unchanged
✓ Database operations identical
✓ Background queue processor unchanged
✓ Session data storage compatible
✓ Static file serving works the same way
✓ SSL/HTTPS configuration preserved

### What Changed (Internal Only)
- Import statements
- Route decorator syntax
- Request object access patterns
- Response creation methods
- Application initialization

## Testing the Migration

Run the included test suite:
```bash
python test_migration.py
```

This validates:
- All FastAPI patterns are in place
- No Flask patterns remain
- Configuration files are updated
- All imports work correctly

## Troubleshooting

### Issue: "No module named 'fastapi'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Templates not found
**Solution**: Ensure templates folder exists at `scripts/templates/`

### Issue: Static files 404
**Solution**: Check that static files are mounted after all routes:
```python
app.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="static")
```

### Issue: Session not persisting
**Solution**: Ensure SessionMiddleware is added:
```python
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
```

## Next Steps

Consider these FastAPI features for future enhancements:
1. **OpenAPI Schema**: Already generated automatically
2. **WebSockets**: For real-time transcription updates
3. **Background Tasks**: For async processing without threads
4. **Dependency Injection**: For cleaner code organization
5. **Request Validation**: Expand Pydantic models for all endpoints
6. **Response Models**: Define response schemas for better documentation
