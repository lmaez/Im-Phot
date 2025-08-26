# Louis Maez
# Amber Benites
# Lowell Observatory
# 08/25/2025
#
# App for statistical comparison between two similiar
# FITS Images. Compares IRAF reductions and Astropy Reductions

#! Does not print to CMD line when run from Im-Phot GUI????

import tkinter as tk
from tkinter import ttk
import Compare_FITS_Images
import subprocess
import sys
import os

inPath1 = r"C:\Users\louis\Desktop\20250626\sorted\object\AP_Lib\B\20250626.0195.fits"
inPath2 = r"C:\Users\louis\Desktop\20250626\sorted\object\AP_Lib\B\20250626.0196.fits"

def start_Compare():
    image1 = inPath1.get()
    image2 = inPath2.get()
    if os.path.exists(image1) and os.path.exists(image2):
        compStatus.configure(text="Status: Working. Check CMD Line")
        comp.update()
        Compare_FITS_Images.statistical_Compare(image1, image2)
        #subprocess.Popen([sys.executable,
        #                  Compare_FITS_Images.statistical_Compare(image1, image2)])
    else:
        print("Status: File(s) Not Found")
        compStatus.configure(text="Status: File(s) not found")

comp = tk.Tk()
comp["bg"] = "Black"
comp.title("FITS Compare")
comp.geometry("490x130")

tk.Label(comp, text="Enter Two File Paths:", fg="Green2", bg="black",
         font=["Consolas", 11, "italic"]).pack(pady=5)

inPath1 = tk.Entry(comp, fg="black", bg="beige", width=65)
inPath1.pack(pady=5)

inPath2 = tk.Entry(comp, fg="black", bg="beige", width=65)
inPath2.pack(pady=5)

tk.Button(comp, text="Compare", fg="black", bg="beige", font=["consolas", 8],
          command=start_Compare).place(x=392, y=98)

compStatus = tk.Label(comp, text="Status: Waiting",
                  fg="Green2", bg="black", font=["Consolas", 8])
compStatus.place(x=5, y=105)

comp.mainloop()


