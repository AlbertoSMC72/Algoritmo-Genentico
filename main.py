import tkinter as tk
from ui.patio_designer import PatioDesigner

def main():
    root = tk.Tk()
    app = PatioDesigner(root)
    root.mainloop()

if __name__ == "__main__":
    main()
