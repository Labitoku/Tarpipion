import sys
from odf import text, teletype
from odf.opendocument import load


class Gamme:
    
    def __init__(self):
        self.notes = ["C", "D", "E", "F", "G", "A", "B"]
        self.notesBemol = ["C", "Db", "D", "Eb", "E", "Fb", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
        self.notesDiese = ["C", "D", "D#", "E", "E#", "F", "F#", "G", "G#", "A", "A#", "B", "B#"]        
        self.bemol = "b"
        self.diese = "#"


    def switchNote(self, note, upping, qte):
        new_note = Note(note.note)
        if upping:
            for i in range(len(self.notesDiese)):
                if self.notesDiese[i] == new_note.note:
                    new_note.note = self.notesDiese[(i + qte) % len(self.notesDiese)]            
                    break
        else:
            for i in range(len(self.notesBemol)):
                if self.notesBemol[i] == new_note.note:
                    new_note.note = self.notesBemol[(i + qte) % len(self.notesBemol)]            
                    break

        return new_note


class Note:

    def __init__(self, valeur):
        self.note = valeur

class NoteSet:

    def __init__(self, ligne):
        self.notes = []
        self.gamme = Gamme()
        text = teletype.extractText(ligne)
        
        for i in range(len(text)):
            if text[i] in self.gamme.notes:
                new_note = text[i]
                if text[i + 1] == "b":
                    new_note += "b"
                elif text[i + 1] == "#":
                    new_note += "#"
                self.notes.append(Note(new_note))

    def show_noteset(self):
        noteset = "["
        for i in range(len(self.notes)):
            noteset += self.notes[i].note
            if i != len(self.notes):
                noteset += ", "
        noteset += "]"
        print(noteset)

    def switch_notes(self, upping, qte):
        for i in range(len(self.notes)):
            self.notes[i] = self.gamme.switchNote(self.notes[i], upping, qte)

    def __getitem__(self, a):
        return self.notes[a]

class Partition:

    def __init__(self, opendocument):
        self.gamme = Gamme()
        
        self.partition = opendocument
        self.allText = self.partition.getElementsByType(text.P)
        
        self.bemol = False
        
        self.lignes = []
        self.notes = []
        self.cpt = 0
        
        self.line_identification()
        self.set_notes()

    #permet de repérer quelles lignes sont pour les notes desquelles sont pour les paroles
    def line_identification(self):
        #teletype.extractText(allText[0])
        for i in range(len(self.allText)):
            if self.noteline_identification(self.allText[i]):
                self.lignes.append(i)
                #print("Ligne de note à la ligne : " + str(self.lignes[self.cpt]))
                self.cpt += 1

    #permet de détecter une ligne de notes  -> determine aussi si on est en diese ou en bemol
    def noteline_identification(self, ligne):
        text = teletype.extractText(ligne)
        bemol_det = False
        for i in range(len(text)):
            if(self.check_char_note(text[i])):
                if(text[i+1].lower() == "m" or text[i+1] == " " or text[i+1] == "#" or text[i+1] == "b"):
                    if(text[i+1] == "b" and bemol_det == False):
                        self.bemol = True
                        bemol_det == True
                    elif(text[i+1] == "#" and bemol_det == False):
                        self.bemol = False
                        bemol_det == True
                    return True
        return False


    def check_char_note(self, char):
        if(char in self.gamme.notes):
            return True

    #permet de stocker localement toutes les notes de la partition
    def set_notes(self):
        for i in range(len(self.lignes)):
            self.notes.append(NoteSet(self.allText[self.lignes[i]]))
            self.notes[i].show_noteset()

    def reset_notes(self):
        self.notes.clear()
        for i in range(len(self.lignes)):
            self.notes.append(NoteSet(self.allText[self.lignes[i]]))
            self.notes[i].show_noteset()
        print("RESETING DONE !\n")

    #permet d'obtenir un index d'une note dans le tableau correspondant
    def get_char_index(self, char):
        if(self.bemol):
            for i in self.gamme.notesBemol:
                if gamme.notesBemol[i] == char:
                    return i
        else:
            for i in self.gamme.notesDiese:
                if gamme.notesDiese[i] == char:
                    return i


    def switch_type(self):
        if(self.bemol):
            for i in range(len(self.lignes)):
                j = 4         

    def switch_notes(self, upping, qte):

        for i in range(len(self.lignes)):
            #print(self.allText[self.lignes[i]])
            #ligne de notes
            old_text = teletype.extractText(self.allText[self.lignes[i]])
            newer_text = ""
            new_notes = []

            for j in range(len(self.notes[i].notes)):
                new_notes.append(self.gamme.switchNote(self.notes[i].notes[j], upping, qte).note)


            print("NOTESET")
            self.notes[i].show_noteset()

            print("NEW NOTESET : " + str(new_notes))            

            cpt = 0
        
            
            for j in range (len(old_text) - 1):
                if old_text[j] != " " and old_text[j] != "/" and (old_text[j] == self.notes[i].notes[cpt].note or (old_text[j] + old_text[j+1]) == self.notes[i].notes[cpt].note):
                    print("NEW NOTE")
                    newer_text += new_notes[cpt]
                    cpt += 1
                    if(cpt == len(new_notes)):
                        newer_text += " "
                        break
                else:
                    if(old_text[j] != "b" and old_text[j] != "#"):
                        newer_text += old_text[j]

            print("OLD TEXT  : " + old_text)
            print("NEW TEXT : " + newer_text)

            new_S = text.P()
            new_S.setAttribute("stylename", self.allText[self.lignes[i]].getAttribute("stylename"))
            new_S.addText(newer_text)
            self.allText[self.lignes[i]] = new_S

#        print("\n\n\n")
 #       for i in range(len(self.allText)):
  #          print(self.allText[i])

        self.reset_notes()





if __name__ == '__main__':

    """#charger et afficher un texte
    testdoc = load("test/a_textTest.odt")
    print(testdoc.text)
    """

    """#detecter les differentes lignes
    """
    #testdoc = load("test/b_DetectionLigne.odt")
    #allparas = testdoc.getElementsByType(text.P)
    #teletype.extractText(allparas[0])


    """
    note = Note(sys.argv[1])
    gamme = Gamme()
    print(gamme.switchNote(note, False, 3).note)
    """
    gamme = Gamme()
    testdoc = load("test/d_TranspoTest.odt")
    partition = Partition(testdoc)
    partition.switch_notes(True, 3)

    partition.switch_notes(True, 6)
   # partition.switch_notes(True, 0)
