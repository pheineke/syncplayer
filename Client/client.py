import socket
import os
import wave
import pyaudio
import pickle
import struct
import threading

class Player():
    def __init__(self) -> None:
        self.host_ip = '10.10.10.199'
        self.port = 12347
        self.running = True

    def run(self):
        def audio_stream():
            p = pyaudio.PyAudio()
            CHUNK = 1024
            stream = p.open(format=p.get_format_from_width(2),
                            channels=2,
                            rate=44100,
                            output=True,
                            frames_per_buffer=CHUNK)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                socket_address = (self.host_ip, self.port - 1)
                print('server listening at', socket_address)
                client_socket.connect(socket_address)
                print("CLIENT CONNECTED TO", socket_address)

                data = b""
                payload_size = struct.calcsize("Q")
                while self.running:
                    try:
                        while len(data) < payload_size:
                            packet = client_socket.recv(4 * 1024)  # 4K
                            if not packet:
                                break
                            data += packet
                        packed_msg_size = data[:payload_size]
                        data = data[payload_size:]
                        msg_size = struct.unpack("Q", packed_msg_size)[0]
                        while len(data) < msg_size:
                            data += client_socket.recv(4 * 1024)
                        frame_data = data[:msg_size]
                        data = data[msg_size:]
                        frame = pickle.loads(frame_data)
                        stream.write(frame)
                    except Exception as e:
                        print("Error:", e)
                        break

            print('Audio closed')
        t1 = threading.Thread(target=audio_stream, args=())
        t1.start()

if __name__ == "__main__":
    p = Player()
    p.run()