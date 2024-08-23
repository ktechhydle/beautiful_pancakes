from imports import *

class SceneManager:
    def __init__(self, scene: QGraphicsScene, parent: QMainWindow, app_name='', app_extension=''):
        self.scene = scene
        self.parent = parent
        self.filename = 'Untitled'
        self.app_name = app_name
        self.app_extension = app_extension

    def reset_to_default_scene(self):
        self.scene.clear()
        self.filename = 'Untitled'
        self.parent.setWindowTitle(f'{self.filename} - {self.app_name}')

    def load(self, parent):
        try:
            filename, _ = QFileDialog.getOpenFileName(self.parent, 'Open File', '',
                                                      f'{self.app_name} files (*{self.app_extension})')

            if filename:
                self.scene.clear()

                with open(filename, 'rb') as f:
                    items_data = pickle.load(f)
                    self.deserialize_items(items_data)

                    self.filename = filename
                    parent.setWindowTitle(f'{os.path.basename(self.filename)} - MPRUN')


        except Exception as e:
            QMessageBox.critical(self.parent,
                                 'Open File Error',
                                 'The document you are attempting to open has been corrupted. '
                                 'Please open a different document, or repair any changes.')

            print(e)

    def load_from_file(self, filename, parent):
        try:
            self.scene.clear()

            with open(filename, 'rb') as f:
                items_data = pickle.load(f)
                self.deserialize_items(items_data)

                self.filename = filename
                parent.setWindowTitle(f'{os.path.basename(self.filename)} - {self.app_name}')

        except Exception as e:
            QMessageBox.critical(self.parent,
                                 'Open File Error',
                                 'The document you are attempting to open has been corrupted. '
                                 'Please open a different document, or repair any changes.')

            print(e)

    def serialize_items(self):
        items_data = []

        for item in self.scene.items():
            pass

        return items_data

    def serialize_item_attributes(self, item):
        return [{
            'rotation': item.rotation(),
            'transform': self.serialize_transform(item.transform()),
            'scale': item.scale(),
            'transformorigin': self.serialize_point(item.transformOriginPoint()),
            'x': item.pos().x(),
            'y': item.pos().y(),
            'name': item.toolTip(),
            'zval': item.zValue(),
            'visible': item.isVisible(),
        }]

    def serialize_color(self, color: QColor):
        return {
            'red': color.red(),
            'green': color.green(),
            'blue': color.blue(),
            'alpha': color.alpha(),
        }

    def serialize_pen(self, pen: QPen):
        return {
            'width': pen.width(),
            'color': self.serialize_color(pen.color()),
            'style': pen.style(),
            'capstyle': pen.capStyle(),
            'joinstyle': pen.joinStyle()
        }

    def serialize_brush(self, brush: QBrush):
        return {
            'color': self.serialize_color(brush.color()),
            'style': brush.style()
        }

    def serialize_font(self, font: QFont):
        return {
            'family': font.family(),
            'pointsize': font.pixelSize(),
            'letterspacing': font.letterSpacing(),
            'bold': font.bold(),
            'italic': font.italic(),
            'underline': font.underline(),
        }

    def serialize_transform(self, transform: QTransform):
        return {
            'm11': transform.m11(),
            'm12': transform.m12(),
            'm13': transform.m13(),
            'm21': transform.m21(),
            'm22': transform.m22(),
            'm23': transform.m23(),
            'm31': transform.m31(),
            'm32': transform.m32(),
            'm33': transform.m33()
        }

    def serialize_point(self, point: QPointF):
        return {'x': point.x(), 'y': point.y()}

    def serialize_path(self, path: QPainterPath):
        elements = []
        for i in range(path.elementCount()):
            element = path.elementAt(i)
            if element.isMoveTo():
                elements.append({'type': 'moveTo', 'x': element.x, 'y': element.y})
            elif element.isLineTo():
                elements.append({'type': 'lineTo', 'x': element.x, 'y': element.y})
            elif element.isCurveTo():
                elements.append({'type': 'curveTo', 'x': element.x, 'y': element.y})
        return elements

    def deserialize_items(self, items_data):
        for item_data in items_data:
            pass

    def deserialize_color(self, color):
        return QColor(color['red'], color['green'], color['blue'], color['alpha'])

    def deserialize_pen(self, data):
        pen = QPen()
        pen.setWidth(data['width'])
        pen.setColor(self.deserialize_color(data['color']))
        pen.setStyle(data['style'])
        pen.setCapStyle(data['capstyle'])
        pen.setJoinStyle(data['joinstyle'])
        return pen

    def deserialize_brush(self, data):
        brush = QBrush()
        brush.setColor(self.deserialize_color(data['color']))
        brush.setStyle(data['style'])
        return brush

    def deserialize_font(self, data):
        font = QFont()
        font.setFamily(data['family'])
        font.setPixelSize(data['pointsize'])
        font.setLetterSpacing(QFont.AbsoluteSpacing, data['letterspacing'])
        font.setBold(data['bold'])
        font.setItalic(data['italic'])
        font.setUnderline(data['underline'])
        return font

    def deserialize_transform(self, data):
        transform = QTransform(
            data['m11'], data['m12'], data['m13'],
            data['m21'], data['m22'], data['m23'],
            data['m31'], data['m32'], data['m33']
        )
        return transform

    def deserialize_point(self, data):
        return QPointF(data['x'], data['y'])

    def deserialize_text_item(self, data):
        text_item = CustomTextItem(data['text'])
        text_item.setFont(self.deserialize_font(data['font']))
        text_item.setDefaultTextColor(self.deserialize_color(data['color']))
        text_item.locked = data['locked']

        for attr in data['attr']:
            text_item.setTransformOriginPoint(self.deserialize_point(attr['transformorigin']))
            text_item.setRotation(attr['rotation'])
            text_item.setTransform(self.deserialize_transform(attr['transform']))
            text_item.setScale(attr['scale'])
            text_item.setPos(attr['x'], attr['y'])
            text_item.setToolTip(attr['name'])
            text_item.setZValue(attr['zval'])
            text_item.setVisible(attr['visible'])

        if data.get('markdown', True):
            text_item.toMarkdown()

        return text_item

    def deserialize_path_item(self, data):
        sub_path = QPainterPath()
        for element in data['elements']:
            if element['type'] == 'moveTo':
                sub_path.moveTo(element['x'], element['y'])
            elif element['type'] == 'lineTo':
                sub_path.lineTo(element['x'], element['y'])
            elif element['type'] == 'curveTo':
                sub_path.cubicTo(element['x'],
                                 element['y'],
                                 element['x'],
                                 element['y'],
                                 element['x'],
                                 element['y'])

        path_item = CustomPathItem(sub_path)
        path_item.setPen(self.deserialize_pen(data['pen']))
        path_item.setBrush(self.deserialize_brush(data['brush']))

        for attr in data['attr']:
            path_item.setTransformOriginPoint(self.deserialize_point(attr['transformorigin']))
            path_item.setRotation(attr['rotation'])
            path_item.setTransform(self.deserialize_transform(attr['transform']))
            path_item.setScale(attr['scale'])
            path_item.setPos(attr['x'], attr['y'])
            path_item.setToolTip(attr['name'])
            path_item.setZValue(attr['zval'])
            path_item.setVisible(attr['visible'])

        if data.get('smooth', True):
            path_item.smooth = True

        else:
            path_item.smooth = False

        if data.get('addtext', True):
            path_item.add_text = True
            path_item.setTextAlongPath(data['textalongpath'])
            path_item.setTextAlongPathColor(self.deserialize_color(data['textcolor']))
            path_item.setTextAlongPathFont(self.deserialize_font(data['textfont']))
            path_item.setTextAlongPathSpacingFromPath(data['textspacing'])
            path_item.setTextAlongPathFromBeginning(data['starttextfrombeginning'])

        else:
            path_item.add_text = False

        return path_item