# Beautiful Pancakes
***The official QGraphicsScene custom file writing/reading framework of MP Software***

## Usage
1. Clone the repository to your project via 
`https://github.com/ktechhydle/beautiful_pancakes.git`
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
