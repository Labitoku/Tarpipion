# coding: utf8 
from PyQt5.QtWidgets import *
import class_set
import subprocess
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 

class IconButton():

    def __init__(self, icon, parent, size_x, size_y, icon_size_x, icon_size_y, tooltip = ""):

        self.button = QPushButton("", parent)
        self.button.resize(size_x, size_y)
        
        
        self.button.maximumWidth = size_x
        self.button.maximumHeight = size_y

        self.button.setIconSize(QSize(icon_size_x, icon_size_y))
        self.button.setIcon(icon)

        self.button.setToolTip(tooltip)

        self.button.setStyleSheet("QPushButton { background-color: rgba(45, 45, 45, 255) ; border-style: outset; border-width: 0px; border-radius: 0px; border-color: rgba(0,0,0,0); }" 
                                  "QPushButton::pressed { background-color: red }" 
                                  "QPushButton::hover{background-color : rgba(15, 15, 15, 255)}")

    def empty_button(parent, size_x, size_y, icon_size_x, icon_size_y):
        button = QPushButton("", parent)
        button.resize(size_x, size_y)
        
        button.maximumWidth = size_x
        button.maximumHeight = size_y
    
        button.setIconSize(QSize(icon_size_x, icon_size_y))
        button.setIcon(QIcon("assets/empty.png"))

        button.setStyleSheet("QPushButton { background-color: rgba(0, 0, 0, 0) ; border-style: outset; border-width: 0px; border-radius: 0px; border-color: rgba(0,0,0,0); }")

        return button

    

class MainWindow(QMainWindow): 
  
    def __init__(self): 
        super().__init__()
        
        self.setStyleSheet("background-color: rgba(75,75,75,255);") 

        self.diese = True

        QtGui.QFontDatabase.addApplicationFont("asset/font/Lato Light Italic.ttf")

        self.setWindowTitle("Tarpipion") 
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.setGeometry(0, 0, 1280, 720) 

        self.dimensions = QDesktopWidget().screenGeometry()
        
        self.square_size = int(self.dimensions.height() / 13.5)

        self.menu_layout = QVBoxLayout()
        self.menu_layout.setGeometry(QRect(0, 0, self.dimensions.width(), self.dimensions.height()))

        
################################################################################################################################################################################################################
        #LAYOUT ARRONDI#
################################################################################################################################################################################################################

        self.partition_layout = QHBoxLayout()
        self.panel_width = int(self.dimensions.width() / 3.2)
        
        self.frame_left = QFrame(self)
        self.frame_left.setFrameShape(QFrame.Box)
        self.frame_left.resize(self.panel_width, self.square_size * 2)
        self.frame_left.setStyleSheet("QFrame { background-color: rgba(0, 0, 0, 0) ; border-style: outset; border-width: 0px; border-radius: 0px; border-color: rgba(0,0,0,0); }")

        self.frame_right = QFrame(self)
        self.frame_right.setFrameShape(QFrame.Box)
        self.frame_right.resize(self.panel_width, self.square_size * 2)
        self.frame_right.setStyleSheet("QFrame { background-color: rgba(0, 0, 0, 0) ; border-style: outset; border-width: 0px; border-radius: 0px; border-color: rgba(0,0,0,0); }")

        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.Box)
        self.frame.resize(self.panel_width, self.square_size * 2)
        self.frame.setStyleSheet("QFrame { background-color: rgba(45, 45, 45, 255) ; border-style: outset; border-width: 0px; border-radius: 75px; border-color: rgba(0,0,0,0); }")

        self.partition_layout.addWidget(self.frame_left, 1)
        self.partition_layout.addWidget(self.frame, 1)
        self.partition_layout.addWidget(self.frame_right, 1)

        self.partition_layout.setGeometry(QRect(0,0, self.dimensions.width(), self.square_size * 2))
        

################################################################################################################################################################################################################
        #LAYOUT DE BOUTONS DE PARTITION#
