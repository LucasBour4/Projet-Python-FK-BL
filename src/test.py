from tkinter import *

class Application(Tk):
    def __init__(self):
        super().__init__()
        self.title("Navigation entre pages avec Frame")
        self.geometry("400x200")

        # Création des frames/pages
        self.frames = {}
        for F in (PageAccueil, Page2):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PageAccueil")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class PageAccueil(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        Label(self, text="Page d'accueil").pack(pady=10)
        Button(self, text="Aller à la page 2", command=lambda: controller.show_frame("Page2")).pack()

class Page2(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        Label(self, text="Page 2").pack(pady=10)
        Button(self, text="Retour à l'accueil", command=lambda: controller.show_frame("PageAccueil")).pack()

if __name__ == "__main__":
    app = Application()
    app.mainloop()