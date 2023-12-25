import librosa
import os
import numpy as np
import soundfile as sf

def resample_rate(path,new_sample_rate = 16000):
    signal, sr = librosa.load(path, sr=None)
    wavfile = path.split('/')[-1]
    wavfile = wavfile.split('.')[0]
    file_name = wavfile + '_new.wav'
    new_signal = librosa.resample(signal, sr, new_sample_rate) #
    #librosa.output.write_wav(file_name, new_signal , new_sample_rate)
    sf.write(file_name, new_signal, new_sample_rate, subtype='PCM_24')
    print(f'{file_name} has download.')
    return file_name
#
# wav_file = 'video/xxx.wav'
# resample_rate(wav_file,new_sample_rate = 16000)
