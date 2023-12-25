# 创建文件夹
import os
import pandas as pd
from pydub import AudioSegment
import subprocess
import ffmpeg
import pysilk


def createFile(file_path):
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    # 切换路径至上面创建的文件夹
    os.chdir(file_path)



def silk_to_pcm(silk_file, pcm_file):
    command = [
        "ffmpeg",
        "-i", silk_file,
        "-f", "s16le",
        "-acodec", "pcm_s16le",
        pcm_file
    ]
    subprocess.run(command)


from pydub import AudioSegment


def convert_slk_to_wav(slk_file_path, wav_file_path):
    # 读取SLK文件
    with open(slk_file_path, 'rb') as file:
        slk_data = file.read()

    # 将SLK数据转换为音频段
    audio_segment = AudioSegment(
        data=slk_data,
        frame_rate=16000,  # 假设SLK文件的采样率为16000Hz，根据实际情况进行调整
        sample_width=2,  # 假设SLK文件的采样宽度为16位（2字节），根据实际情况进行调整
        frame_count=len(slk_data) // 2  # 计算帧数，假设采样宽度为2字节
    )

    # 将音频段保存为WAV文件
    audio_segment.export(wav_file_path, format="wav")

def   ffmpeg_aur( input_file,output_file):
     input=ffmpeg.input(input_file)
     output=ffmpeg.output(input,output_file)
     ffmpeg.run(output)


slik_path="F:\\BaiduNetdiskDownload\\silk_v3_decoder.exe"
def  silk_change(input_path,pcm_path):
      command = [
            slik_path,
            input_path,
            pcm_path
       ]
      subprocess.run(command)
      subprocess.run("taskkill -f -t -im silk_v3_decoder.exe")

ffmpeg_path="E:\\ffmpeg\\ffmpeg-2023-12-18-git-be8a4f80b9-full_build\\bin\\ffmpeg.exe"
def  ffmpeg_change(pcmPath,target):
    command = [
          ffmpeg_path,
              "-y",
              "-f",
              "s16le",
              "-ar",
              "24000",
              "-ac",
              "1",
              "-i",
              pcmPath,
              target
      ]
    subprocess.run(command)

def  voice_to_wav(path,pcmPath,target):
    silk_change(path,pcmPath)
    ffmpeg_change(pcmPath,target)



if __name__ == '__main__':
    path="F:\\test_voice\\message-4670396532500881838-audio.slk"
    pcmPath =  "F:\\test_voice\\audio.pcm"
    target = "F:\\test_voice\\audio.mp3"
    # createFile(out_path)
    # 使用函数
    # silk_to_pcm()
    # pysilk.encode_file(open(path, "rb"), out_path)
    # 调用函数进行转换
    # convert_slk _to_wav(path, out_path)
    # ffmpeg_aur(path,out_path)
    silk_change(path,pcmPath)
    # pcmPath = "F:\\test_voice\\audio.pcm"
    ffmpeg_change(pcmPath,target)
