import sys
from time import strftime, localtime
import threading
from time import sleep
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuick import QQuickWindow
from PyQt6.QtCore import QObject, pyqtSignal, Qt, pyqtSlot

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget
)

class Backend(QObject):
    updated = pyqtSignal(str, arguments=['updater'])

    def __init__(self):
        QWidget.__init__(self)
        
    @pyqtSlot(str)
    def getNews(self):
        print("Gathering news on life cycle assessment")
        
    def updater(self, curr_time):
        self.updated.emit(curr_time)
        
    def bootUp(self):
        t_thread = threading.Thread(target=self._bootUp)
        t_thread.daemon = True
        t_thread.start()
        
    def _bootUp(self):
        while True:
            curr_time = strftime("%H:%M:%S", localtime())
            self.updater(curr_time)
            sleep(0.1)

if __name__ == "__main__":
    QQuickWindow.setSceneGraphBackend('software')

    app = QApplication(sys.argv)
    
    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)

    engine.load('./main.qml')
    # engine.load('./UIButton.qml')
    # engine.load('./ButtonPresser.qml')

    back_end = Backend()

    engine.rootObjects()[0].setProperty('backend', back_end)

    back_end.bootUp()

    sys.exit(app.exec())