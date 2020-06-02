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
        self.partition = opendocument
        self.lignes = []
        self.line_identification()


    def line_identification(self):
        allText = self.partition.getElementsByType(text.P)
        #teletype.extractText(allText[0])
        for i in range(len(allText)):
            #if(allText[i])
            if self.noteline_identification(allText[i]):
                print("Ligne de note à la ligne : " + str(i))

            

    def noteline_identification(self, ligne):
        text = teletype.extractText(ligne)
        
        for i in range(len(text)):
            if(len(text) > 5):
                if(self.check_char_note(text[i])):
                    if(text[i+1].lower() == 'm' or text[i+1] == ' ' or text[i+1] == '#' or text[i+1] == 'b'):
                        return True

#                    if(text[i+1] == ' '):
 #                       if(text[i+2] == ' '):
   #                         if(text[i+3] == ' '):
    #                            return True

        return False

    def check_char_note(self, char):
        if(char in gamme.notes):
            return True

    """def check_line_word(self, line):
        if()
"""
"""    old_text = teletype.extractText(texts[i])
    new_text = old_text.replace('something','something else')
    new_S = text.P()
    new_S.setAttribute("stylename",texts[i].getAttribute("stylename"))
    new_S.addText(new_text)
    texts[i].parentNode.insertBefore(new_S,texts[i])
    texts[i].parentNode.removeChild(texts[i])
"""



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
    """
    note = Note(sys.argv[1])
    gamme = Gamme()
    print(gamme.switchNote(note, False, 3).note)"""
    gamme = Gamme()
    testdoc = load("test/c_IdentificationDeLigne.odt")
    partition = Partition(testdoc)

