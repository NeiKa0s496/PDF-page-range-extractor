import os
from tkinter import messagebox

class InputValidator:
    def __init__(self):
        pass
    
    def validar_interfaz(self, archivo_entrada, archivo_salida, pagina_inicio_str, pagina_fin_str, total_paginas):
        """Valida todos los campos de la interfaz gráfica"""
        if not archivo_entrada:
            messagebox.showerror("Error", "Seleccione un archivo PDF de entrada")
            return False
        
        if not os.path.exists(archivo_entrada):
            messagebox.showerror("Error", "El archivo de entrada no existe")
            return False
        
        if not archivo_salida:
            messagebox.showerror("Error", "Error en archivo PDF de salida")
            return False
        
        # Valida que las páginas sean números
        try:
            pagina_inicio = int(pagina_inicio_str)
            pagina_fin = int(pagina_fin_str)
        except ValueError:
            messagebox.showerror("Error", "Las páginas deben ser números enteros")
            return False
        
        # Valida rango de páginas
        if pagina_inicio < 1 or pagina_fin > total_paginas:
            messagebox.showerror("Error", f"El rango de páginas no es válido. El PDF tiene {total_paginas} páginas.")
            return False
        
        if pagina_inicio > pagina_fin:
            messagebox.showerror("Error", "La página inicial no puede ser mayor que la página final")
            return False
        
        return True
    
    def validar_rango_paginas(self, pagina_inicio, pagina_fin, total_paginas):
        """Valida que el rango de páginas sea correcto"""
        if pagina_inicio < 1 or pagina_fin > total_paginas:
            return False, f"Rango inválido. El PDF tiene {total_paginas} páginas."
        
        if pagina_inicio > pagina_fin:
            return False, "La página inicial no puede ser mayor que la final"
        
        return True, "Rango válido"