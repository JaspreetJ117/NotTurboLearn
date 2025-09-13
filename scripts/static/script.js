document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const recordBtn = document.getElementById('recordBtn');
    const recordBtnText = document.getElementById('recordBtnText');
    const uploadInput = document.getElementById('uploadInput');
    const loader = document.getElementById('loader');
    const loaderText = document.getElementById('loader-text');
    const loaderStatus = document.getElementById('loader-status');
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress-bar');
    const historyList = document.getElementById('history-list');
    const notesOutput = document.getElementById('notes-output');
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatSubmitBtn = document.getElementById('chat-submit-btn');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    const sidebar = document.querySelector('.sidebar');

    // --- State Management ---
    let isRecording = false;
    let mediaRecorder;
    let audioChunks = [];

    // --- Core Functions ---
    const loadHistory = async () => {
        try {
            const response = await fetch('/history');
            if (!response.ok) throw new Error('Failed to fetch history.');
            const history = await response.json();

            historyList.innerHTML = '';
            if (history.length === 0) {
                historyList.innerHTML = '<p class="placeholder">No sessions yet.</p>';
                return;
            }

            history.forEach(item => {
                const div = document.createElement('div');
                div.className = 'history-item';
                div.dataset.id = item.id;
                
                const fileName = item.filename || 'Recording';
                const date = new Date(item.created_at).toLocaleString();

                div.innerHTML = `
                    <div class="history-item-info">
                        <p class="filename">${fileName}</p>
                        <p class="date">${date}</p>
                    </div>
                    <div class="history-item-actions">
                        <button class="edit-btn" title="Edit Name">✏️</button>
                        <button class="delete-btn" title="Delete Session">🗑️</button>
                    </div>
                `;
                div.querySelector('.history-item-info').addEventListener('click', () => loadSession(item.id));
                div.querySelector('.edit-btn').addEventListener('click', (e) => {
                    e.stopPropagation();
                    editSessionName(item.id, fileName);
                });
                div.querySelector('.delete-btn').addEventListener('click', (e) => {
                    e.stopPropagation();
                    deleteSession(item.id);
                });
                historyList.appendChild(div);
            });
        } catch (error) {
            console.error('Failed to load history:', error);
            historyList.innerHTML = `<p class="placeholder">Could not load history.</p>`;
        }
    };

    const loadSession = async (transcriptId) => {
        showLoader(true, 'Loading session...');
        try {
            const response = await fetch(`/session/${transcriptId}`);
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            const data = await response.json();
            
            renderNotes(data.notes_markdown);
            renderChatHistory(data.chat_history);
            enableChat();
            
            document.querySelectorAll('.history-item').forEach(item => {
                item.classList.toggle('active', item.dataset.id == transcriptId);
            });
        } catch (error) {
            alert(`Failed to load session: ${error.message}`);
        } finally {
            showLoader(false);
        }
    };

    const sendAudioWithProgress = (audioData, fileName) => {
        const formData = new FormData();
        formData.append('audio', audioData, fileName);

        showLoader(true, 'Uploading...');
        loaderStatus.textContent = '';
        progressContainer.classList.remove('hidden');

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/transcribe', true);

        xhr.upload.onprogress = (event) => {
            if (event.lengthComputable) {
                const percentComplete = Math.round((event.loaded / event.total) * 100);
                progressBar.style.width = percentComplete + '%';
                if (percentComplete === 100) {
                    loaderText.textContent = 'Processing...';
                    loaderStatus.textContent = 'Transcribing audio with Whisper...';
                }
            }
        };

        xhr.onload = async () => {
            loaderStatus.textContent = 'Generating notes with Ollama...';
            if (xhr.status >= 200 && xhr.status < 300) {
                const data = JSON.parse(xhr.responseText);
                renderNotes(data.notes_markdown);
                renderChatHistory([]);
                await loadHistory();
                if (data.transcript_id) {
                    const newItem = historyList.querySelector(`[data-id='${data.transcript_id}']`);
                    if (newItem) newItem.click();
                    enableChat();
                }
            } else {
                let errorMessage = `HTTP error! Status: ${xhr.status}`;
                try {
                    const errData = JSON.parse(xhr.responseText);
                    errorMessage = errData.error || errorMessage;
                } catch (e) {}
                renderNotes(`## Upload Failed\n\n${errorMessage}`);
            }
            showLoader(false);
        };
        
        xhr.onerror = () => {
            renderNotes(`## Upload Failed\n\nCould not connect to the server.`);
            showLoader(false);
        };

        xhr.send(formData);
    };

    const editSessionName = async (transcriptId, currentName) => {
        const newName = prompt("Enter a new name for this session:", currentName);
        if (newName && newName.trim() !== "") {
            try {
                const response = await fetch(`/edit/${transcriptId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: newName.trim() })
                });
                if (!response.ok) throw new Error('Failed to save new name.');
                loadHistory();
            } catch (error) {
                alert(`Error: ${error.message}`);
            }
        }
    };

    const deleteSession = async (transcriptId) => {
        if (confirm("Are you sure you want to delete this session? This action cannot be undone.")) {
            try {
                const response = await fetch(`/delete/${transcriptId}`, { method: 'POST' });
                if (!response.ok) throw new Error('Failed to delete session.');
                
                const activeItem = document.querySelector('.history-item.active');
                if (activeItem && activeItem.dataset.id == transcriptId) {
                    renderNotes('<div class="placeholder-content"><h3>Session Deleted</h3><p>Please select another session or start a new one.</p></div>');
                    renderChatHistory([]);
                    enableChat(false);
                }
                loadHistory();
            } catch (error) {
                alert(`Error: ${error.message}`);
            }
        }
    };
    
    // --- UI Update Functions ---
    const showLoader = (isLoading, text = 'Processing...') => {
        loaderText.textContent = text;
        loader.classList.toggle('hidden', !isLoading);
        if (!isLoading) {
            progressContainer.classList.add('hidden');
            progressBar.style.width = '0%';
            loaderStatus.textContent = '';
        }
    };
    
    const renderNotes = (markdown) => {
        notesOutput.innerHTML = markdown ? marked.parse(markdown) : '<div class="placeholder-content"><h3>Error</h3><p>Received empty notes from the server.</p></div>';
    };

    const renderChatHistory = (history) => {
        chatMessages.innerHTML = '';
        if (history && history.length > 0) {
            history.forEach(chat => addChatMessage(chat.message, chat.sender));
        } else {
            addChatMessage("Hello! Ask me anything about the loaded lecture notes.", 'ai');
        }
    };
    
    const addChatMessage = (message, sender) => {
        const messageEl = document.createElement('div');
        messageEl.className = `chat-bubble ${sender}-bubble`;
        messageEl.innerHTML = marked.parse(message);
        chatMessages.appendChild(messageEl);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const enableChat = (enabled = true) => {
        chatInput.disabled = !enabled;
        chatSubmitBtn.disabled = !enabled;
        chatInput.placeholder = enabled ? "Ask a question about the notes..." : "Upload or record audio to begin chat.";
    };
    
    const updateRecordingUI = () => {
        recordBtnText.textContent = isRecording ? 'Stop' : 'Record';
        recordBtn.classList.toggle('recording', isRecording);
    };

    // --- Event Handlers ---
    uploadInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            sendAudioWithProgress(file, file.name);
        }
    });

    recordBtn.addEventListener('click', async () => {
        if (isRecording) {
            mediaRecorder.stop();
        } else {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                isRecording = true;
                audioChunks = [];
                mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
                
                mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
                
                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    const fileName = `recording_${new Date().toISOString()}.webm`;
                    sendAudioWithProgress(audioBlob, fileName);
                    stream.getTracks().forEach(track => track.stop());
                    isRecording = false;
                    updateRecordingUI();
                };
                
                mediaRecorder.start();
                updateRecordingUI();
            } catch (err) {
                alert("Could not access microphone. Please check permissions.");
            }
        }
    });

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const userMessage = chatInput.value.trim();
        if (!userMessage) return;

        addChatMessage(userMessage, 'user');
        chatInput.value = '';
        chatInput.disabled = true;
        chatSubmitBtn.disabled = true;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage }),
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to get response.');
            addChatMessage(data.response, 'ai');
        } catch (error) {
            addChatMessage(`Error: ${error.message}`, 'ai');
        } finally {
            chatInput.disabled = false;
            chatSubmitBtn.disabled = false;
            chatInput.focus();
        }
    });

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(btn.dataset.tab).classList.add('active');
        });
    });

    // --- Sidebar Toggle for Mobile ---
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebarBackdrop = document.createElement('div');
    sidebarBackdrop.className = 'sidebar-backdrop';

    if (sidebarToggle) {
        document.body.appendChild(sidebarBackdrop);

        const toggleSidebar = () => {
            const isActive = sidebar.classList.contains('active');
            sidebar.classList.toggle('active', !isActive);
            sidebarBackdrop.classList.toggle('active', !isActive);
            document.body.style.overflow = !isActive ? 'hidden' : '';
        };

        sidebarToggle.addEventListener('click', toggleSidebar);
        sidebarBackdrop.addEventListener('click', toggleSidebar);

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && sidebar.classList.contains('active')) {
                toggleSidebar();
            }
        });
    }

    // --- Initial Load ---
    loadHistory();
});