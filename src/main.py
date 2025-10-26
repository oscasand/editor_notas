import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

class SimpleNotepad:
    def __init__(self, root):
        self.root = root
        self.default_title = "Editor de Notas Simple"
        self.root.title(self.default_title)
        self.filename = None
        
        # Crear área de texto con scrollbar
        self.frame_text = tk.Frame(self.root)
        self.frame_text.pack(expand=True, fill='both')
        
        self.scrollbar = tk.Scrollbar(self.frame_text)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_area = tk.Text(self.frame_text, wrap=tk.WORD, undo=True,
                                yscrollcommand=self.scrollbar.set)
        self.text_area.pack(expand=True, fill='both')
        self.scrollbar.config(command=self.text_area.yview)
        
        # Barra de estado
        self.status_bar = ttk.Label(root, text="Listo", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Crear menú
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # Menú Archivo
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Nuevo", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Abrir", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Guardar", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Guardar como", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Menú Editar
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Editar", menu=self.edit_menu)
        self.edit_menu.add_command(label="Deshacer", command=self.text_area.edit_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Rehacer", command=self.text_area.edit_redo, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cortar", command=self.cut_text, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copiar", command=self.copy_text, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Pegar", command=self.paste_text, accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Seleccionar todo", command=self.select_all, accelerator="Ctrl+A")
        
        # Vincular atajos de teclado
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        
        # Vincular evento de cambios en el texto
        self.text_area.bind('<<Modified>>', self.changed)
        self.text_modified = False

    def _update_title(self):
        if self.filename:
            name = os.path.basename(self.filename)
            self.root.title(f"{self.default_title} - {name}")
        else:
            self.root.title(self.default_title)

    def changed(self, event=None):
        if self.text_area.edit_modified():
            self.text_modified = True
            words = len(self.text_area.get(1.0, tk.END).split())
            chars = len(self.text_area.get(1.0, tk.END)) - 1
            self.status_bar.config(text=f'Caracteres: {chars} Palabras: {words}')
        self.text_area.edit_modified(False)
        
    def new_file(self):
        if self.text_modified:
            response = messagebox.askyesnocancel("Guardar cambios", "¿Desea guardar los cambios?")
            if response is None:
                return
            if response:
                self.save_file()
        self.text_area.delete(1.0, tk.END)
        self.filename = None
        self.text_modified = False
        self.status_bar.config(text="Nuevo archivo")
        self._update_title()
        
    def open_file(self):
        if self.text_modified:
            response = messagebox.askyesnocancel("Guardar cambios", "¿Desea guardar los cambios?")
            if response is None:
                return
            if response:
                self.save_file()

        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                    filetypes=[("Archivos de texto", "*.txt"),
                                               ("Todos los archivos", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.filename = file_path
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, content)
                self.text_modified = False
                self.status_bar.config(text=f"Abierto: {os.path.basename(self.filename)}")
                self._update_title()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo: {str(e)}")

    def save_file(self):
        if self.filename:
            try:
                text = self.text_area.get(1.0, tk.END)
                with open(self.filename, 'w', encoding='utf-8') as file:
                    file.write(text)
                self.text_modified = False
                self.status_bar.config(text=f"Guardado: {os.path.basename(self.filename)}")
                self._update_title()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")
        else:
            self.save_as_file()
            
    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                      filetypes=[("Archivos de texto", "*.txt"),
                                                 ("Todos los archivos", "*.*")])
        if file_path:
            try:
                self.filename = file_path
                text = self.text_area.get(1.0, tk.END)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.text_modified = False
                self.status_bar.config(text=f"Guardado: {os.path.basename(self.filename)}")
                self._update_title()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")
        
        
    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")
        
        
    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")
        
        
    def select_all(self, event=None):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        return 'break'

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = SimpleNotepad(root)
    root.mainloop()