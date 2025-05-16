import whisper


model = whisper.load_model("base")


result = model.transcribe("try.mp3")

print(result["text"])

