# -*- coding: utf-8 -*-

import pyaudio
import wave
import numpy as np
from matplotlib import pyplot as plt

import datetime
import os
import picamera

now=datetime.datetime.now()
dir_name=now.strftime('%m%d')
dir_path='/home/pi/'+dir_name

#オーディオ初期設定
FORMAT = pyaudio.paInt16
CHANNELS = 2        #ステレオ
RATE = 44100        #サンプルレート
CHUNK = 2**11       #データ点数
RECORD_SECONDS = 60 #録音する時間の長さ


#start pyaudio
audio = pyaudio.PyAudio()
cam=picamera.PiCamera()

frames_e = []
frames_m = []
try:
        #open stream
        input_device_index = 2
        stream = audio.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
        print ("capturing...")
        #データを入れる箱
        frames = []
        
        if not os.path.exists(dir_path):
                    os.mkdir(dir_path)
##        if not os.path.isdir(dir_path):
##                os.makedirs(dir_path)
         #ファイル作成
        file_name = now.strftime('%H:%M:%S')
        #カメラ撮影
        cam.start_recording(dir_path+"/"+file_name+".h264")

        #play stream
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK) #データを読む
            frames.append(data)       #箱にデータを追加
            npdata = np.frombuffer(data, dtype = "int16") #データを整数型にする

            #左チャンネル
            emg = npdata[::2]
            #右チャンネル
            mic = npdata[1::2]

            e_max = np.max(emg)
            
            m_max= np.max(mic)
            
            frames_e.append(e_max)
            frames_m.append(m_max)

            print(e_max),
            print(m_max)
            

            #stop stream
        stream.stop_stream()
        stream.close()

            #stop recording
        cam.stop_recording()

            

except KeyboardInterrupt:
        pass
finally:
        #finish pyaudio
        audio.terminate()
        print("End of Smile captyring!")
        plt.plot(frames_e,label = "EMG",color="crimson",lw =5)
        plt.plot(frames_m,label = "MIC",color="midnightblue",lw = 5)
        plt.legend()

        plt.title("Smile Capture Data")
        plt.xlabel("time")
        plt.ylabel("value")

        plt.ylim(-100,32768)
        plt.show()
