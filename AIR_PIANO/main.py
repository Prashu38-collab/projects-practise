# 61 keys keyboard
'''
1. Create a list of notes C2 TO C7
2. Identify black note and white note
'''


# steps

notes_name=["C", "C#", "D", "D#", "E",
    "F", "F#", "G", "G#", "A", "A#", "B"]
notes=[]
for octave in range(2,7):
    for note in notes_name:
        notes.append(note+str(octave))

notes.append("C7")
print(len(notes))
print(notes)

# black and white notes
black_notes=[]
white_notes=[]
for note in notes:
    if '#' in note:
        black_notes.append(note)
    else:
        white_notes.append(note)
print(len(white_notes))
print(len(black_notes))

