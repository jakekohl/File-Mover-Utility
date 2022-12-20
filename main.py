import os
from pathlib import * 
import glob
import shutil
import PySimpleGUI as sg

# Set the window layout
layout = [[sg.Text("This is a file mover utility program. It allows you to move txt files from one location to another.")], [sg.Button("OK")]]

# First the window layout in 2 columns
file_list_column = [
    [
        sg.Text("Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]
# For now will only show the name of the file that was chosen
destination_viewer_column = [
    [sg.Text("Choose files that you want to move from the list:"),
    sg.In(size=(25, 1), enable_events=True, key="-FOLDER2-"),
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
            and f.lower().endswith((".txt"))
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
            for file in fnames:
                print(file)
                shutil.copy2(file,dest)
        except:
            pass

window.close()


'''
# Set the working directory to the Documents folder
os.chdir('/Users/jakek/Documents')
path = os.getcwd()

# Get list of all files excluding folders and print it for validation
files = (glob.glob('*.txt'))
print(f'files in {path}')
for file in files:
    print(file)


# Check to see if a directory called 'txt_files' exists. If not, creates directory
if not os.path.exists('txt_files'):
    os.mkdir('txt_files')

# copies .txt files over | does not overwrite
for file in files:
    shutil.copy2(file,'txt_files')

# Navigates into txt_files and then prints out a list of copied files for validation
os.chdir('txt_files')
path = os.getcwd()
files = (file for file in os.listdir(path)
            if os.path.isfile(os.path.join(path, file)))
print(f'files in {path}')
for file in files:
    print(file)'''