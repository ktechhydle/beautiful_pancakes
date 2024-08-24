from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyqt import BeautifulPancakeCreator


# optional: use pyside
# from beautiful_pancakes.pyside import BeautifulPancakeCreator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        self.setCentralWidget(self.view)
        self.setWindowTitle("Demo")

        # Add items to the scene
        rect_item = QGraphicsRectItem(0, 0, 100, 100)
        self.scene.addItem(rect_item)

        manager = BeautifulPancakeCreator(self.scene, self, app_name='Demo', app_extension='.demo')
        manager.save()


app = QApplication([])
window = MainWindow()
window.show()
app.exec()