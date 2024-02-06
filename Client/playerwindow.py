import tkinter as tk
from client import Player  # Beachte die Großschreibung für Klassennamen

class LoginWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Player')
        
        self.ip = '10.10.10.199'
        self.port = 12347
        self.slider_value = None  # Hinzugefügtes Attribut für den Slider-Wert

        self.window_width, self.window_height = 400, 300

        self.canvas1 = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas1.pack()

        # Erstes Eingabefeld für die IP-Adresse
        self.ip_input_field = tk.Entry(self.root) 
        self.canvas1.create_window(self.window_width//2, self.window_height//4, window=self.ip_input_field)

        # Zweites Eingabefeld für den Port
        self.port_input_field = tk.Entry(self.root) 
        self.canvas1.create_window(self.window_width//2, (self.window_height//4)*2-self.window_height//6, window=self.port_input_field)

        # Slider für den zweiten Bereich
        self.slider_label = tk.Label(self.root, text="Slider Value:")
        self.canvas1.create_window(self.window_width//2, (self.window_height//4)+self.window_height//6, window=self.slider_label)
        
        # Button für die Verbindung zum Server
        self.button1 = tk.Button(text='Connect to Server', command=lambda: self.get_inputs())
        self.canvas1.create_window(200, 220, window=self.button1)



    def get_inputs(self):
        self.ip = self.ip_input_field.get()
        self.port = self.port_input_field.get()

        p = Player()  # Beachte die Großschreibung für die Instanzierung
        p.run()

        # Starte die Tkinter Haupt-Schleife erst nach dem Button-Klick
        self.run()



    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.run()  # Entferne diesen Aufruf aus dem __main__-Block
