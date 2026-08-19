import pyttsx3
import PyPDF2

with open('/Users/prashamsaghimire/Desktop/Projects/Text_Speech/aboutMe.pdf', 'rb') as file:

    reading_pdf = PyPDF2.PdfReader(file)

    pdf_pages = len(reading_pdf.pages)

    choose_page = reading_pdf.pages[0]

    pdf_text = choose_page.extract_text()

pdf_speaker = pyttsx3.init()

pdf_speaker.say(pdf_text)
pdf_speaker.runAndWait()

# save to aiff- mac supports this

pdf_speaker.save_to_file(pdf_text,'/Users/prashamsaghimire/Desktop/Projects/Text_Speech/aboutMe.aiff')
pdf_speaker.runAndWait()