# Beautiful Pancakes
***The official QGraphicsScene custom file writing/reading framework of MP Software based on MPRUN's SceneManager class***

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

## Methods
Mentioned above, there are methods for loading, saving, saving as, and more. A full list of methods is 
listed below:
- `reset_to_default_scene()`: Reset the scene (clear scene, reset filename, etc.)
- `save()`: Save current file
- `save_as()`: Save file as a new document (triggered automatically if `save` has been called and `filename` is `Untitled`)
- `load()`: Load file via a file dialog
- `load_from_file(filename: str)`: Load a file by passing the filename

## Supported Items
- **QGraphicsRectItem**
- **QGraphicsLineItem**
- **QGraphicsEllipseItem**
- **QGraphicsTextItem**
- **QGraphicsPixmapItem**
- **QGraphicsPathItem**

*We will add items such as QGraphicsSvgItem and QGraphicsGroupItem in future updates. 
For now, `BeautifulPancakeSerializer` and `BeautifulPancakeDeserializer` have methods 
that can make implementing these items yourself easy.*

## Full demo
```
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from beautiful_pancakes.managers import BeautifulPancakeCreator

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

***We hope you enjoy, and remember to check release notes before updating any clones of this repository***
