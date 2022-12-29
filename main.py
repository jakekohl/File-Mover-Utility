import os
from pathlib import * 
import glob
import shutil
import PySimpleGUI as sg


# Theme/Color
sg.theme('LightPurple')
# First the window layout in 2 columns
file_list_column = [
    [
        sg.Text("Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 10), key="-FILE LIST-"
        )
    ],
]
# For now will only show the name of the file that was chosen
destination_viewer_column = [
    [sg.Text("Files on the left will be moved to the following directory:")],
    [sg.In(size=(25, 1), enable_events=True, key="-FOLDER2-"),
        sg.FolderBrowse()
    ],
    [sg.Button("COPY", enable_events=True,key='-COPY-'), sg.Cancel(),
    ]
]
# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(destination_viewer_column),
    ]
]

window = sg.Window("File Mover Utilty", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
                #and f.lower().endswith((".txt"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-FOLDER-"].update(filename=filename)
        except:
            pass
    if event == "-FOLDER2-":
        dest = values["-FOLDER2-"]
    elif event == "-COPY-":  # Press the COPY button to copy files over
        try:
            # copies .txt files over | does not overwrite
            src, dest = values['-FOLDER-'],values['-FOLDER2-']
            print(f'I am copying txt files from {src} to {dest}')
            print(fnames)
            for file in fnames:
                fullpath = os.path.join(src,file)
                print(fullpath)
                shutil.copy2(fullpath,dest) 
            os.chdir(dest)
            currentdir = os.getcwd()
            print(f'I am printing out files from {currentdir}')
            print(os.listdir())
        except IOError as e:
            print(e)
        except shutil.SameFileError:
            print("Source and destination represents the same file.")
        except PermissionError:
            print("Permission denied.")
        except:
            print('I have no idea what happened')

window.close()
