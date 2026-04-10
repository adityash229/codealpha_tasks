import glob
import pickle
import numpy as np
from music21 import converter, instrument, note, chord

def get_notes():
    notes = []
    # Ensure you have .mid files in the 'midi_data' folder
    for file in glob.glob("midi_data/*.mid"):
        midi = converter.parse(file)
        print(f"Parsing {file}")
        
        notes_to_parse = None
        try: # File has instrument parts
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse() 
        except: # File has notes in a flat structure
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    with open('data/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)

    return notes

# Run this to extract notes
# get_notes()