################################################################################################################################################################################################################

        self.partition_menu_layout = QHBoxLayout()
        self.panel_width = int(self.dimensions.width() / 3.2)
        
        self.frame_left = QFrame(self)
        self.frame_left.setFrameShape(QFrame.Box)
        self.frame_left.resize(self.panel_width, self.square_size * 2)
        self.frame_left.setStyleSheet("QFrame { background-color: rgba(0, 0, 0, 0) ; border-style: outset; border-width: 0px; border-radius: 0px; border-color: rgba(0,0,0,0); }")

        self.frame_right = QFrame(self)
        self.frame_right.setFrameShape(QFrame.Box)
        self.frame_right.resize(self.panel_width, self.square_size * 2)
        self.frame_right.setStyleSheet("QFrame { background-color: rgba(0, 0, 0, 0) ; border-style: outset; border-width: 0px; border-radius: 0px; border-color: rgba(0,0,0,0); }")

        self.diese_icon = QIcon("assets/diese_mieux.png")
        self.bemol_icon = QIcon("assets/bemol_mieux.png")

        #BOUTON TYPE - DEMOL / DIESE
        self.type_button = IconButton(self.diese_icon, self, self.square_size, self.square_size*2, self.square_size, self.square_size*2, "New File")
        self.type_button.button.setCheckable(True)
        self.type_button.button.clicked.connect(self.switch_type)

        #SEPARATION
        self.button_spacer = IconButton.empty_button(self, self.square_size, self.square_size*2, self.square_size, self.square_size*2)

        #BOUTON REDUCTION
        minus = QIcon("assets/minus_mieux.png")
        self.minus_button = IconButton(minus, self, self.square_size, self.square_size*2, self.square_size, self.square_size*2, "New File")
        self.minus_button.button.setCheckable(True)
        self.minus_button.button.clicked.connect(self.down_switch_note)

        #LABEL DEMI TON
        self.demi_ton = QLabel(self)
        pixmap = QPixmap("assets/demi_ton_mieux.png")
        small_pixmap = pixmap.scaled(self.square_size * 2, self.square_size * 2, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.demi_ton.setPixmap(small_pixmap)
        self.demi_ton.show()
        self.demi_ton.setStyleSheet("background-color: rgba(45,45,45,255);") 

        #BOUTON AUGMENTATION
        plus = QIcon("assets/plus_mieux.png")
        self.plus_button = IconButton(plus, self, self.square_size, self.square_size*2, self.square_size, self.square_size*2, "New File")
        self.plus_button.button.setCheckable(True)
        self.plus_button.button.clicked.connect(self.up_switch_note)


        self.partition_menu_layout.addWidget(self.frame_left, 1)
        self.partition_menu_layout.addWidget(self.type_button.button, 0)
        self.partition_menu_layout.addWidget(self.button_spacer, 0)
        self.partition_menu_layout.addWidget(self.minus_button.button, 0)
        self.partition_menu_layout.addWidget(self.demi_ton, 0)
        self.partition_menu_layout.addWidget(self.plus_button.button, 0)

        self.partition_menu_layout.addWidget(self.frame_right, 1)

        self.partition_menu_layout.setGeometry(QRect(0,0, self.dimensions.width(), self.square_size * 2))

################################################################################################################################################################################################################
        #LAYOUT D'ACCUEIL#
################################################################################################################################################################################################################
        
        self.button_layout = QHBoxLayout()

        new_icon = QIcon("assets/new_mieux.png")
        self.new_button = IconButton(new_icon, self, self.square_size, self.square_size, self.square_size, self.square_size, "New File")

        open_icon = QIcon("assets/open_mieux.png")
        self.open_button = IconButton(open_icon, self, self.square_size, self.square_size, self.square_size, self.square_size, "Open File")
        self.open_button.button.setCheckable(True)
        self.open_button.button.clicked.connect(self.open_file)

        save_icon = QIcon("assets/save_mieux.png")
        self.save_button = IconButton(save_icon, self, self.square_size, self.square_size, self.square_size, self.square_size, "Save File")

        self.button_layout.addWidget(self.new_button.button,0)
        self.button_layout.addWidget(self.open_button.button,0)
        self.button_layout.addWidget(self.save_button.button,0)

        self.label = QLabel(self)
        self.label.setText("Aucune partition")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("QLabel { color : rgba(230, 230, 230, 255) ;  background-color : rgba(45, 45, 45, 255) ; font-family : Lato ; font-style : italic ;  font-size : 48px }")

        self.button_layout.addWidget(self.label,1)

        self.button_layout.setSpacing(0)
        self.button_layout.setGeometry(QRect(0,0, self.dimensions.width(), self.square_size))
        

################################################################################################################################################################################################################
        #LAYOUT DE PARTITIONS#
################################################################################################################################################################################################################

        self.partition_text_layout = QHBoxLayout()

        self.partition_originale = QScrollArea(self)
        self.partition_originale.setViewportMargins(QMargins(int(self.square_size / 6), int(self.square_size / 6), int(self.square_size / 6), int(self.square_size / 6)))
        self.partition_originale.setStyleSheet("QScrollArea {background-color: rgba(230,230,230,255);}")

        self.partition_modifiee = QScrollArea(self)
        self.partition_modifiee.setViewportMargins(QMargins(int(self.square_size / 6), int(self.square_size / 6), int(self.square_size / 6), int(self.square_size / 6)))
        self.partition_modifiee.setStyleSheet("QScrollArea {background-color: rgba(230,230,230,255);}")


        self.text_size = 14

        self.partition_text_layout.addWidget(self.partition_originale, 0)
        self.partition_text_layout.addWidget(self.partition_modifiee, 0)
        self.partition_text_layout.setSpacing(self.square_size)
        self.partition_text_layout.setGeometry(QRect(int(self.dimensions.width() * .175), int(self.dimensions.height() * .166667), int(self.dimensions.width() * .65), int(self.dimensions.height() * .75)))

        self.showMaximized()


    def open_file(self, pressed):

        try:
            label_b = QLabel("")
            self.partition_modifiee.setWidget(label_b)

            name = QFileDialog.getOpenFileName(self, 'Open File', 'C\\', 'Text files (*.txt)')
            path = name[0]
            self.partition = class_set.TxtPartition(path)
            
            label_a = QLabel()
            #label_b = QLabel()

            self.partition_originale.setWidget(label_a)
            #self.partition_modifiee.setWidget(label_b)

            with open(path, "r", encoding="utf-8") as f:


                text = ""
                for t in self.partition.all_text:
                        text += t

                partition_originale_text = QLabel()
                partition_originale_text.setText(text)
                partition_originale_text.setStyleSheet("QLabel { color : rgba(75, 75, 75, 255) ;  background-color : rgba(0, 0, 0, 0) ; font-family : Lato ;  font-size : "+str(self.text_size)+"px }")


                #partition_modifiee_text = QLabel()
                #partition_modifiee_text.setText(text)
                #partition_modifiee_text.setStyleSheet("QLabel { color : rgba(75, 75, 75, 255) ;  background-color : rgba(0, 0, 0, 0) ; font-family : Lato ;  font-size : "+str(self.text_size)+"px }")


                self.partition_originale.setWidget(partition_originale_text)
                #self.partition_modifiee.setWidget(partition_modifiee_text)

                self.unfade(self.partition_originale.findChild(QLabel))
                #self.unfade(self.partition_modifiee.findChild(QLabel))

                self.set_titre(self.partition.titre)

                print(self.partition.notes[0])

        except FileNotFoundError:
            pass

    def switch_type(self, pressed):
        try:
            if self.partition:
                source = self.sender()

                if(self.diese):
                    source.setIcon(self.bemol_icon)
                else:
                    source.setIcon(self.diese_icon)

                self.partition.switch_type()
                partition_new = QLabel()
                text = ""
                for t in self.partition.all_text:
                    text += t
                partition_new.setText(text)
                partition_new.setStyleSheet("QLabel { color : rgba(75, 75, 75, 255) ;  background-color : rgba(0, 0, 0, 0) ; font-family : Lato ;  font-size : "+str(self.text_size)+"px }")
                
                self.partition_modifiee.setWidget(partition_new)
                self.unfade(self.partition_modifiee.findChild(QLabel))

                self.diese = not self.diese

        except AttributeError:
            pass


    def up_switch_note(self, pressed):
        try:
            if self.partition:
                self.partition.switch_notes(1)
                partition_new = QLabel()
                text = ""
                for t in self.partition.all_text:
                    text += t
                partition_new.setText(text)
                partition_new.setStyleSheet("QLabel { color : rgba(75, 75, 75, 255) ;  background-color : rgba(0, 0, 0, 0) ; font-family : Lato ;  font-size : "+str(self.text_size)+"px }")
            
                self.partition_modifiee.setWidget(partition_new)

                self.unfade(self.partition_modifiee.findChild(QLabel))
        except AttributeError:
            pass

    def down_switch_note(self, pressed):
        try:
            if self.partition:
                self.partition.switch_notes(-1)
                partition_new = QLabel()
                text = ""
                for t in self.partition.all_text:
                    text += t
                print("TEXT IN CODE 2 : " + text)
                partition_new.setText(text)
                partition_new.setStyleSheet("QLabel { color : rgba(75, 75, 75, 255) ;  background-color : rgba(0, 0, 0, 0) ; font-family : Lato ;  font-size : "+str(self.text_size)+"px }")
                
                self.partition_modifiee.setWidget(partition_new)

                self.unfade(self.partition_modifiee.findChild(QLabel))

        except AttributeError:
            pass


    def set_titre(self, titre):
        cpt = 0
        new_titre = ""

        for i in titre:
            cpt += 1
            new_titre = new_titre + i
            if cpt >= 75:
                new_titre = new_titre + "..."
                break

        self.label.setText(new_titre)
    
    def fade(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def unfade(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()




# create pyqt5 app 
App = QApplication(sys.argv) 

# create the instance of our Window 
window = MainWindow() 
  
# start the app 
sys.exit(App.exec_()) 