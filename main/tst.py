from odf import text, teletype
from odf.opendocument import load

"""#charger et afficher un texte
testdoc = load("test/a_textTest.odt")
print(testdoc.text)
"""

"""#detecter les differentes lignes
"""
testdoc = load("test/b_DetectionLigne.odt")
allparas = testdoc.getElementsByType(text.P)
#teletype.extractText(allparas[0])

for i in range(len(allparas)):
    print(str(i) + "          " + str(allparas[i]))

