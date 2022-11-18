# System operations ...............
import sys
# OS module for operation .........
import os
# For alarm sound .................
import winsound
# Time module for applications.....
import time
# Notification for Timer time-out .....
from plyer import notification

# Importing PyQt5................. 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi

# Packages for play mp3s .....
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist

# Progress bar Class for application.....
from ProgressBar import CrlProgressBar
# All files and paths for them.....
full_list = []
# Only Songs in list ....................
song_list = []


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        # Loading Middle Watch UI.....................................
        loadUi('UI/MiddleWatch.ui', self)
        # Set window title  ..........................................
        self.setWindowTitle('MS StopWatch & Timer')

        # Set validation points to allow only to type numbers.........
        set_Validator_SecMin = QRegExpValidator(QRegExp('[0-9]+'))
        self.Seconds.setValidator(set_Validator_SecMin)
        self.Minutes.setValidator(set_Validator_SecMin)
        set_Validator_hrs = QRegExpValidator(QRegExp('[0-8]+'))
        self.Hours.setValidator(set_Validator_hrs)

        # Set background to transparent and frameless window & Always on Top ..............
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) # Set window frameless and Stay on top....
        self.setAttribute(Qt.WA_TranslucentBackground)                        # Set window transparent .................

        # Set text alignment to center......................................
        self.Seconds.setAlignment(Qt.AlignCenter)
        self.Minutes.setAlignment(Qt.AlignCenter)
        self.Hours.setAlignment(Qt.AlignCenter)
        # Set Window positions ..............................................
        self.oldPosition = None

        # Setting object to ProgressBar class...............................
        self.progress = CrlProgressBar()

        # Starting Qtimer...................................................
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.resumeOpz)  # Main function to run when Timer TimeOut
        self.timer.start(997)  # Time is decreased because few micro-seconds are needed for operations
        
        # Set-up Round progress bar in application ......... 
        self.ShowRoundProgressBar()
        
        # For make shadows for items in Ui...........
        self.shadow = QGraphicsDropShadowEffect(self)
        self.HighLt = {}  # Making objects for shadows.......

        # Setting default variables to their values.........
        self.timerStarted = False
        self.Sec_increment = 1
        self.Min_increment = 0
        self.Hrs_increment = 0
        self.TimerHrs = None
        self.TimerMins = None
        self.TimerSecs = None
        
        # Navigation for moving the application...........
        self.x1 = 0
        self.y1 = 0
        
        # Setting time-out count .........................
        self.TimeOut_Count = 0

        # making a object to QMediaPlaylist  Class...........
        self.playlist = QMediaPlaylist()
        
        # Audio payer Staff.......
        
        self.player = None
        # list that only contains mp3s..........
        self.song_list = []
        # list that contains all files in the folder..........
        self.full_list = []
        
        self.FolderAdded = 0
        self.Playing = 0
        # Index of song that playing ....................
        self.SongIndex = 0

        # Functions that critical for operation.........
        self.HandleButtons()
        self.HandleEditables()
        # Enabling shadow for progress bar...............
        self.Set_Shadow()

    def Set_Shadow(self):
        # Setting shadows for better visibility..........
        self.shadow.setBlurRadius(10)
        self.shadow.setXOffset(1)
        self.shadow.setYOffset(1)
        self.shadow.setColor(QColor(0, 0, 0, 200))
        self.label_MS.setGraphicsEffect(self.shadow)

        self.HighLt[1] = QGraphicsDropShadowEffect(self)
        self.HighLt[1].setBlurRadius(10)
        self.HighLt[1].setXOffset(1)
        self.HighLt[1].setYOffset(1)
        self.HighLt[1].setColor(QColor(0, 0, 0, 200))
        self.label_AppName.setGraphicsEffect(self.HighLt[1])

        self.HighLt[2] = QGraphicsDropShadowEffect(self)
        self.HighLt[2].setBlurRadius(10)
        self.HighLt[2].setXOffset(1)
        self.HighLt[2].setYOffset(1)
        self.HighLt[2].setColor(QColor(0, 0, 0, 200))
        self.Hours.setGraphicsEffect(self.HighLt[2])

        self.HighLt[3] = QGraphicsDropShadowEffect(self)
        self.HighLt[3].setBlurRadius(10)
        self.HighLt[3].setXOffset(1)
        self.HighLt[3].setYOffset(1)
        self.HighLt[3].setColor(QColor(0, 0, 0, 200))
        self.Minutes.setGraphicsEffect(self.HighLt[3])

        self.HighLt[4] = QGraphicsDropShadowEffect(self)
        self.HighLt[4].setBlurRadius(10)
        self.HighLt[4].setXOffset(1)
        self.HighLt[4].setYOffset(1)
        self.HighLt[4].setColor(QColor(0, 0, 0, 200))
        self.Seconds.setGraphicsEffect(self.HighLt[4])

        self.HighLt[5] = QGraphicsDropShadowEffect(self)
        self.HighLt[5].setBlurRadius(10)
        self.HighLt[5].setXOffset(1)
        self.HighLt[5].setYOffset(1)
        self.HighLt[5].setColor(QColor(0, 0, 0, 200))
        self.label_Sep1.setGraphicsEffect(self.HighLt[5])

        self.HighLt[6] = QGraphicsDropShadowEffect(self)
        self.HighLt[6].setBlurRadius(10)
        self.HighLt[6].setXOffset(1)
        self.HighLt[6].setYOffset(1)
        self.HighLt[6].setColor(QColor(0, 0, 0, 200))
        self.label_Sep2.setGraphicsEffect(self.HighLt[6])

        self.HighLt[7] = QGraphicsDropShadowEffect(self)
        self.HighLt[7].setBlurRadius(10)
        self.HighLt[7].setXOffset(1)
        self.HighLt[7].setYOffset(1)
        self.HighLt[7].setColor(QColor(0, 0, 0, 200))
        self.CloseBTN.setGraphicsEffect(self.HighLt[7])

        self.HighLt[8] = QGraphicsDropShadowEffect(self)
        self.HighLt[8].setBlurRadius(4)
        self.HighLt[8].setXOffset(1)
        self.HighLt[8].setYOffset(1)
        self.HighLt[8].setColor(QColor(0, 0, 0, 200))
        self.StartBTN.setGraphicsEffect(self.HighLt[8])

        self.HighLt[9] = QGraphicsDropShadowEffect(self)
        self.HighLt[9].setBlurRadius(4)
        self.HighLt[9].setXOffset(1)
        self.HighLt[9].setYOffset(1)
        self.HighLt[9].setColor(QColor(0, 0, 0, 200))
        self.ResetBTN.setGraphicsEffect(self.HighLt[9])

        self.HighLt[10] = QGraphicsDropShadowEffect(self)
        self.HighLt[10].setBlurRadius(4)
        self.HighLt[10].setXOffset(1)
        self.HighLt[10].setYOffset(1)
        self.HighLt[10].setColor(QColor(0, 0, 0, 200))
        self.StopBTN.setGraphicsEffect(self.HighLt[10])

        self.HighLt[11] = QGraphicsDropShadowEffect(self)
        self.HighLt[11].setBlurRadius(3)
        self.HighLt[11].setXOffset(1)
        self.HighLt[11].setYOffset(1)
        self.HighLt[11].setColor(QColor(0, 0, 0, 200))
        self.StopWatch.setGraphicsEffect(self.HighLt[11])

        self.HighLt[12] = QGraphicsDropShadowEffect(self)
        self.HighLt[12].setBlurRadius(3)
        self.HighLt[12].setXOffset(1)
        self.HighLt[12].setYOffset(1)
        self.HighLt[12].setColor(QColor(0, 0, 0, 200))
        self.Timer.setGraphicsEffect(self.HighLt[12])

    def HandleButtons(self):
        # Buttons that handle Main operations...........
        self.StopWatch.clicked.connect(self.SetTimerOpz)
        self.Timer.clicked.connect(self.SetStopWatchOpz)
        self.ResetBTN.clicked.connect(self.ReSet)
        self.StartBTN.clicked.connect(self.StartResume)
        self.StopBTN.clicked.connect(self.Stop)
        self.CloseBTN.clicked.connect(self.CloseApp)

        # Audio Player Buttons......................
        self.PlayBtn.clicked.connect(self.Play_Pause)
        self.Next.clicked.connect(self.NextSong)
        self.Back.clicked.connect(self.PreviousSong)
        self.Folder.clicked.connect(self.AudioFolder)

    def HandleEditables(self):
        # Setting Labels to readonly when starting.....
        self.Minutes.setReadOnly(True)
        self.Hours.setReadOnly(True)
        self.Seconds.setReadOnly(True)
        
        # Disable StopWatch button ....................
        self.StopWatch.setEnabled(False)

    def SetTimerOpz(self):

        if self.StopWatch.isChecked():
            self.Timer.setChecked(False)
            self.timerStarted = False
            self.Minutes.setReadOnly(True)
            self.Hours.setReadOnly(True)
            self.Seconds.setReadOnly(True)

            self.StopWatch.setEnabled(False)
            self.Timer.setEnabled(True)

    def SetStopWatchOpz(self):

        if self.Timer.isChecked():
            
            self.timerStarted = False
            self.StopWatch.setEnabled(True)
            self.StopWatch.setChecked(False)

            self.Timer.setEnabled(False)

            self.Minutes.setReadOnly(False)
            self.Hours.setReadOnly(False)
            self.Seconds.setReadOnly(False)

    def ShowRoundProgressBar(self):     # Calling progress bar ....

        self.progress.width = 527     # setting progress bar width ......
        self.progress.height = 527    # setting progress bar height .....

        self.progress.setFixedSize(self.progress.width, self.progress.height)
        self.progress.move(12, 12)                   # setting positions for middle clock and progress bar .......
        self.progress.setParent(self.centralwidget)  # setting parent for progress bar ........
        self.progress.Set_Shadow(True)               # make progress bar visible...............
        self.progress.lower()
        self.progress.show()

    def resumeOpz(self):
        if self.timerStarted:
            ############################################################################################################
            # Main StopWatch Operations....................................
            if self.StopWatch.isChecked():
                if self.Sec_increment == 60:

                    self.Seconds.setText('00')

                    self.progress.set_value(self.Sec_increment)
                    self.Sec_increment = 1
                    self.Min_increment += 1

                    if self.Min_increment < 10:
                        self.Minutes.setText(str(f"0{self.Min_increment}"))

                    elif self.Min_increment == 60:

                        self.Min_increment = 0
                        self.Minutes.setText("00")
                        self.Hrs_increment += 1

                        if self.Hrs_increment < 10:
                            self.Hours.setText(str(f"0{self.Hrs_increment}"))
                        else:
                            self.Hours.setText(str(self.Hrs_increment))

                    else:
                        self.Minutes.setText(str(self.Min_increment))
                    self.y1 = time.perf_counter()
                    print(f"Time = {(self.y1 - self.x1)}")
                elif self.Sec_increment <= 59:

                    if self.Sec_increment < 10:
                        self.Seconds.setText(f'0{str(self.Sec_increment)}')
                    else:
                        self.Seconds.setText(str(self.Sec_increment))

                    print(f'{str(self.Sec_increment)}')
                    self.progress.set_value(self.Sec_increment)
                    self.Sec_increment += 1
                    self.x1 = time.perf_counter()

            ############################################################################################################
            # Main Timer operations.............................

            elif self.Timer.isChecked():
                self.TimerSecs = int(self.TimerSecs)
                if self.TimerSecs != 0:
                    self.TimerSecs -= 1
                    self.progress.set_value(self.TimerSecs)
                    if self.TimerSecs < 10:
                        self.Seconds.setText(f"0{str(self.TimerSecs)}")
                    else:
                        self.Seconds.setText(str(self.TimerSecs))

                elif self.TimerSecs == 0:
                    self.TimerMins = int(self.Minutes.text())
                    if self.TimerMins != 0:
                        self.TimerSecs = 59
                        self.Seconds.setText("59")
                        self.progress.set_value(59)
                        self.TimerMins -= 1
                        if self.TimerMins < 10:
                            self.Minutes.setText(f"0{str(self.TimerMins)}")
                        else:
                            self.Minutes.setText(str(self.TimerMins))

                    elif self.TimerMins == 0:
                        self.TimerHrs = int(self.Hours.text())
                        if self.TimerHrs != 0:
                            self.TimerMins = 59
                            self.TimerSecs = 59
                            self.progress.set_value(59)
                            self.Minutes.setText("59")
                            self.Seconds.setText("59")
                            self.TimerHrs -= 1
                            if self.TimerHrs < 10:
                                self.Hours.setText(f"0{str(self.TimerHrs)}")
                            else:
                                self.Hours.setText(str(self.TimerHrs))
                        elif self.TimerHrs == 0:
                            self.TimeOut()

    def StartResume(self):
        self.timerStarted = True
        self.TimeOut_Count = 1
        self.StartBTN.setEnabled(False)
        self.StopBTN.setEnabled(True)

        if self.Timer.isChecked():
            try:
                self.TimerSecs = int(self.Seconds.text())
                self.TimerMins = int(self.Minutes.text())
                self.TimerHrs = int(self.Hours.text())
            except:  # ValueError

                if self.Seconds.text() == "":
                    self.TimerSecs = 0

                if self.Minutes.text() == "":
                    self.TimerMins = 0

                    self.Minutes.setText("00")
                if self.Hours.text() == "":
                    self.TimerHrs = 0
                    self.Hours.setText("00")

            print(f"Timer...{self.TimerSecs}.......{self.TimerMins}........{self.TimerHrs}.....")
            self.progress.set_value(self.TimerSecs)

            self.Minutes.setReadOnly(False)
            self.Hours.setReadOnly(False)
            self.Seconds.setReadOnly(False)

    def Stop(self):
        self.timerStarted = False
        self.StopBTN.setEnabled(False)
        self.StartBTN.setEnabled(True)
        if self.Timer.isChecked():
            self.Minutes.setReadOnly(False)
            self.Hours.setReadOnly(False)
            self.Seconds.setReadOnly(False)

    def ReSet(self):

        self.timerStarted = False
        self.Sec_increment = 1
        self.Min_increment = 0
        self.Hrs_increment = 0

        self.Seconds.setText("00")
        self.Minutes.setText("00")
        self.Hours.setText("00")
        self.progress.set_value(0)
        self.StartBTN.setEnabled(True)
        self.StopBTN.setEnabled(False)

        self.Minutes.setReadOnly(False)
        self.Hours.setReadOnly(False)
        self.Seconds.setReadOnly(False)

    def TimeOut(self):
        if self.TimeOut_Count == 1:
            winsound.PlaySound("Sounds/Alarm.wav", winsound.SND_FILENAME)
            self.Notification()
            self.TimeOut_Count = 0
            self.timerStarted = False
            self.StopBTN.setEnabled(False)
            self.StartBTN.setEnabled(True)

            self.Minutes.setReadOnly(False)
            self.Hours.setReadOnly(False)
            self.Seconds.setReadOnly(False)
            
    def Notification(self):
        notification.notify(
            title="MS StopWatch & Timer",
            message="Time-Out",
            app_icon="E:\other\Python\Projects\MS_StopWatch&Timer\Icons\icons.ico",
            timeout=10,
            app_name="MS StopWatch & Timer",
            ticker="Timer",
            toast=True
        )
        

    ####################################################################################################################
    """________________________________________ MP3 Playing Capabilities ____________________________________________"""

    def Play_Pause(self):
        if self.FolderAdded == 1 and len(self.song_list) != 0:

            if self.Playing == 0:
                print("Play")
                self.PlayBtn.setIcon(QIcon(r'Icons\pauseIcon.png'))
                self.GIF()
                self.Playing = 1

                QMediaPlaylist.setCurrentIndex(self.playlist, self.SongIndex)
                print("Audio Playing")
                self.player.play()


            elif self.Playing == 1:
                print("Pause")
                self.PlayBtn.setIcon(QIcon(r'Icons\playIcon.png'))
                self.label_MS.setText("MS")
                self.Playing = 0

                try:
                    self.player.pause()
                except:
                    print("Nothing to Stop")
        else:
            print("Add Audio folder that have MP3s")

    def AudioFolder(self):
        try:
            self.player.stop()
            self.label_MS.setText("MS")
            self.PlayBtn.setIcon(QIcon(r'Icons\playIcon.png'))
            self.Playing = 0
            self.SongIndex = 0

        except:
            print("Nothing playing now .................")
        if self.FolderAdded == 1:
            self.full_list.clear()
            self.song_list.clear()
            self.playlist.clear()
        try:
            Audio_folder = str(QFileDialog.getExistingDirectory(self, " Select Directory to Play Audios...."))

            song_list_content = os.listdir(Audio_folder)

            self.song_list = [x for x in song_list_content if x.endswith(".mp3")]

            for i in self.song_list:
                audio = f"{Audio_folder}/{i}"
                print(audio)
                self.full_list.append(audio)

            try:
                for item in self.full_list:
                    self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(item)))
                self.player = QMediaPlayer()
                self.player.setPlaylist(self.playlist)

            except:
                print("Error.........Song Listing........")

            self.FolderAdded = 1

        except OSError as x1:
            print(x1)
        except:
            print("Error happen while getting Mp3s form folder.....")

    def NextSong(self):
        print("Next")
        try:
            if self.SongIndex != len(self.song_list):
                self.SongIndex += 1
            elif self.SongIndex == len(self.song_list):
                self.SongIndex = 0

            QMediaPlaylist.setCurrentIndex(self.playlist, self.SongIndex)

        except AttributeError as e1:
            print(e1)
        except:
            print("Error happen when Forwarding")

    def PreviousSong(self):
        print("Back")
        try:
            if self.SongIndex != 0:
                self.SongIndex -= 1
            elif self.SongIndex == 0:
                self.SongIndex = len(self.song_list) - 1

            QMediaPlaylist.setCurrentIndex(self.playlist, self.SongIndex)

        except AttributeError as e1:
            print(e1)
        except:
            print("Error happen when Backing")

    def GIF(self):
        Loading_GIf = QMovie(r'GIFs\AudioWave.gif')
        self.label_MS.setMovie(Loading_GIf)
        Loading_GIf.start()
        

    ########################################################################################################################
    ".............................. Used to  closing Application because window is frame less ........................."

    def CloseApp(self):
        end_time = time.perf_counter()
        full_time = end_time - self.x1
        print(f"Time for all : {full_time}")
        print("............... Closing Application ...............")
        QApplication.instance().quit()

    ########################################################################################################################
    "......................... Mouse Press & Move Events help to move the Application window .........................."
 
    # setting previous position of the application  .................
    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    # setting moving positions to application .......................    
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
