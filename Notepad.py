import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3

class Notepad(tk.Tk):
    def __init__(self):
        super().__init__()
        #Name of application - GUI Notepad with SQL
        self.title("GUI Notepad with SQL")
        self.filename = None
        
       # Initialize the database connection
        self.conn = sqlite3.connect('notepad.db')
        self.c = self.conn.cursor()

        # Create a table to store notes if it doesn't exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS notes
                         (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
        self.conn.commit()

        # Create a Text widget for the main text area
        self.text_area = tk.Text(self)
        self.text_area.pack(expand=True, fill='both')
        # Create a Menu bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Create a File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        # Create an Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.filename = None
        self.title("Untitled - GUI Notepad with SQL")
    def open_file(self):
        self.filename = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")]
        )
        if self.filename:
            self.text_area.delete(1.0, tk.END)
            with open(self.filename, "r") as file:
                self.text_area.insert(1.0, file.read())
            self.title(f"{self.filename} - GUI Notepad with SQL")
    def save_file(self):
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(
                initialfile='Untitled.txt',
                defaultextension=".txt",
                filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")]
            )
        if self.filename:
            with open(self.filename, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.title(f"{self.filename} - GUI Notepad with SQL")
    def cut(self):
        self.text_area.event_generate("<<Cut>>")
    def copy(self):
        self.text_area.event_generate("<<Copy>>")
    def paste(self):
        self.text_area.event_generate("<<Paste>>")
    def quit(self):
        self.conn.close()
        self.destroy()
if __name__ == "__main__":
    notepad_app = Notepad()
    notepad_app.mainloop()
