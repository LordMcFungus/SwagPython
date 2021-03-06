import os
import threading
from filecmp import cmp
from shutil import copy2
from tkinter import *
from tkinter.filedialog import askdirectory


SourceFolder = ""
TargetFolder = ""
SourceFiles = []
TargetFiles = []

window = Tk()

#window Size
window.geometry("900x150")

#guilabels erstellen
Label(window, text="Source Folder").grid(row=0)
Label(window, text="Target Folder").grid(row=1)

e1 = Entry(window, width=100)
e2 = Entry(window, width =100)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

#Zielordner Wählen
def chooseTargetFolder():
    TargetDirectoryEntry = askdirectory(title="Target Folder", mustexist=True)
    e2.insert(10, TargetDirectoryEntry)

#Sourceordner Wählen
def chooseSourceFolder():
    SourceDirectoryEntry = askdirectory(title="Source Folder", mustexist=True)
    e1.insert(10, SourceDirectoryEntry)


def show_entry_fields():
   print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))

#Dateien in Sourceordner suchen und mit Zielordner Synchronisieren
def iterateThroughFolder():
    threading.Timer(60.0, iterateThroughFolder).start()
    TargetFiles.clear()
    SourceFiles.clear()

    SourceFolder = e1.get()
    TargetFolder = e2.get()
    #Dateien in Sourcfolder in Array speichern
    for subdir, dirs, files in os.walk(SourceFolder):
        for file in files:
            full_path = os.path.join(subdir, file)
            relative_path = os.path.relpath(full_path, SourceFolder)
            print(full_path)
            print(relative_path)
            SourceFiles.append(relative_path)

    #Dateien in Targetfolder in Array Speichern
    for subdir, dirs, files in os.walk(TargetFolder):
        for file in files:
            full_path = os.path.join(subdir, file)
            relative_path = os.path.relpath(full_path, TargetFolder)
            print(full_path)
            print(relative_path)
            TargetFiles.append(relative_path)

    for file in SourceFiles:
        #ist datei nicht vorhanden ->Kopieren
        if not file in TargetFiles:
            full_target_path = os.path.join(TargetFolder, file)
            full_source_path = os.path.join(SourceFolder, file)
            if not os.path.exists(os.path.dirname(full_target_path)):
                os.makedirs((os.path.dirname(full_target_path)))
            copy2(full_source_path, full_target_path)
        #Wurde Datei verändert -> Kopieren
        else :
            full_path_targetfile = os.path.join(TargetFolder, file)
            full_path_sourcefile = os.path.join(SourceFolder, file)
            if not cmp(full_path_sourcefile, full_path_targetfile):
               copy2(full_path_sourcefile, full_path_targetfile)

    for target_file in TargetFiles:
        if not target_file in SourceFiles:
            full_path_target = os.path.join(TargetFolder, target_file)
            os.remove(full_path_target)




Button(window, text='Choose Source Folder', command=chooseSourceFolder).grid(row=0, column=2, sticky=W, pady=4)
Button(window, text='Choose Target Folder', command=chooseTargetFolder).grid(row=1, column=2, sticky=W, pady=4)
Button(window, text='Quit', command=window.quit).grid(row=3, column=0, sticky=W, pady=4)
Button(window, text='Show', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)
Button(window, text='SYNC', command=iterateThroughFolder).grid(row=3, column=3, sticky=W, pady=4)

window.mainloop()