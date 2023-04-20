from PyQt5 import QtGui
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtWidgets import*
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal,QTimer
import speech_recognition as sr
import difflib
import sys
import os
import pygame
import time
import subprocess


#得到gif动图的绝对路径

#得到当前工作文件夹的名字
current_dir = os.getcwd()
print(current_dir)
def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

#为了在语音识别的过程中更新界面UI，需要给其建立一个新的线程
class RecognitionThread(QThread):
    signal = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('请开始说话...')
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='en-US')
            self.signal.emit(text)
        except sr.UnknownValueError:
            print('无法识别输入音频')
        except sr.RequestError as e:
            print('无法从 Google Web 语音 API 中获取识别结果，错误原因：', e)
            self.signal.emit('')

class MyWidget(QWidget):
    #初始化界面
    def __init__(self):
        super().__init__()
        self.initUI()
        self.playing=False
    #加载界面
    def initUI(self):
        #设置要用到的一些图片的路径
        # self.PhoneImgPath=os.path.abspath('phone.png')
        # self.VoiceGif = os.path.abspath('siri.gif')
        # self.PhoneGif=os.path.abspath('play.gif')
        # self.Music_CHINA=os.path.abspath('CHINA-2.mp3')
        self.PhoneImgPath='phone.png'
        self.VoiceGif = 'siri.gif'
        self.PhoneGif='play.gif'
        self.Music_CHINA='CHINA-2.mp3'
        # 设置窗口大小和标题
        self.setGeometry(100, 100, 400, 500)
        self.setWindowTitle('My Voice Assistant')

        # 设置黑色背景
        self.setStyleSheet('background-color: black;')
        
        #标题：Hi! I'm Luna!
        Title=QLabel('Hi! I\'m Luna!' )
        Title.setStyleSheet('color: #20c2b1; font-size: 60px; margin-bottom:20px;font-weight: bold;')

        # 创建三个标签控件，用来显示文本
        label_text1 = QLabel('1.Say "Play Music" to play music!')
        label_text1.setStyleSheet('color: white; font-size: 30px; margin-top:20px;')
        label_text2 = QLabel('2.Say "Open Notepad" to take notes!')
        label_text2.setStyleSheet('color: white; font-size: 30px;margin-top:20px;')
        label_text3 = QLabel('3.Say "Open caculator" to open the caculator!')
        label_text3.setStyleSheet('color: white; font-size: 30px;margin-top:20px;')
        label_text4 = QLabel('4.Say "Stop music" to stop playing the music!')
        label_text4.setStyleSheet('color: white; font-size: 30px;margin-top:20px;')
        label_text5 = QLabel('5.Say "Goodbye" to exit \'Luna\'!')
        label_text5.setStyleSheet('color: white; font-size: 30px;margin-top:20px;')

        #设置三个标签控件都居中
        Title.setAlignment(Qt.AlignCenter)
        label_text1.setAlignment(Qt.AlignCenter)
        label_text2.setAlignment(Qt.AlignCenter)
        label_text3.setAlignment(Qt.AlignCenter)
        label_text4.setAlignment(Qt.AlignCenter)
        label_text5.setAlignment(Qt.AlignCenter)

        # 创建一个标签控件，用来显示动图
        movie = QMovie(self.VoiceGif)
        # 调整动图大小
        scaled_size = QSize(350, 200)
        movie.setScaledSize(scaled_size)
        #QLabel控件是 Qt 中用于显示文本和图像的控件
        label_gif = QLabel()
        label_gif.setMovie(movie)  #将动图放入QLabel中
        label_gif.setAlignment(Qt.AlignCenter)
        #使得动图动起来的启动函数
        movie.start()#如果没有调用 movie.start() 方法，动图就不会动起来

        # 创建一个按钮控件
        self.button = QPushButton('Click Me To Speak')  #按钮上的文字
        self.button.setFixedSize(250, 50)  #设置按钮的大小
        #将按钮挪到中心区域
        qr = self.button.frameGeometry()  #获取按钮的矩形区域，便于后面的布局和操作
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.button.move(qr.topLeft())
        self.button.setStyleSheet('QPushButton:pressed {background-color: #1383c2;} QPushButton:released {background-color: #20c2b1;} QPushButton{background-color: #20c2b1; color: white; font-size: 18px; border-radius: 10px;font-weight: bold;}')
        # self.button.setStyleSheet("QPushButton:pressed {background-color: darkblue;} QPushButton:released {background-color: #20c2b1;}")
        #绑定按钮的点击事件
        self.button.clicked.connect(self.start_recognition)

        #按钮控件右边放一个静止的话筒
        phone_static = QPixmap( self.PhoneImgPath)
        # 调整图片大小
        phone_static = phone_static.scaled(50, 50)        
        self.PhoneLabel=QLabel()
        self.PhoneLabel.setPixmap(phone_static) #将静止的话筒图片放入一个QLabel中
        
        #用来显示识别结果的标签
        self.result = QLabel('')
        self.result.setStyleSheet('color: white;font-size:30px;')
        self.result.setAlignment(Qt.AlignCenter)
        self.result.hide()    #一开始的时候隐藏

        # 设置布局
        layout = QVBoxLayout()   #创建一个垂直布局，这是界面整体的布局
        hbox = QHBoxLayout()     #创建一个水平布局，用来放按钮，并且实现他的居中
        
        layout.addWidget(Title)
        layout.addWidget(label_text1)
        layout.addWidget(label_text2)
        layout.addWidget(label_text3)
        layout.addWidget(label_text4)
        layout.addWidget(label_text5)
        layout.addWidget(label_gif)
        layout.addStretch()

        # 创建一个水平布局，用来放置按钮
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.button)
        hbox.addWidget(self.PhoneLabel)
        hbox.addStretch(1)
        # 添加水平布局到垂直布局中
        layout.addLayout(hbox)
        # 添加stretch使按钮居中
        layout.addStretch(1)
        layout.addWidget(self.result)

        self.setLayout(layout)
    #点击按钮开始进行语音识别
    def start_recognition(self):
        # 将右下角的phone图标变成动图
        phone_dy = QMovie(self.PhoneGif)
        # 调整动图大小
        scaled_size = QSize(50, 50)
        phone_dy.setScaledSize(scaled_size)
        #QLabel控件是 Qt 中用于显示文本和图像的控件
        self.PhoneLabel.setMovie(phone_dy)  #将动图放入QLabel中
        self.PhoneLabel.setAlignment(Qt.AlignCenter)
        #使得动图动起来的启动函数
        phone_dy.start()#如果没有调用 movie.start() 方法，动图就不会动起来
        
        print('phone该动动了吧')
        #这边需要给语音识别创建一个新的线程才可以使得上面的动起来
        
        # 创建一个语音识别线程，用于在后台进行语音识别
        self.thread = RecognitionThread(self)
        self.thread.signal.connect(self.show_recognition_result)
        self.thread.start()
  # 显示语音识别的结果
    def show_recognition_result(self, text):
        # 将右下角的 phone.png 图标显示在 QLabel 控件中
        phone_icon = QPixmap(os.path.abspath('phone.png'))
        scaled_size = QSize(50, 50)
        phone_icon = phone_icon.scaled(scaled_size, Qt.KeepAspectRatio)
        self.PhoneLabel.setPixmap(phone_icon)
        self.PhoneLabel.setAlignment(Qt.AlignCenter)
        print('识别结果：',text)
        #接下来需要将识别的结果进行相似度分析，选择相似度最高的指令执行相应的操作
        commend=["play music","open notepad","open the calculator","stop music","Goodbye"]
        list = [string_similar(text, "play music"),
                string_similar(text, "open notepad"),
                string_similar(text, "open the calculator"),
                string_similar(text, "stop music"),
                string_similar(text, "Goodbye")]

        max_value = max(list)           # 获得这中间的最大值
        max_index = list.index(max_value)     # 最大值的索引
        print("I guess you want to",commend[max_index])
        #在屏幕上打印出
        self.show_text("I guess you want to "+commend[max_index])
        #打开对应的功能
        self.execution(commend[max_index])

    def show_text(self, text):
        print(text)
        self.result.setText(text)
        self.result.show()
        # 创建一个 QTimer，6 秒后执行 hide_label 函数
        timer = QTimer()
        timer.singleShot(6000, self.hide_label)

    def hide_label(self):
        self.result.clear()
        self.result.hide()

    def execution(self,command):
        print(command)
        if command=="play music":
            self.playing=True
            #播放音乐
            pygame.mixer.init()
            pygame.mixer.music.load(self.Music_CHINA)
            pygame.mixer.music.play()
               # 计时 30 秒
            # time.sleep(30)
        
            # 暂停音乐播放
            # pygame.mixer.music.pause()
        if command=="open the calculator":
            subprocess.Popen('calc.exe')
        if command=="open notepad":
            subprocess.Popen('notepad.exe')
        if command=="stop music":
            if self.playing:
                pygame.mixer.music.stop()
                self.playing=False
        if command=="Goodbye":
            # 设置 QLabel 的文本并居中显示
            self.show_text("See You Next Time!")
            # time.sleep(5000)
            sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
