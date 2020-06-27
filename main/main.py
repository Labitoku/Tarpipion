from odf import text, teletype
from odf.style import Style, TextProperties
from odf.opendocument import load, OpenDocumentText
from odf.text import Span


class Gamme:
    def __init__(self):
        self.notes = ["C", "D", "E", "F", "G", "A", "B"]
        self.notes_bemol = ["C", "Db", "D", "Eb", "E", "Fb", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
        self.notes_diese = ["C", "D", "D#", "E", "E#", "F", "F#", "G", "G#", "A", "A#", "B", "B#"]
        self.bemol = "b"
        self.diese = "#"

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

class OdtPartition:
    def __init__(self, opendocument):
        self.gamme = Gamme()

        self.partition = opendocument
        self.all_text = self.partition.getElementsByType(text.P)

        self.lignes = []
        self.notes = []
        self.cpt = 0

        self.line_identification()
        self.set_notes()

        self.bemol = self.set_bemol()

    # permet de repérer quelles lignes sont pour les notes desquelles sont pour les paroles
    def line_identification(self):
        #teletype.extractText(all_text[0])
        for i, line in enumerate(self.all_text):
            if self.noteline_identification(line):
                self.lignes.append(i)
                #print("Ligne de note à la ligne : " + str(self.lignes[self.cpt]))
                self.cpt += 1

    # permet de détecter une ligne de notes  -> determine aussi si on est en diese ou en bemol
    def noteline_identification(self, ligne):
        text = teletype.extractText(ligne)
        for i, txt in enumerate(text):
            if self.check_char_note(txt):
                if(text[i+1] == " " or text[i+1] == "#" or (text[i+1] == "b" and (text[i+2] == " " or text[i+2].lower == "m" or text[i+2] == "/"))):
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
        for i, line in enumerate(self.lignes):
            self.notes.append(NoteSet(self.all_text[line]))
            self.notes[i].show_noteset()

    def reset_notes(self):
        self.notes.clear()
        for i, line in enumerate(self.lignes):
            self.notes.append(NoteSet(self.all_text[line]))
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
            old_text = teletype.extractText(self.all_text[line])
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

            new_S = text.P()
            new_S.setAttribute("stylename", self.all_text[line].getAttribute("stylename"))
            new_S.addText(new_text)

            self.all_text[line] = new_S
            self.bemol = not self.bemol

        self.reset_notes()

    def switch_notes(self, qte):

        for i, line in enumerate(self.lignes):
            #print(self.all_text[self.lignes[i]])
            #ligne de notes
            old_text = teletype.extractText(self.all_text[line])
            newer_text = ""
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
                    newer_text += new_notes[cpt]
                    cpt += 1
                    if cpt == len(new_notes):
                        newer_text += " "
                        break
                else:
                    if old_text[j] != "b" and old_text[j] != "#":
                        newer_text += old_text[j]

            print("OLD TEXT  : " + old_text)
            print("NEW TEXT : " + newer_text)

            new_s = text.P()
            new_s.setAttribute("stylename", self.all_text[line].getAttribute("stylename"))
            new_s.addText(newer_text)
            self.all_text[line] = new_s



        self.reset_notes()

    def save_test(self):
        new_partition = OpenDocumentText()

        T5_style = Style(name="T5", family="text")
        T5_style.addElement(TextProperties(fontname="Arial"))
        new_partition.automaticstyles.addElement(T5_style)

        for i, txt in enumerate(self.all_text):
            old_text = teletype.extractText(txt)
            p = text.P(text="", stylename="T5")

            for txt_old in old_text:
                if txt_old == " " and i in self.lignes:
                    p.addElement(Span(text=' ', stylename='T5'))
                else:
                    p.addText(txt_old)

            new_partition.text.addElement(p)
        new_partition.save("x_test.odt")



class TxtPartition:
    def __init__(self, document):
        self.gamme = Gamme()

        self.partition = open(document, 'r+')
        self.partition.seek(0)

        self.all_text = []

        for line in self.partition:
            if(line.endswith("\n")):
                new_line = line
                new_line = new_line[:-2]
                self.all_text.append(new_line)

            else:
               self.all_text.append(line)

        for i, line in enumerate(self.all_text):
            if(not self.all_text[i].endswith("\n")):
                self.all_text[i] = self.all_text[i] + "\n"

        self.lignes = []
        self.cpt = 0

        self.line_identification()
        print(self.lignes)

        self.notes = []
        self.set_notes()

        self.bemol = self.set_bemol()

        #print("all text = " + self.all_text)

        #print("\n\nligne 4 : " + self.lignes[4])
        #print(self.lignes[4])


    # permet de repérer quelles lignes sont pour les notes desquelles sont pour les paroles
    def line_identification(self):
        #id_lines = self.partition.readlines()
        for i, line in enumerate(self.all_text):
            if self.noteline_identification(self.all_text[i]):
                self.lignes.append(i)
                #print("Ligne de note à la ligne : " + str(self.lignes[self.cpt]))
                self.cpt += 1
        print(self.lignes)

    # permet de détecter une ligne de notes  -> determine aussi si on est en diese ou en bemol
    def noteline_identification(self, ligne):
        text = ligne
        print("TEXT : " + text)
        for i, txt in enumerate(text):
            if self.check_char_note(txt):
                if(text[i+1] == " " or text[i+1] == "#" or (text[i+1] == "b" and (text[i+2] == " " or text[i+2].lower == "m" or text[i+2] == "/"))):
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

            #new_S = text.P()
            #new_S.setAttribute("stylename", self.all_text[line].getAttribute("stylename"))
            #new_S.addText(new_text)

            self.all_text[line] = new_text
            self.bemol = not self.bemol

        self.reset_notes()

    def switch_notes(self, qte):

        for i, line in enumerate(self.lignes):
            #print(self.all_text[self.lignes[i]])
            #ligne de notes
            old_text = teletype.extractText(self.all_text[line])
            newer_text = ""
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
                    newer_text += new_notes[cpt]
                    cpt += 1
                    if cpt == len(new_notes):
                        newer_text += " "
                        break
                else:
                    if old_text[j] != "b" and old_text[j] != "#":
                        newer_text += old_text[j]

            print("OLD TEXT  : " + old_text)
            print("NEW TEXT : " + newer_text)

            new_s = text.P()
            new_s.setAttribute("stylename", self.all_text[line].getAttribute("stylename"))
            new_s.addText(newer_text)
            self.all_text[line] = new_s

#        print("\n\n\n")
 #       for i in range(len(self.all_text)):
  #          print(self.all_text[i])

        self.reset_notes()

    def save_test(self):
        
        new_partition = open("x_test.txt","w+")

        for i, txt in enumerate(self.all_text):
            new_partition.write(txt)
            new_partition.write("\n")
            
            """old_text = teletype.extractText(txt)
            p = text.P(text="", stylename="T5")

            for txt_old in old_text:
                if txt_old == " " and i in self.lignes:
                    p.addElement(Span(text=' ', stylename='T5'))
                else:
                    p.addText(txt_old)

            new_partition.text.addElement(p)"""

        #new_partition.save("x_test.odt")












if __name__ == '__main__':

    txt_partition = TxtPartition("test/e_TxtTest.txt")
    txt_partition.switch_type()

    print("\n\n\n\n\n\n")
    print(txt_partition.all_text)
    print("\n\n\n\n\n\n")

    txt_partition.save_test()

"""    gamme = Gamme()
    testdoc = load("test/d_TranspoTest.odt")
    odt_partition = OdtPartition(testdoc)
    odt_partition.switch_notes(3)

    odt_partition.switch_type()

    print("\n\n\n")
    for i in range(len(odt_partition.all_text)):
        print(odt_partition.all_text[i])

    odt_partition.switch_type()
    odt_partition.save_test()
"""
