import kivy
import sqlite3
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
#from.kivy.properties import ObjectProperty


readedNote = None
priorToSearch=10
nowEditing=10
seenNotes = list()
lastId = 0

#Builder.load_file('style.kv')

class MyGrid(Widget):
    pass
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)


        """
        #add layer
        self.addTextBox = TextInput(multiline= False)
        self.addTextBox.size_hint_y = None
        self.addTextBox.height = 40
        self.add_widget(self.addTextBox)
        self.priorityBox = Spinner(text="10", values=("10","9","8","7","6","5","4","3","2","1"))
        self.priorityBox.size_hint_y = None
        self.priorityBox.height = 40
        self.add_widget(self.priorityBox)
        self.addButton = Button(text="+")
        self.addButton.size_hint_y = None
        self.addButton.height = 40
        self.addButton.bind(on_press=self.add)
        self.add_widget(self.addButton)

        #read layer
        self.buttonDid = Button(text="DID IT")
        self.buttonDid.bind(on_press=self.didIt)
        self.add_widget(self.buttonDid)
        self.noteLabel = Label(text="Note")
        self.add_widget(self.noteLabel)
        self.buttonLater = Button(text="DO IT LATER")
        self.buttonLater.bind(on_press=self.doItLater)
        self.add_widget(self.buttonLater)
        """

        self.addButton.bind(on_press=self.add)
        self.buttonDid.bind(on_press=self.didIt)
        self.buttonLater.bind(on_press=self.doItLater)

    def add(self, obj):
        noteText = self.addTextBox.text
        priority = int(self.priorityBox.text )
        print(priority)
        print(noteText)
        conn = sqlite3.connect('cards.db')
        c = conn.cursor()
        #c.execute("""CREATE TABLE cards
        #            (note text, priority number)""")
        c.execute("INSERT INTO cards VALUES (?, ?)", (noteText, priority))
        conn.commit()
        conn.close()
        #nowEditing = nowEditing - 1

    def didIt(self, obj):
        global priorToSearch
        conn = sqlite3.connect('cards.db')
        c = conn.cursor()
        c.execute('DELETE FROM cards WHERE priority=?', (priorToSearch + 1,))
        conn.commit()
        conn.close()
        self.findNew(obj)

    def doItLater(self, obj):
        self.findNew(obj)

    def findNew(self, obj):
        global priorToSearch
        global seenNotes
        global lastId
        cycleNumber = 0
        while True:
            conn = sqlite3.connect('cards.db')
            c = conn.cursor()
            c.execute("SELECT * FROM cards WHERE priority=?", (priorToSearch,))
            recordRow = c.fetchone()
            if recordRow is not None:    
                c.execute("SELECT rowid, * FROM cards WHERE note=?", (recordRow[0],))
                lastId = c.fetchone
            else:
                self.noteLabel.text = "Create note first"

            if recordRow is None:
                self.noteLabel.text = ""
                priorToSearch = priorToSearch - 1
                if priorToSearch < 1:
                    if cycleNumber == 1:
                        break
                    else:
                        priorToSearch = 10
                        cycleNumber = cycleNumber + 1
                        seenNotes = list()
            else:
                if lastId not in seenNotes:
                    print(recordRow)
                    self.noteLabel.text = recordRow[0]
                    #priorityLabel.config(text=recordRow[1])
                    seenNotes.append(lastId)
                    break
                else:
                    priorToSearch = priorToSearch - 1

        conn.commit()
        conn.close()
        priorToSearch = priorToSearch -1


class Window(App):

    def build(self):
        return MyGrid()

window = Window()

window.run()