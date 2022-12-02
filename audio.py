import color

import wave
import numpy as np
import moviepy.editor as mpe
import os

import matplotlib.pyplot as plt
from multiprocessing import Process
import simpleaudio as sa

# TIME = NR_FRAMES / FRAME_RATE
# T......NR_FRAMES
# 5/1000......X
# X = 5*NR_FRAMES / T

def get_images_from_sound(raw, nr_sampled_frames, frame_rate):
    images = []
    index = 0
    color_vector = color.create_color_vector()
    while index<=len(raw):
        raw_sample = raw[index:index+nr_sampled_frames]
        index+=nr_sampled_frames
        ft = np.fft.fft(raw_sample)
        magnitude_spectrum = np.abs(ft)
        frequency = np.linspace(0, frame_rate, len(magnitude_spectrum))
        ratio = 2
        freq_range = int(len(frequency)*ratio)
        frequency = frequency[:freq_range]
        magnitude_spectrum = magnitude_spectrum[:freq_range]
        max_freq = int(frequency[np.argmax(magnitude_spectrum)])

        img = color.generate_img(color_vector[(max_freq)%len(color_vector)])
        images += [img]

    return images

def play_audio(path):
    filename = path
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  

if __name__ == '__main__':
    path = 'sounds/yngmt.wav'
    wav = wave.open(path, 'r')
    raw = wav.readframes(-1)
    raw = np.frombuffer(raw, 'int16')
    # new_raw = []
    # if wav.getnchannels()==2:
    #     for i in range(len(raw)):
    #         if i%2==0:
    #             new_raw+=[raw[i]]
    #     raw = new_raw[:]
    nr_frames = wav.getnframes()
    frame_rate = wav.getframerate()
    time = nr_frames/frame_rate

    nr_sampled_frames =nr_frames//int(color.FRAME_RATE*time) 
    nr_sampled_frames *= wav.getnchannels()

    images = get_images_from_sound(raw, nr_sampled_frames=nr_sampled_frames, frame_rate=frame_rate)
    color.create_video(images)
    video = mpe.VideoFileClip(color.AUX_VIDEO_PATH)
    audio_background = mpe.AudioFileClip(path)
    final = video.set_audio(audio_background)
    final.write_videofile("videos/output.mp4")
    os.remove(color.AUX_VIDEO_PATH)

    #print(nr_sampled_frames, time)
    #p1 = Process(target=play_audio, args=(path,))
    #p1.start()
    #p2 = Process(target=visualize_sound, args=(raw, nr_sampled_frames, frame_rate, SAMPLE_TIME_IN_MS))
    #p2.start()
    #p1.join()
    #p2.join()
   