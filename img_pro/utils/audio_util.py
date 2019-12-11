from pygame import mixer
import pygame
import time
from threading import Thread

class Audio:
    def __init__(self, path, playCount=1):
        self.path = path
        self.playCount = playCount
        self.isPlaying = False
        mixer.init()  # mixer的初始化
        mixer.music.load(self.path)

    def play(self):
        def task():
            # 检查音乐流播放，有返回True，没有返回False
            count = 0
            while count < self.playCount:
                if mixer.music.get_busy() == False:  # 检查是否正在播放音乐
                    self.isPlaying = True
                    mixer.music.play()  # 开始播放音乐
                    count += 1
                if count == self.playCount:
                    self.isPlaying = False
                    print('播放完成')
                    break
        if self.isPlaying is False:
            self.isPlaying = True
            t = Thread(target=task)
            t.start()


    def pause(self):
        pass

    def stop(self):
        if mixer is not None:
            mixer.music.stop()
