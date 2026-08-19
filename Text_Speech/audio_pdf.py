import pyttsx3
import PyPDF2

# read book in binary format
with open('/Users/prashamsaghimire/Desktop/Projects/Text_Speech/aboutMe.pdf','rb') as file:
    reading_pdf=PyPDF2.PdfReader(file)

# number of pages
    pdf_pages = len(reading_pdf.pages)

# Convert it to speech 

pdf_speaker=pyttsx3.init() #initialize library
#  IT WILL READ INDEX WISE SO FOR READING 4 PAGE- PROVIDE 3
choose_page=reading_pdf.pages[0]
pdf_text=choose_page.extract_text()
print(pdf_text)
pdf_speaker.say(pdf_text)
pdf_speaker.runAndWait()