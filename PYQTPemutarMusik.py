import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QListWidget, QPushButton, QFileDialog, QLabel, QSlider, QHBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl, QTimer

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initPlayer()

    def initUI(self):
        self.setWindowTitle("Aplikasi Pemutar Musik")
        self.setGeometry(100, 100, 600, 300)

        self.playList = QListWidget(self)
        self.playList.setGeometry(20, 20, 200, 250)

        self.addButton = QPushButton("Tambah Lagu", self)
        self.addButton.setGeometry(250, 20, 120, 30)
        self.addButton.clicked.connect(self.addMusic)

        self.playButton = QPushButton("Mainkan", self)
        self.playButton.setGeometry(250, 70, 120, 30)
        self.playButton.clicked.connect(self.playMusic)

        self.stopButton = QPushButton("Hentikan", self)
        self.stopButton.setGeometry(250, 120, 120, 30)
        self.stopButton.clicked.connect(self.stopMusic)

        self.volumeLabel = QLabel("Volume:", self)
        self.volumeLabel.setGeometry(250, 170, 80, 30)

        self.volumeSlider = QSlider(Qt.Horizontal, self)
        self.volumeSlider.setGeometry(330, 170, 100, 30)
        self.volumeSlider.setValue(50)
        self.volumeSlider.valueChanged.connect(self.setVolume)

        self.durationLabel = QLabel(self)
        self.durationLabel.setGeometry(250, 220, 100, 30)

        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVolume(50)
        self.mediaPlayer.stateChanged.connect(self.updateButtons)
        self.mediaPlayer.positionChanged.connect(self.updateDuration)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDuration)

    def initPlayer(self):
        self.playlist = []
        self.currentTrack = 0
        self.mediaPlayer.mediaStatusChanged.connect(self.nextTrack)

    def addMusic(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        files, _ = QFileDialog.getOpenFileNames(self, "Pilih Lagu", "", "File Musik (*.mp3 *.ogg *.wav)", options=options)
        if files:
            self.playlist.extend(files)
            self.playList.addItems([os.path.basename(file) for file in files])

    def playMusic(self):
        if self.playlist:
            media = QMediaContent(QUrl.fromLocalFile(self.playlist[self.currentTrack]))
            self.mediaPlayer.setMedia(media)
            self.mediaPlayer.play()
            self.timer.start(1000)  # Timer untuk mengupdate durasi setiap detik

    def stopMusic(self):
        self.mediaPlayer.stop()
        self.timer.stop()
        self.durationLabel.setText("")

    def setVolume(self):
        volume = self.volumeSlider.value()
        self.mediaPlayer.setVolume(volume)

    def updateButtons(self):
        state = self.mediaPlayer.state()
        if state == QMediaPlayer.PlayingState:
            self.playButton.setEnabled(False)
            self.stopButton.setEnabled(True)
        elif state == QMediaPlayer.StoppedState:
            self.playButton.setEnabled(True)
            self.stopButton.setEnabled(False)
        elif state == QMediaPlayer.PausedState:
            self.playButton.setEnabled(True)
            self.stopButton.setEnabled(True)

    def updateDuration(self):
        if self.mediaPlayer.duration() > 0:
            position = self.mediaPlayer.position() // 1000
            duration = self.mediaPlayer.duration() // 1000
            minutes = position // 60
            seconds = position % 60
            self.durationLabel.setText(f"{minutes:02}:{seconds:02} / {duration // 60:02}:{duration % 60:02}")

    def nextTrack(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.currentTrack = (self.currentTrack + 1) % len(self.playlist)
            self.playMusic()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())
