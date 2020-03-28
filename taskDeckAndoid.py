import kivy
import sqlite3
import json
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
index = 0

#Builder.load_file('style.kv')

class MyGrid(Widget):
    pass
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)

        self.addButton.bind(on_press=self.add)
        self.buttonDid.bind(on_press=self.didIt)
        self.buttonLater.bind(on_press=self.doItLater)

        self.aboutBt.bind(on_press=self.about)
        self.showAllBt.bind(on_press=self.showAll)

        configFile = open("config.json", "r")
        config = json.load(configFile)

        self.addButton.text = config.get("addButton", "+")
        self.buttonDid.text = config.get("doneButton", "DONE")
        self.buttonLater.text = config.get("laterButton", "LATER")
        self.showAllBt.text = config.get("showAllButton", "SHOW ALL")
        self.aboutBt.text = config.get("aboutButton", "ABOUT")
        self.settingsBt.text = config.get("settingsButton", "SETTINGS")

        self.findNew(self)


    def about(self, obj):
        global index
        self.noteLabel.text = "By: Marek Maskarinec \n version: 0.1"
        index = 0

    def showAll(self, obj):
        global index
        conn = sqlite3.connect('cards.db')
        c = conn.cursor()
        c.execute("SELECT * FROM cards")
        cards = c.fetchall()
        print(cards)
        if cards is not []:
            for i in range(len(cards)):
                self.noteLabel.text += cards[i][0] + "\n" + str(cards[i][1]) + "\n" + "--------" + "\n"
        else:
            self.noteLabel.text = "No notes"
        conn.close()
        index = 0

    def add(self, obj):
        global index
        noteText = self.addTextBox.text
        priority = int(self.priorityBox.text )
        print(priority)
        print(noteText)
        conn = sqlite3.connect('cards.db')
        c = conn.cursor()
        #c.execute("""CREATE TABLE cards
        #            (note text, priority number)""")
        c.execute("INSERT INTO cards VALUES (?, ?)", (noteText, priority))
        c.execute("SELECT * FROM cards ORDER BY priority DESC")
        conn.commit()
        conn.close()
        index = 0
        #nowEditing = nowEditing - 1

    def didIt(self, obj):
        global index
        global priorToSearch
        conn = sqlite3.connect('cards.db')
        c = conn.cursor()
        c.execute("SELECT * FROM cards")
        cards = c.fetchall()
        if len(cards) > 0 and index < len(cards):
            c.execute('DELETE FROM cards WHERE note=?', (cards[index][0],))
        conn.commit()
        conn.close()
        if len(cards) > 0:
            self.findNew(obj)
        #index += 1

    def doItLater(self, obj):
        global index
        self.findNew(obj)
        index += 1

    def findNew(self, obj):
        global index
        print(index)
        conn = sqlite3.connect('cards.db')
        c = conn.cursor()
        c.execute("SELECT * FROM cards ORDER BY priority DESC")
        #c.execute("SELECT * FROM cards")
        cards = c.fetchall()
        print(cards)
        conn.close()
        if index >= len(cards):
            index = 0

        if len(cards) > 0:
            self.noteLabel.text = cards[index][0]
        else:
            self.noteLabel.text = "no notes"
        """global priorToSearch
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
                        #seenNotes = list()
            else:
                print(seenNotes)
                print(lastId)
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
        priorToSearch = priorToSearch -1"""


class Window(App):

    def build(self):
        return MyGrid()

window = Window()

window.run()
