![Beautiful_Pancakes_Logo_Github](https://github.com/user-attachments/assets/082aedaa-4913-4213-8a99-4fca1eb6450c)

# Beautiful Pancakes - the QGraphicsScene custom serialization/deserialization package

Beautiful Pancakes can serialize/deserialize your QGraphicsScene to implement basic file
reading and writing for QGraphicsItems.

## It supports items such as:
- **QGraphicsRectItem**
- **QGraphicsLineItem**
- **QGraphicsEllipseItem**
- **QGraphicsTextItem**
- **QGraphicsPixmapItem**
- **QGraphicsPathItem**

## Usage
1. Clone the repository to your project via 
  `https://github.com/ktechhydle/beautiful_pancakes.git` and run `pip install -r requirements.txt`.
2. Import the `BeautifulPancakeCreator` class and initialize it.
3. There are four arguments to pass into the initializer:

- `scene`: Your QGraphicsScene
- `parent`: Your main window (this is for setting window titles based on open files)
- `app_name`: The name of your app
- `app_extension`: The file extension of your app (for example, MPRUN has the `.mp` file extension)

4. Once you have initialized the class correctly, use it's respective methods as you require (`load`, `save`, etc.)
5. We offer two versions of `BeautifulPancakeCreator`, PyQt5 and PySide6. Use whatever one your project requires.

## Methods
  Mentioned above, there are methods for loading, saving, saving as, and more. A full list of methods is 
  listed below:
- `reset_to_default_scene()`: Reset the scene (clear scene, reset filename, etc.)
- `save()`: Save current file
- `save_as()`: Save file as a new document (triggered automatically if `save` has been called and `filename` is `Untitled`)
- `load()`: Load file via a file dialog
- `load_from_file(filename: str)`: Load a file by passing the filename

*We will add items such as `QGraphicsGroupItem` in future updates, you will have to implement `QGraphicsSvgItem` yourself,
as there is no real way to obtain svg data without subclassing the item. For now, `BeautifulPancakeSerializer` and 
`BeautifulPancakeDeserializer` have methods that can make implementing these items yourself easy.*

## Full demo
```python
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from beautiful_pancakes.pyqt5 import BeautifulPancakeCreator
# optional: use pyside
# from beautiful_pancakes.pyside6 import BeautifulPancakeCreator

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
```

This will generate a window with a QGraphicsView/GraphicsScene and open a file dialog asking you where to save the file.

***We hope you enjoy, and remember to check release notes before updating any clones of this repository***
