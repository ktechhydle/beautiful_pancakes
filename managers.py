from imports import *


class BeautifulPancakeCreator:
    def __init__(self, scene: QGraphicsScene, parent: QMainWindow, app_name='', app_extension=''):
        self.scene = scene
        self.parent = parent
        self.filename = 'Untitled'
        self.app_name = app_name
        self.app_extension = app_extension

        self.serializer = BeautifulPancakeSerializer(self.scene)
        self.deserializer = BeautifulPancakeDeserializer(self.scene)

    def reset_to_default_scene(self):
        self.scene.clear()
        self.filename = 'Untitled'
        self.parent.setWindowTitle(f'{self.filename} - {self.app_name}')

    def save(self):
        try:
            if self.filename != 'Untitled':
                with open(self.filename, 'wb') as f:
                    pickle.dump(self.serializer.serialize_items(), f)
                    self.parent.setWindowTitle(f'{os.path.basename(self.filename)} - {self.app_name}')

            else:
                self.saveas()

        except Exception as e:
            QMessageBox.critical(self.parent, 'Open File Error', f'Error saving scene: {e}', QMessageBox.Ok)

    def saveas(self):
        filename, _ = QFileDialog.getSaveFileName(self.parent, 'Save As', '',
                                                  f'{self.app_name} files (*{self.app_extension})')

        if filename:
            try:
                with open(filename, 'wb') as f:
                    pickle.dump(self.serializer.serialize_items(), f)

                    self.filename = filename
                    self.parent.setWindowTitle(f'{os.path.basename(self.filename)} - {self.app_name}')

                    return True

            except Exception as e:
                print(e)

        else:
            return False

    def load(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self.parent, 'Open File', '',
                                                      f'{self.app_name} files (*{self.app_extension})')

            if filename:
                self.scene.clear()

                with open(filename, 'rb') as f:
                    items_data = pickle.load(f)
                    self.deserializer.deserialize_items(items_data)

                    self.filename = filename
                    self.parent.setWindowTitle(f'{os.path.basename(self.filename)} - MPRUN')


        except Exception as e:
            QMessageBox.critical(self.parent,
                                 'Open File Error',
                                 'The document you are attempting to open has been corrupted. '
                                 'Please open a different document, or repair any changes.')

            print(e)

    def load_from_file(self, filename: str):
        try:
            self.scene.clear()

            with open(filename, 'rb') as f:
                items_data = pickle.load(f)
                self.deserializer.deserialize_items(items_data)

                self.filename = filename
                self.parent.setWindowTitle(f'{os.path.basename(self.filename)} - {self.app_name}')

        except Exception as e:
            QMessageBox.critical(self.parent,
                                 'Open File Error',
                                 'The document you are attempting to open has been corrupted. '
                                 'Please open a different document, or repair any changes.')

            print(e)

class BeautifulPancakeSerializer:
    def __init__(self, scene):
        self.scene = scene

    def serialize_items(self):
        items_data = []

        for item in self.scene.items():
            item_data = self.serialize_item_attributes(item)

            if isinstance(item, QGraphicsRectItem):
                item_data.append({
                    'rect': self.serialize_rect(item.rect()),
                    'pen': self.serialize_pen(item.pen()),
                    'brush': self.serialize_brush(item.brush())
                })
            elif isinstance(item, QGraphicsEllipseItem):
                item_data.append({
                    'rect': self.serialize_rect(item.rect()),
                    'pen': self.serialize_pen(item.pen()),
                    'brush': self.serialize_brush(item.brush())
                })
            elif isinstance(item, QGraphicsLineItem):
                item_data.append({
                    'line': self.serialize_line(item.line()),
                    'pen': self.serialize_pen(item.pen())
                })
            elif isinstance(item, QGraphicsTextItem):
                item_data.append({
                    'text': item.toPlainText(),
                    'font': self.serialize_font(item.font()),
                    'defaultTextColor': self.serialize_color(item.defaultTextColor())
                })
            elif isinstance(item, QGraphicsPixmapItem):
                item_data.append({
                    'pixmap': item.pixmap().toImage().bits().asstring(
                        item.pixmap().width() * item.pixmap().height() * 4)
                    # Example serialization, may need a better approach
                })
            elif isinstance(item, QGraphicsPathItem):
                item_data.append({
                    'path': self.serialize_path(item.path()),
                    'pen': self.serialize_pen(item.pen()),
                    'brush': self.serialize_brush(item.brush())
                })

            items_data.append(item_data)

        return items_data

    def serialize_rect(self, rect: QRectF):
        return {
            'x': rect.x(),
            'y': rect.y(),
            'width': rect.width(),
            'height': rect.height()
        }

    def serialize_line(self, line: QLineF):
        return {
            'x1': line.x1(),
            'y1': line.y1(),
            'x2': line.x2(),
            'y2': line.y2()
        }

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

class BeautifulPancakeDeserializer:
    def __init__(self, scene):
        self.scene = scene

    def deserialize_items(self, items_data):
        items = []

        for item_data in items_data:
            base_attributes = item_data[0]
            transform = self.deserialize_transform(base_attributes['transform'])
            item = None

            if 'rect' in item_data[1]:
                item = QGraphicsRectItem(self.deserialize_rect(item_data[1]['rect']))
                item.setPen(self.deserialize_pen(item_data[1]['pen']))
                item.setBrush(self.deserialize_brush(item_data[1]['brush']))
            elif 'line' in item_data[1]:
                item = QGraphicsLineItem(self.deserialize_line(item_data[1]['line']))
                item.setPen(self.deserialize_pen(item_data[1]['pen']))
            elif 'text' in item_data[1]:
                item = QGraphicsTextItem(item_data[1]['text'])
                item.setFont(self.deserialize_font(item_data[1]['font']))
                item.setDefaultTextColor(self.deserialize_color(item_data[1]['defaultTextColor']))
            elif 'pixmap' in item_data[1]:
                pixmap = QPixmap()
                pixmap.loadFromData(item_data[1]['pixmap'])
                item = QGraphicsPixmapItem(pixmap)
            elif 'path' in item_data[1]:
                item = QGraphicsPathItem(self.deserialize_path(item_data[1]['path']))
                item.setPen(self.deserialize_pen(item_data[1]['pen']))
                item.setBrush(self.deserialize_brush(item_data[1]['brush']))

            if item:
                item.setPos(base_attributes['x'], base_attributes['y'])
                item.setRotation(base_attributes['rotation'])
                item.setTransformOriginPoint(self.deserialize_point(base_attributes['transformorigin']))
                item.setScale(base_attributes['scale'])
                item.setZValue(base_attributes['zval'])
                item.setVisible(base_attributes['visible'])
                item.setTransform(transform)
                item.setToolTip(base_attributes['name'])
                self.scene.addItem(item)
                items.append(item)

        return items

    def deserialize_rect(self, data):
        return QRectF(data['x'], data['y'], data['width'], data['height'])

    def deserialize_line(self, data):
        return QLineF(data['x1'], data['y1'], data['x2'], data['y2'])

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

    def deserialize_path(self, data):
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

        return sub_path
