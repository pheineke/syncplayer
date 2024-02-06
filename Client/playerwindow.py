import tkinter as tk
from player import Player  # Beachte die Großschreibung für Klassennamen

class LoginWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Player')
        
        self.ip = None
        self.port = None
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
        
        self.slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, length=200, resolution=1,
                               command=lambda value: self.on_slider_change(value))
        self.canvas1.create_window(self.window_width//2, (self.window_height//4)+2*self.window_height//6, window=self.slider)

        # Button für die Verbindung zum Server
        self.button1 = tk.Button(text='Connect to Server', command=lambda: self.get_inputs())
        self.canvas1.create_window(200, 220, window=self.button1)

    def on_slider_change(self, value):
        self.slider_value = int(value)
        self.port = self.slider_value + 12300

    def get_inputs(self):
        self.ip = self.ip_input_field.get()
        self.port = self.port_input_field.get()
        # Hier kannst du self.slider_value verwenden, um auf den Slider-Wert zuzugreifen
        print(f"IP: {self.ip}, Port: {self.port}, Slider Value: {self.slider_value}")

        p = Player()  # Beachte die Großschreibung für die Instanzierung
        p.run()

        # Starte die Tkinter Haupt-Schleife erst nach dem Button-Klick
        self.run()



    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.run()  # Entferne diesen Aufruf aus dem __main__-Block
