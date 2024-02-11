import socket
import pyaudio

# Server-Konfiguration
SERVER_HOST = '10.10.10.199'
SERVER_PORT = 12345

# PyAudio-Konfiguration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Funktion zum Erfassen von Audio und Senden an den Server
def send_audio(stream):
    while True:
        try:
            data = stream.read(CHUNK)
            client_socket.sendall(data)
        except KeyboardInterrupt:
            break

# Hauptprogramm
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

audio_stream = pyaudio.PyAudio().open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK)

send_audio(audio_stream)

client_socket.close()