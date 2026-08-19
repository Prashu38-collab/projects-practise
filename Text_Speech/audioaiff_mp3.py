import pyttsx3
import PyPDF2
import subprocess

pdf_path = '/Users/prashamsaghimire/Desktop/Projects/Text_Speech/aboutMe.pdf'
aiff_path = '/Users/prashamsaghimire/Desktop/Projects/Text_Speech/aboutMe.aiff'
mp3_path = '/Users/prashamsaghimire/Desktop/Projects/Text_Speech/aboutMe.mp3'

with open(pdf_path, 'rb') as file:
    reading_pdf = PyPDF2.PdfReader(file)
    pdf_text = reading_pdf.pages[0].extract_text()

speaker = pyttsx3.init()

speaker.save_to_file(pdf_text, aiff_path)
speaker.runAndWait()

subprocess.run([
    "ffmpeg",
    "-i",
    aiff_path,
    mp3_path
])

print("MP3 created successfully!")