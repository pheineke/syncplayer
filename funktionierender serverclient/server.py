import socket
import threading
import wave
import pyaudio
import pickle
import struct
import asyncio


host_name = socket.gethostname()
host_ip = '10.10.10.199'
print(host_ip)
port = 12346
test = True

clients = []  # Liste zum Speichern der verbundenen Clients
clients_lock = threading.Lock()  # Lock für die Thread-Sicherheit der Clients-Liste

def audio_stream(client_socket):
    wf = wave.open("./resource/temp.wav", 'rb')

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

    data = None
    while True:
        if clients:
            data = wf.readframes(CHUNK)
            a = pickle.dumps(data)
            message = struct.pack("Q", len(a)) + a
            print(clients)
            with clients_lock:  # Sicheres Lesen der Clients-Liste
                for client in clients:
                    try:
                        client.send(message)

                    except Exception as e:
                        print("Error sending audio to client:", str(e))
                        if client in clients:  # Überprüfung vor der Entfernung
                            clients.remove(client)  # Client entfernen, wenn ein Fehler auftritt

def accept_clients(server_socket):
    while True:
        global test
        client_socket, addr = server_socket.accept()
        print('Accepted connection from', addr)
        with clients_lock:  # Sicheres Bearbeiten der Clients-Liste
            clients.append(client_socket)  # Hinzufügen des neuen Clients zur Liste
        if test:
                    client_thread = threading.Thread(target=audio_stream, args=(client_socket,))
                    client_thread.start()
                    test = False

def audio_stream_server():
    server_socket = socket.socket()
    server_socket.bind((host_ip, (port-1)))

    server_socket.listen(5)
    print('Server listening at', (host_ip, (port-1)))

    accept_clients(server_socket)


t1 = threading.Thread(target=audio_stream_server, args=())
t1.start()
