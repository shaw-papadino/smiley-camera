# -*- coding: utf-8 -*-
#pulse2番からの入力を受ける。一定時間(RECROD_SECONDS)だけ録音し、ファイル名：file.wavで保存する。
import numpy as np
import pyaudio
import wave

import os
import datetime
import picamera


now=datetime.datetime.now()
dir_name=now.strftime('%m%d')
dir_path='/home/pi/'+dir_name

cam=picamera.PiCamera()

CHUNK= 1024*2
FORMAT = pyaudio.paInt16
CHANNELS = 2
 #サンプリングレート、マイク性能に依存
RATE = 44100
#録音時間
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME="file.wav"
 #pyaudio
audio = pyaudio.PyAudio()
try:
    while True:
        input_device_index = 2
        stream = audio.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
        print("capturing...")
        frames = []

        for i in range(0, RATE / CHUNK* RECORD_SECONDS):
            data = stream.read(CHUNK)
            frames.append(data)
            npdata = np.frombuffer(data, dtype="int16")

            left  = npdata[::2]
            right = npdata[1::2]

            lmax = np.max(left)
            rmax = np.max(right)

            print(lmax),
            print(rmax)

            if(lmax >= 10000 and rmax >= 10000):
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)
                file_name = now.strftime('%H:%M:%S')
                cam.capture(dir_path+"/"+file_name+".jpg")

        stream.stop_stream()
        stream.close()
        
except KeyboardInterrupt:
    pass
finally:
    audio.terminate()
    print("End of Smile captyring!")
                       
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFIle.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
