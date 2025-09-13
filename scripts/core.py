import whisper
import torch

# Check if a CUDA-enabled GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load the model and send it to the selected device
model = whisper.load_model("medium").to(device)

file_path = r'C:\Users\jaspr\OneDrive\Documents\Github\NotTurboAI\data\recordings\test.m4a'

# Transcribe with the progress bar enabled
print("Starting transcription...")
result = model.transcribe(file_path, verbose=True)
print("Transcription finished!")

print("\n--- Transcribed Text ---")
print(result["text"])