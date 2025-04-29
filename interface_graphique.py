from tkinter import *
from tkinter import ttk

# https://python.doctor/page-tkinter-interface-graphique-python-tutoriel
# https://stackoverflow.com/questions/22925599/mouse-position-python-tkinter

#Programme 

application = Tk()

nom_application = Label(application, text = "Votre compte réservation", font = ("Arial", 20), fg = "Green")
nom_application.pack()

bouton = Button(application, text="Cliquez ici", command=quit, background="blue", fg="white", font=("Arial", 12))
bouton.config(width=20, height=2)
bouton.pack()

canvas = Canvas(application, width=200, height=200)
canvas.pack()

canvas.create_rectangle(0, 50, 500, 500, fill='red')

application.mainloop()