# Louis Maez
# Amber Benites
# Lowell Observatory
# 08/25/2025

import tkinter as tk
from tkinter import ttk
import Fix_Sort_EXECUTE
import os

input_folder = "TEST"
output_folder = "TEST"
append = "sorted"
frame_type = ["bias", "flat", "object"]

def exit_program():
    sort.destroy()

def start_process():
    input_folder = inPath.get()
    if os.path.exists(input_folder):
        status.config(text="Working...", fg="Green2")
        sort.update()

        Fix_Sort_EXECUTE.sortType(input_folder)
        output_folder = os.path.join(input_folder, append)

        # counter to track progress
        total_files = 0
        for frame in frame_type:
            folder = os.path.join(output_folder, frame)
            total_files += sum(1 for f in os.listdir(folder) if f.lower().endswith('.fits'))

        progress["maximum"] = total_files
        progress["value"] = 0
        sort.update()

        processed = 0
        for frame in frame_type:
            frame_path = os.path.join(output_folder, frame)

            # count FITS before processing
            fits_files = [f for f in os.listdir(frame_path) if f.lower().endswith('.fits')]
            Fix_Sort_EXECUTE.sortTrimFix(frame_path)
            processed += len(fits_files)
            progress["value"] = processed

            # update progress color(buggy)
            percent = (processed / total_files) * 100
            if percent < 25:
                progress.config(style="Red.Horizontal.TProgressbar")
            elif percent < 50:
                progress.config(style="Yellow.Horizontal.TProgressbar")
            elif percent < 75:
                progress.config(style="Blue.Horizontal.TProgressbar")
            else:
                progress.config(style="Green.Horizontal.TProgressbar")
            sort.update()

        progress["value"] = total_files
        status.config(text="Done!", fg="Green2")
        sort.update()
    else:
        status.config(text="File does not exist :o", fg="Green2", bg="black")
        print("❌ File does not exist")
        sort.update()

# GUI
sort = tk.Tk()
sort["bg"] = "Black"
sort.title("FITS Fix-Sort")
sort.geometry("490x130")

style = ttk.Style(sort)
style.theme_use('default')
style.configure("Red.Horizontal.TProgressbar", troughcolor="DarkSlateGray", background="tomato")
style.configure("Yellow.Horizontal.TProgressbar", troughcolor="DarkSlateGray", background="gold")
style.configure("Green.Horizontal.TProgressbar", troughcolor="DarkSlateGray", background="chartreuse3")
style.configure("Blue.Horizontal.TProgressbar", troughcolor="DarkSlateGray", background="deepskyblue")

tk.Label(sort, text="Enter Source Filepath:", fg="Green2", bg="black",
         font=["Consolas", 11, "italic"]).pack(pady=10)

inPath = tk.Entry(sort, fg="black", bg="beige", width=65)
inPath.pack()

tk.Button(sort, text="Fix & Sort", fg="black", bg="beige", font=["consolas", 8],
          command=start_process).place(x=260, y=95)


progress = ttk.Progressbar(sort, orient="horizontal", length=100,
                           mode="determinate", style="Red.Horizontal.TProgressbar")
progress.place(x=375, y=96)

tk.Button(sort, text="Exit", fg="black", bg="tomato",
          font=["consolas", 8], command=exit_program).place(x=335, y=95)

status = tk.Label(sort, text="FITS Header Fixer, Sci-Image Sorter 3.0.",
                  fg="Green2", bg="black", font=["Consolas", 8])
status.place(x=5, y=100)

sort.mainloop()
