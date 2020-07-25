# coding: utf8 
from odf import text, teletype
from odf.style import Style, TextProperties
from odf.opendocument import load, OpenDocumentText
from odf.text import Span


class Gamme:
    def __init__(self):
        self.notes = ["C", "D", "E", "F", "G", "A", "B"]
        self.notes_bemol = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
        self.notes_diese = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self.bemol = "b"
        self.diese = "#"
        self.iemes = ["1","2","3","4","5","6","7","8","9"]
        

    def switch_note(self, note, bemol, qte):
        new_note = Note(note.note)
        if bemol:
            for i, note_bemol in enumerate(self.notes_bemol):
                if note_bemol == new_note.note:
                    new_note.note = self.notes_bemol[(i + qte) % len(self.notes_bemol)]
                    break

        else:
            for i, note_diese in enumerate(self.notes_diese):
                if note_diese == new_note.note:
                    new_note.note = self.notes_diese[(i + qte) % len(self.notes_diese)]
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

        for i, txt in enumerate(text):

            if txt in self.gamme.notes:
                new_note = txt

                if text[i + 1] == "b":
                    new_note += "b"

                elif text[i + 1] == "#":
                    new_note += "#"

                self.notes.append(Note(new_note))

    def show_noteset(self):
        noteset = "Noteset : ["

        for i, note in enumerate(self.notes):
            noteset += note.note

            if i != len(self.notes):
                noteset += ", "

        noteset += "]"
        print(noteset)

    def switch_notes(self, bemol, qte):
        for note in self.notes:
            note = self.gamme.switch_note(note, bemol, qte)

    def is_bemol(self):
        for note in self.notes:
            if note.note.endswith("b"):
                return True

        return False


    def __getitem__(self, a):
        return self.notes[a]



class TxtNoteSet:
    def __init__(self, ligne):

        self.notes = []
        self.gamme = Gamme()
        text = ligne

        for i, txt in enumerate(text):

            if txt in self.gamme.notes:
                new_note = txt

                if text[i + 1] == "b":
                    new_note += "b"

                elif text[i + 1] == "#":
                    new_note += "#"

                self.notes.append(Note(new_note))

    def show_noteset(self):
        noteset = " Noteset : ["

        for i, note in enumerate(self.notes):
            noteset += note.note

            if i != len(self.notes):
                noteset += ", "

        noteset += "]"
        print(noteset)

    def switch_notes(self, bemol, qte):
        for note in self.notes:
            note = self.gamme.switch_note(note, bemol, qte)

    def is_bemol(self):
        for note in self.notes:
            if note.note.endswith("b"):
                return True

        return False

    def __getitem__(self, a):
        return self.notes[a]


