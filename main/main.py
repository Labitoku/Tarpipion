import sys
from odf import text, teletype
from odf.opendocument import load


class Gamme:
    
    def __init__(self):
        self.notes = ["C", "D", "E", "F", "G", "A", "B"]
        self.notesDown = ["C", "Db", "D", "Eb", "E", "Fb", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
        self.notesUp = ["C", "D", "D#", "E", "E#", "F", "F#", "G", "G#", "A", "A#", "B", "B#"]        
        self.bemol = "b"
        self.diese = "#"


    def switchNote(self, note, upping, qte):
        if upping:
            for i in range(len(self.notesUp)):
                if self.notesUp[i] == note.note:
                    note.note = self.notesUp[(i + qte) % len(self.notesUp)]            
                    break
        else:
            for i in range(len(self.notesDown)):
                if self.notesDown[i] == note.note:
                    note.note = self.notesDown[(i + qte) % len(self.notesDown)]            
                    break

        return note


class Note:

    def __init__(self, valeur):
        self.note = valeur



class Partition:

    def __init__(self, opendocument):
        self.gamme = Gamme()




class Ligne:

    def __init__(self, words):
        i = 1



class LigneGamme:
    def __init__(self):
        i = 1


"""#charger et afficher un texte
testdoc = load("test/a_textTest.odt")
print(testdoc.text)
"""

"""#detecter les differentes lignes
"""
#testdoc = load("test/b_DetectionLigne.odt")
#allparas = testdoc.getElementsByType(text.P)
#teletype.extractText(allparas[0])


if __name__ == '__main__':
    note = Note(sys.argv[1])
    gamme = Gamme()
    print(gamme.switchNote(note, False, 3).note)