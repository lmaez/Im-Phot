# Louis Maez
# Amber Benites
# Lowell Observatory
# 08/25/2025

import tkinter as tk
from tkinter import ttk
import subprocess
import sys
#import create_Master_Bias
import os

def exit_program():
    app.destroy()

def bias_Input():
    #Bias Input
    if biasVar.get() == 1:
        biasLabel.configure(text="Bias Directory:")
        app.update()
    else:
        biasLabel.configure(text="Master Bias:")
        app.update()

def flat_Input():
    #Bias Input
    if flatVar.get() == 1:
        flatLabel.configure(text="Flat Directory:")
        app.update()
    else:
        flatLabel.configure(text="Master Flat:")
        app.update()

def run_Sort():
    subprocess.Popen([sys.executable, "fits_fix_sort3.py"])

def run_Compare():
    subprocess.Popen([sys.executable, "GUI_FITS_Compare.py"])

# GUI
app = tk.Tk()
app["bg"] = "Black"
app.title("Lowell Im-Phot")
app.geometry("600x600")

style = ttk.Style(app)
style.theme_use('default')

#Title
tk.Label(app, text="Image Reduction", fg="Green2", bg="Black",
         font=["Consolas", 11]).pack(pady=10)

#Bias Checkbox
biasVar = tk.BooleanVar()
biasVar.set(1)
biasCheck = tk.Checkbutton(app, text="Build", command=bias_Input,
                           variable=biasVar, bg="DarkSlateGray", fg="Black")
biasCheck.place(x=500,y=40)
#Bias Input
biasLabel = tk.Label(app,  text="Bias Directory:", fg="Green2", bg="Black",
     font=["Consolas", 10])
biasLabel.place(x=10, y=40)
biasPath = tk.Entry(app, fg="black", bg="beige", width=60)
biasPath.place(x=130, y=42)

#Combine Option Dropbox
stackMethod = tk.Label(app,  text="Stack Method", fg="Green2", bg="Black",
         font=["Consolas", 10])
stackMethod.place(x=30, y=150)
combOptions = ["Average Only", "3 Sigma Clip", "5 Sigma Clip"]
dropdown = ttk.Combobox(app, values=combOptions)
dropdown.config(state="readonly")
selected_option = dropdown.get()
dropdown.set(combOptions[0])
dropdown.place(x=10, y=175)

#Flat Checkbox
flatVar = tk.BooleanVar()
flatVar.set(1)
flatCheck = tk.Checkbutton(app, text="Build", command=flat_Input,
                           variable=flatVar, bg="DarkSlateGray", fg="Black")
flatCheck.place(x=500,y=70)
#Flat Input
flatLabel = tk.Label(app,  text="Flat Directory:", fg="Green2", bg="Black",
         font=["Consolas", 10])
flatLabel.place(x=10, y=70)
flatPath = tk.Entry(app, fg="black", bg="beige", width=60)
flatPath.place(x=130, y=72)

#Image Input
imageLabel = tk.Label(app,  text="Image Directory:", fg="Green2", bg="Black",
         font=["Consolas", 10])
imageLabel.place(x=10, y=100)
imageLabel = tk.Entry(app, fg="black", bg="beige", width=60)
imageLabel.place(x=130, y=102)

#Sorting App Button
sortButton = tk.Button(app, text="Sort Images", fg="black", bg="beige", font=["consolas", 8],
          command=run_Sort)
sortButton.place(x=500, y=175)

#Comparing App Button
compareButton = tk.Button(app, text="Compare Images", fg="black", bg="beige", font=["consolas", 8],
          command=run_Compare)
#compareButton.place(x=500, y=205)

#Start Button
startButton = tk.Button(app, text="Start", fg="black", bg="beige", font=["consolas", 8],
          command=exit_program)
startButton.place(x=405, y=569)

#Exit Button
exitButton = tk.Button(app, text="Exit", fg="black", bg="tomato",
          font=["consolas", 8], command=exit_program)
exitButton.place(x=450, y=569)

#Progress bar
progress = ttk.Progressbar(app, orient="horizontal", length=100,
                           mode="determinate", style="Green.Horizontal.TProgressbar")
style.configure("Green.Horizontal.TProgressbar", troughcolor="darkslateGray", background="Green2")
progress.place(x=490, y=570)

#Status Label
statusText = tk.Label(app, text="Status: Waiting",
                  fg="Green2", bg="Black", font=["Consolas", 10])
statusText.place(x=10, y=570)

app.mainloop()

