##What to do as a user
## resolution of heightmap
## number of plots
import tkinter as tk
from tkinter.filedialog import askopenfilename

window = tk.Tk()
window.title("GPX Data Analysis")

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

def get_entry_value_resolution():
    resolution = entry.get()
    return resolution

def get_filename():
    filename = askopenfilename()
    return filename

'''
entry = tk.Entry(window)
entry.pack()

button2 = tk.Button(window, text="resolution", command=get_entry_value_resolution)
button2.pack()

button = tk.Button(window, text="Select File", command=get_filename)
button.pack()
'''
entry = tk.Entry(window)

frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)

btn_open = tk.Button(frm_buttons, text="Open", command=get_filename)

btn_save = tk.Button(frm_buttons, text="resolution", command=get_entry_value_resolution)
btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

btn_save.grid(row=1, column=0, sticky="ew", padx=5)
frm_buttons.grid(row=0, column=0, sticky="ns")

entry.grid(row=0, column=1, sticky="nsew")

window.mainloop()