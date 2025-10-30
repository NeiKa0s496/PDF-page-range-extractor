from gui.interface import PDFExtractorApp
import tkinter as tk

def main():
    root = tk.Tk()
    app = PDFExtractorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()