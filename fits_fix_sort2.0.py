import tkinter as tk
from tkinter import ttk
import Fix_Sort_EXECUTE
import os

input_folder = "TEST"
output_folder = "TEST"
append = "sorted"
frame_type = ["bias", "flat", "object"]

def exit_program():
    app.destroy()

def start_process():
    input_folder = inPath.get()
    if os.path.exists(input_folder):
        status.config(text="Working...", fg="chartreuse3")
        app.update()

        Fix_Sort_EXECUTE.sortType(input_folder)
        output_folder = os.path.join(input_folder, append)

        # counter to track progress
        total_files = 0
        for frame in frame_type:
            folder = os.path.join(output_folder, frame)
            total_files += sum(1 for f in os.listdir(folder) if f.lower().endswith('.fits'))

        progress["maximum"] = total_files
        progress["value"] = 0
        app.update()

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
            app.update()

        progress["value"] = total_files
        status.config(text="Done!", fg="chartreuse3")
        app.update()
    else:
        status.config(text="File does not exist :o", fg="chartreuse3", bg="darkslateblue")
        print("❌ File does not exist")
        app.update()

# GUI
app = tk.Tk()
app["bg"] = "darkslateblue"
app.title("FITS Fix-Sort")
app.geometry("490x230")

style = ttk.Style(app)
style.theme_use('default')
style.configure("Red.Horizontal.TProgressbar", troughcolor="slateblue", background="tomato")
style.configure("Yellow.Horizontal.TProgressbar", troughcolor="slateblue", background="gold")
style.configure("Green.Horizontal.TProgressbar", troughcolor="slateblue", background="chartreuse3")
style.configure("Blue.Horizontal.TProgressbar", troughcolor="slateblue", background="deepskyblue")

tk.Label(app, text="Enter Source Filepath:", fg="chartreuse3", bg="darkslateblue",
         font=["Consolas", 11, "italic"]).pack(pady=10)

inPath = tk.Entry(app, fg="black", bg="beige", width=65)
inPath.pack()

tk.Button(app, text="Fix & Sort", fg="black", bg="beige", font=["consolas", 10],
          command=start_process).pack(pady=10)


progress = ttk.Progressbar(app, orient="horizontal", length=100,
                           mode="determinate", style="Red.Horizontal.TProgressbar")
progress.place(x=380, y=200)

tk.Button(app, text="Exit", fg="black", bg="tomato",
          font=["consolas", 10], command=exit_program).pack(pady=2)

status = tk.Label(app, text="FITS Header Fixer, Sci-Image Sorter 2.0.",
                  fg="chartreuse3", bg="darkslateblue", font=["Consolas", 10])
status.pack(pady=10)

app.mainloop()
