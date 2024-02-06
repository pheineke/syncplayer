import socket
import threading
import wave
import pyaudio
import pickle
import struct
import time
import os
import glob

host_name = socket.gethostname()
host_ip = '10.10.10.199'
print(host_ip)
port = 12347
test = False
test2 = True
test3 = False

clients = []  # Liste zum Speichern der verbundenen Clients
clients_lock = threading.Lock()  # Lock für die Thread-Sicherheit der Clients-Liste

# Variable, um den Status des Streams zu speichern (pausiert oder nicht)
stream_paused = False

class SongPlayer:
    def __init__(self, folder_path='./resource'):
        self.folder_path = folder_path
        self.songs = self.get_song_list()
        self.current_song_index = 0

    def get_song_list(self):
        song_list = glob.glob(os.path.join(self.folder_path, '*.wav'))
        return song_list

    def play_next_song(self):
        if self.current_song_index < len(self.songs):
            return self.songs[self.current_song_index]
        else:
            return None

    def move_to_next_song(self):
        self.current_song_index += 1
        if self.current_song_index >= len(self.songs):
            self.current_song_index = 0

def audio_stream(client_socket, song_player):
    p = pyaudio.PyAudio()

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

    while True:
        if clients and test3 and not stream_paused:
            song_path = song_player.play_next_song()
            if song_path:
                wf = wave.open(song_path, 'rb')
                data = wf.readframes(CHUNK)
                while data:
                    a = pickle.dumps(data)
                    message = struct.pack("Q", len(a)) + a
                    with clients_lock:  # Sicheres Lesen der Clients-Liste
                        for client in clients:
                            try:
                                client.send(message)
                            except Exception as e:
                                print("Error sending audio to client:", str(e))
                                if client in clients:  # Überprüfung vor der Entfernung
                                    clients.remove(client)  # Client entfernen, wenn ein Fehler auftritt
                    data = wf.readframes(CHUNK)
                wf.close()
                song_player.move_to_next_song()

def accept_clients(server_socket, song_player):
    while True:
        global test
        global test2
        global test3
        print(test, test2, test3)
        client_socket, addr = server_socket.accept()
        print('Accepted connection from', addr)
        with clients_lock:  # Sicheres Bearbeiten der Clients-Liste
            pause_stream()
            clients.append(client_socket)  # Hinzufügen des neuen Clients zur Liste
            time.sleep(1)
            resume_stream()
        if test2:
            if len(clients) >= 1:
                test2 = False
                test = True
                test3 = True
                # Start the song player thread
                song_player_thread = threading.Thread(target=song_player_run, args=(song_player,))
                song_player_thread.start()
        if test:
            client_thread = threading.Thread(target=audio_stream, args=(client_socket, song_player))
            client_thread.start()
            test = False

def song_player_run(song_player):
    while True:
        song_path = song_player.play_next_song()
        if song_path:
            print(f"Playing: {song_path}")
            wf = wave.open(song_path, 'rb')
            duration = wf.getnframes() / float(wf.getframerate())
            time.sleep(duration)
            song_player.move_to_next_song()
            wf.close()

def audio_stream_server(song_player):
    server_socket = socket.socket()
    server_socket.bind((host_ip, (port-1)))

    server_socket.listen(5)
    print('Server listening at', (host_ip, (port-1)))

    accept_clients(server_socket, song_player)

# Funktion zum Pausieren des Streams
def pause_stream():
    global stream_paused
    stream_paused = True

# Funktion zum Fortsetzen des Streams
def resume_stream():
    global stream_paused
    stream_paused = False

if __name__ == "__main__":
    song_player = SongPlayer()
    t1 = threading.Thread(target=audio_stream_server, args=(song_player,))
    t1.start()
