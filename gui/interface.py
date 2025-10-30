import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from pdf.operations import PDFOperations
from utils.validators import InputValidator

class PDFExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Extractor de PDF")
        self.root.geometry("600x500")
        
        self.pdf_ops = PDFOperations()
        self.validator = InputValidator()
        
        # Variables
        self.archivo_entrada = tk.StringVar()
        self.archivo_salida = tk.StringVar()
        self.pagina_inicio = tk.StringVar()
        self.pagina_fin = tk.StringVar()
        self.total_paginas = 0
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        titulo = ttk.Label(main_frame, text="Extractor de Páginas PDF", font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Selección archivo entrada
        ttk.Label(main_frame, text="Archivo PDF de entrada:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.archivo_entrada, width=50).grid(row=1, column=1, pady=5, padx=5)
        ttk.Button(main_frame, text="Examinar", command=self.seleccionar_archivo_entrada).grid(row=1, column=2, pady=5)
        
        # Información del PDF
        self.info_label = ttk.Label(main_frame, text="Seleccione un archivo PDF para ver su información", foreground="blue")
        self.info_label.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Rango de páginas
        ttk.Label(main_frame, text="Página inicial:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.pagina_inicio, width=10).grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        
        ttk.Label(main_frame, text="Página final:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.pagina_fin, width=10).grid(row=4, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Selección archivo salida
        ttk.Label(main_frame, text="Archivo PDF de salida:").grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.archivo_salida, width=50).grid(row=5, column=1, pady=5, padx=5)
        ttk.Button(main_frame, text="Examinar", command=self.seleccionar_archivo_salida).grid(row=5, column=2, pady=5)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Extraer Páginas", command=self.extraer_paginas).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Salir", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Área de log
        ttk.Label(main_frame, text="Log de operaciones:").grid(row=7, column=0, sticky=tk.W, pady=(20, 5))
        self.log_text = tk.Text(main_frame, height=10, width=70)
        self.log_text.grid(row=8, column=0, columnspan=3, pady=5)
        
        # Scrollbar para el log
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=8, column=3, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)
    
    def seleccionar_archivo_entrada(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo PDF",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            self.archivo_entrada.set(archivo)
            self.examinar_pdf(archivo)
            # Sugerir nombre para el archivo de salida
            nombre_base = os.path.splitext(archivo)[0]
            self.archivo_salida.set(f"{nombre_base}_extraido.pdf")
    
    def seleccionar_archivo_salida(self):
        archivo = filedialog.asksaveasfilename(
            title="Guardar PDF como",
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            self.archivo_salida.set(archivo)
    
    def examinar_pdf(self, archivo_entrada):
        try:
            info_pdf = self.pdf_ops.examinar_pdf(archivo_entrada)
            self.total_paginas = info_pdf['total_paginas']
            
            info_text = f"Archivo: {os.path.basename(archivo_entrada)} | "
            info_text += f"Páginas: {self.total_paginas} | "
            info_text += f"Autor: {info_pdf['autor']} | "
            info_text += f"Título: {info_pdf['titulo']}"
            
            self.info_label.config(text=info_text)
            self.log(f"PDF examinado: {archivo_entrada}")
            self.log(f"Total de páginas: {self.total_paginas}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo examinar el PDF: {e}")
            self.log(f"Error al examinar PDF: {e}")
    
    def extraer_paginas(self):
        if not self.validar_campos():
            return
        
        try:
            archivo_entrada = self.archivo_entrada.get()
            archivo_salida = self.archivo_salida.get()
            pagina_inicio = int(self.pagina_inicio.get())
            pagina_fin = int(self.pagina_fin.get())
            
            self.log(f"Iniciando extracción: páginas {pagina_inicio} a {pagina_fin}")
            
            # Usar la clase de operaciones PDF
            self.pdf_ops.extraer_paginas(archivo_entrada, archivo_salida, pagina_inicio, pagina_fin)
            
            self.log(f"Extracción completada: {archivo_salida}")
            self.log(f"Páginas extraídas: {pagina_inicio} - {pagina_fin}")
            self.log(f"Total de páginas en nuevo PDF: {pagina_fin - pagina_inicio + 1}")
            
            messagebox.showinfo("Éxito", f"PDF creado exitosamente:\n{archivo_salida}")
            
        except Exception as e:
            error_msg = f"Error durante la extracción: {e}"
            self.log(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def validar_campos(self):
        return self.validator.validar_interfaz(
            self.archivo_entrada.get(),
            self.archivo_salida.get(),
            self.pagina_inicio.get(),
            self.pagina_fin.get(),
            self.total_paginas
        )
    
    def limpiar_campos(self):
        self.archivo_entrada.set("")
        self.archivo_salida.set("")
        self.pagina_inicio.set("")
        self.pagina_fin.set("")
        self.info_label.config(text="Seleccione un archivo PDF para ver su información")
        self.log_text.delete(1.0, tk.END)
        self.total_paginas = 0
    
    def log(self, mensaje):
        self.log_text.insert(tk.END, f"{mensaje}\n")
        self.log_text.see(tk.END)