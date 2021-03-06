
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