class TxtPartition:
    def __init__(self, document):
        self.gamme = Gamme()

        self.partition = open(document, 'r+', encoding="utf-8")
        self.partition.seek(0)


        self.all_text = []
        self.surplus = []

        for line in self.partition:
            print(line)
            if line.endswith("\n"):
                new_line = line
                new_line = new_line[:-1]
                self.all_text.append(new_line)

            else:
                self.all_text.append(line)

        for i, line in enumerate(self.all_text):
            #if(self.all_text[i].startswith(" ")):
             #   self.all_text[i] = self.all_text[i][1:]
            if(not self.all_text[i].endswith("\n")):
                self.all_text[i] = self.all_text[i] + "\n"
        

        self.lignes = []

        self.titre = ""
        self.set_titre()
        self.remove_surplus()

        self.line_identification()
        print("LINES : ")
        print(self.lignes)        

        self.notes = []
        self.set_notes()




        self.bemol = self.set_bemol()

        
        #print("all text = " + self.all_text)

        #print("\n\nligne 4 : " + self.lignes[4])
        #print(self.lignes[4])

    def remove_surplus(self):

        cpt_lines = 0
        for i, line in enumerate(self.all_text):
            if cpt_lines < 3:
                if '-------' in self.all_text[0]:
                    cpt_lines += 1
                self.surplus.append(self.all_text[0])
                self.all_text.pop(0)
        if self.all_text[0].lower().startswith('\n'):
            self.surplus.append(self.all_text[0])
            self.all_text.pop(0)

    def add_surplus(self):
        for i, line in enumerate(self.surplus):
            self.all_text.insert(0, self.surplus[len(self.surplus) - 1 - i])


    # permet de repérer quelles lignes sont pour les notes desquelles sont pour les paroles
    def line_identification(self):
        for i, line in enumerate(self.all_text):
            print(str(i))
            if self.noteline_identification(self.all_text[i]):
                self.lignes.append(i)
                #print("Ligne de note à la ligne : " + str(self.lignes[self.cpt]))

    # permet de détecter une ligne de notes  -> determine aussi si on est en diese ou en bemol
    def noteline_identification(self, ligne):
        text = ligne
        for i, txt in enumerate(text):
            if self.check_char_note(txt):
                if(text[i] == "|" or text[i+1] == " " or text[i+1] == "#" or text[i+1] == "m" or (text[i+1] in self.gamme.iemes) or (text[i+1] == "b" and (text[i+2] == " " or text[i+2].lower == "m" or text[i+2] == "/"))):
                    return True
        return False

    def set_bemol(self):
        for i, _ in enumerate(self.lignes):
            if self.notes[i].is_bemol():
                print("BEMOL")
                return True

        print("DIESE")
        return False

    def check_char_note(self, char):
        if char in self.gamme.notes:
            return True
        return False

    # permet de stocker localement toutes les notes de la partition
    def set_notes(self):
        print("SETTING NOTES . . . ")
        for i, line in enumerate(self.lignes):
            self.notes.append(TxtNoteSet(self.all_text[self.lignes[i]]))
            self.notes[i].show_noteset()

    def reset_notes(self):
        self.notes.clear()
        for i, line in enumerate(self.lignes):
            self.notes.append(TxtNoteSet(self.all_text[line]))
            self.notes[i].show_noteset()

        print("RESETING DONE !\n")

    # permet d'obtenir un index d'une note dans le tableau correspondant
    def get_char_index(self, char):
        if self.bemol:
            for i, note in enumerate(self.gamme.notes_bemol):
                if note == char:
                    print("INDEX NOTE = " + str(i))
                    return i
        else:
            for i, note in enumerate(self.gamme.notes_diese):
                if note == char:
                    print("INDEX NOTE = " + str(i))
                    return i

        return -1


    def switch_type(self):
        for i, line in enumerate(self.lignes): 
            old_text = self.all_text[line]
            new_text = ""

            new_notes = []

            cpt = 0

            for j, note in enumerate(self.notes[i].notes):
                ind = self.get_char_index(note.note)

                if self.bemol:
                    new_notes.append(self.gamme.notes_diese[ind])

                else:
                    new_notes.append(self.gamme.notes_bemol[ind])

            print("NOTES : " + str(new_notes))

            for j in range(len(old_text) - 1):
                if (old_text[j] != " " and old_text[j] != "/" and (old_text[j] == self.notes[i].notes[cpt].note or (old_text[j] + old_text[j+1]) == self.notes[i].notes[cpt].note)):

                    print("NEW NOTE")
                    new_text += new_notes[cpt]
                    cpt += 1

                    if cpt == len(new_notes):
                        new_text += " "
                        break
                else:
                    if(old_text[j] != "b" and old_text[j] != "#"):
                        new_text += old_text[j]

            print("OLD TEXT : " + old_text)
            print("NEW TEXT : " + new_text)

            new_text += "\n"

            self.all_text[line] = new_text
        self.bemol = not self.bemol

        self.reset_notes()

    def switch_notes(self, qte):

        for i, line in enumerate(self.lignes):
            #print(self.all_text[self.lignes[i]])
            #ligne de notes
            old_text = self.all_text[line]
            new_text = ""
            new_notes = []

            for note in self.notes[i].notes:
                new_notes.append(self.gamme.switch_note(note, self.bemol, qte).note)


            print("NOTESET")
            self.notes[i].show_noteset()

            print("NEW NOTESET : " + str(new_notes))

            cpt = 0


            for j in range(len(old_text) - 1):
                if old_text[j] != " " and old_text[j] != "/" and (old_text[j] == self.notes[i].notes[cpt].note or (old_text[j] + old_text[j+1]) == self.notes[i].notes[cpt].note):
                    print("NEW NOTE")
                    new_text += new_notes[cpt]
                    cpt += 1
                    if cpt == len(new_notes):
                        new_text += " "
                        break
                else:
                    if old_text[j] != "b" and old_text[j] != "#":
                        new_text += old_text[j]

            print("OLD TEXT  : " + old_text)
            print("NEW TEXT : " + new_text)

            new_text += "\n"

            self.all_text[line] = new_text

        self.reset_notes()
    
    def set_titre(self):
        for i, line in enumerate(self.all_text):
            new_line = self.all_text[i]
            #if new_line.lower().startswith(' artiste'):
            if 'artiste' in new_line.lower() and ':' in new_line.lower():
                print ("ARTISTE : " + new_line[10:])
                self.titre += new_line[10:]
                self.titre = self.titre [:-1]
                self.titre += " - "
                       
            #if new_line.lower().startswith(' titre'):
            if 'titre' in new_line.lower() and ':' in new_line.lower():    
                #new_line = self.all_text[line]
                self.titre += new_line[10:]
                self.titre = self.titre [:-1]

        print("TITRE : " + self.titre)

        if self.titre == "":
            self.titre = "Sans titre"


