# -*- coding: utf-8 -*-

import pyaudio
import wave
import numpy as np
#import matplotlib .pyplot as plt

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
WAVE_OUTPUT_FILENAME = "file.wav"

#start pyaudio
audio = pyaudio.PyAudio()
cam=picamera.PiCamera()

try:
        #open stream
        stream = audio.open(format=FORMAT, channels=CHANNELS,
        rate=RATE, input=True,
        input_device_index=2,   #デバイスのインデックス番号
        frames_per_buffer=CHUNK)

        print ("capturing...")
        #データを入れる箱
        frames = []

        if not os.path.isdir(dir_path):
                os.makedirs(dir_path)
         #ファイル作成
        file_name = now.strftime('%H:%M:%S')
        #カメラ撮影
        cam.start_recording(dir_path+"/"+file_name+".h264")
##        cam.wait_recording(60)
        #play stream
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK) #データを読む
            frames.append(data)       #箱にデータを追加
            npdata = np.frombuffer(data, dtype = "int16") #データを整数型にする

            #左チャンネル
            left = npdata[::2]
            #右チャンネル
            right = npdata[1::2]

            lmax = np.max(left)

            rmax = np.max(right)

            print(lmax),
            print(rmax)

            #stop stream
        stream.stop_stream()
        stream.close()

            #stop recording
        cam.stop_recording()

            #finish pyaudio
        audio.terminate()

except KeyboardInterrupt:
    pass

##    #stop stream
##    stream.stop_stream()
##    stream.close()
##
##    #stop recording
##    cam.stop_recording()
##
##    #finish pyaudio
##    audio.terminate()


##    lmax_nom = lmax/2**15
##    rmax_nom = rmax/2**15
##    x = np.arange(0,int(RATE / CHUNK * RECORD_SECONDS),0.1)
##    plt.subplot(2,1,1)
##    plt.plot(x, lmax_nom)
##    plt.title("LMAX")
##    plt.xlim(0, int(RATE / CHUNK * RECORD_SECONDS))
##    plt.ylim(-0.1,1.1)
##
##    plt.subplot(2,1,2)
##    plt.plot(x, rmax_nom)
##    plt.title("RMAX")
##    plt.xlim(0, int(RATE / CHUNK * RECORD_SECONDS))
##    plt.ylim(-0.1,1.1)
##
##    plt.tight_layout()
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
