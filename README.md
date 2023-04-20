# SpeechRecognitionAssignment-TongjiHCI
这是同济大学2023年春季学期人机交互的第二次作业，内容是使用Python中语音识别的库写一个机器人，并使用pyQT5进行图形化界面设计。

HCI Lab1 Automatic Speech Recognition

环境要求：
1.Python 3.7.16 
2.代码编辑器：VScode(我是用这个写的）
3.依赖的Python包：
      图形界面库：PyQt5
      语音识别库：speech_recognition
      音乐播放：pygame
      打开计算机应用程序：subprocess
      比较字符串相似度：difflib
4.系统：Windows
5.网络代理（因为使用了recognize_google函数调用Google的API）

运行方法：
1.(推荐)命令行下运行：
   cd+code文件夹的地址 ——进入code文件夹内
   
   python LunaInterface.py ——运行该文件

2.在VScode中运行：
   ·打开VScode，然后选择File>Open Folder。
   ·然后选择Code文件夹打开。（一定要选择Code文件夹然后打开，否则可能会出现文件路径错误）
   ·将VScode的Python环境切换到我上面所说的Python环境中。
   ·打开LunaInterface.py，在文档空白处右击，选择“Run Python File in terminal”,就可以运行这个Python文件了。

使用方法：
运行成功之后，点击页面下方的蓝色按钮，然后说出页面提示的指令就可以执行相应的操作了。

