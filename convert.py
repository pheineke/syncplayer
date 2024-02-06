from pydub import AudioSegment
sound = AudioSegment.from_mp3("./temp_2.mp3")
sound.export("./temp_2.wav", format="wav")

