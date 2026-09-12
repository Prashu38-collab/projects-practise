import re
from word2number import w2n

def convert_words_to_number(text):
    #  text lowercase
    text = text.lower()

    #  Remove dashes or hyphens
    text = text.replace("-", " ")

    # Remove currency words
    text = re.sub(r"\brupees\b", "", text)
    text = re.sub(r"\brupee\b", "", text)
    text = re.sub(r"\bpaise\b", "", text)
    
    #  Clean up extra spaces and remove the word and
    text = text.replace(" and ", " ")
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return 0

    # Handle the Indian numbering system manually
    total = 0
    
    # Check for crore 
    if "crore" in text:
        parts = text.split("crore")
        total += w2n.word_to_num(parts[0].strip()) * 10000000
        text = parts[1].strip()

    # Check for lakh 
    if "lakh" in text:
        parts = text.split("lakh")
        total += w2n.word_to_num(parts[0].strip()) * 100000
        text = parts[1].strip()

    # Convert the remaining standard English words
    if text:
        try:
            total += w2n.word_to_num(text)
        except ValueError:
            return "Invalid words"
            
    return total
print(convert_words_to_number("one hundred and twenty-three"))
print(convert_words_to_number("two lakh and fifty thousand"))
print(convert_words_to_number("two crore fifty lakh"))