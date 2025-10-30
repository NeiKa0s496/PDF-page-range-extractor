import PyPDF2
import os

class PDFOperations:
    def __init__(self):
        pass
    
    def examinar_pdf(self, archivo_entrada):
        """Examina un archivo PDF y retorna información sobre él"""
        try:
            with open(archivo_entrada, 'rb') as archivo:
                lector = PyPDF2.PdfReader(archivo)
                
                info = {
                    'total_paginas': len(lector.pages),
                    'titulo': lector.metadata.get('/Title', 'No disponible'),
                    'autor': lector.metadata.get('/Author', 'No disponible'),
                    'creado': lector.metadata.get('/CreationDate', 'No disponible'),
                    'modificado': lector.metadata.get('/ModDate', 'No disponible'),
                    'nombre_archivo': os.path.basename(archivo_entrada)
                }
                
                return info
                
        except Exception as e:
            raise Exception(f"Error al examinar PDF: {e}")
    
    def extraer_paginas(self, archivo_entrada, archivo_salida, pagina_inicio, pagina_fin):
        """Extrae un rango de páginas de un PDF y las guarda en un nuevo archivo"""
        try:
            with open(archivo_entrada, 'rb') as archivo:
                lector = PyPDF2.PdfReader(archivo)
                escritor = PyPDF2.PdfWriter()
                
                # Validar rango de páginas
                if pagina_inicio < 1 or pagina_fin > len(lector.pages):
                    raise ValueError(f"Rango de páginas no válido. El PDF tiene {len(lector.pages)} páginas.")
                
                # Extraer las páginas deseadas
                for pagina_num in range(pagina_inicio - 1, pagina_fin):
                    pagina = lector.pages[pagina_num]
                    escritor.add_page(pagina)
                
                # Guardar el nuevo PDF
                with open(archivo_salida, 'wb') as output_file:
                    escritor.write(output_file)
                    
        except Exception as e:
            raise Exception(f"Error en extracción: {e}")
    
    def obtener_total_paginas(self, archivo_entrada):
        """Obtiene el número total de páginas de un PDF"""
        try:
            with open(archivo_entrada, 'rb') as archivo:
                lector = PyPDF2.PdfReader(archivo)
                return len(lector.pages)
        except Exception as e:
            raise Exception(f"Error al obtener páginas: {e}")