import re
from xml.dom.minidom import parseString

from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QListWidgetItem
from dicttoxml import dicttoxml


class ImageItem(QListWidgetItem):

    def __init__(self, text, widget):
        super().__init__(text, widget)
        self.path_to_image = text
        # self._image = QImage(text)
        self.image_name = self.path_to_image.split('/')[-1]
        self.image_folder = self.path_to_image.split('/')[-3]

    def text(self):
        return self.path_to_image

    @property
    def image(self):
        return QImage(self.path_to_image)


class XmlModel:

    def __init__(self, folder=None, filename=None, size=None, objects=None):
        self.folder = folder or ''
        self.filename = filename or ''
        self.size = size
        self.objects = objects or []

    def to_dict(self):
        return {
            'folder': self.folder,
            'filename': self.filename,
            'size': {
                'width': self.size.width,
                'height': self.size.height,
                'depth': self.size.depth
            },
            'objects': [{'object': obj.to_dict()} for obj in self.objects]
        }

    def to_xml(self):
        tmp = dicttoxml(self.to_dict(), custom_root='annotation').decode(
            'utf-8')
        tmp = re.sub('</?objects.*?>', '', tmp)
        tmp = re.sub('</?item.*?>', '', tmp)
        tmp = parseString(tmp)
        tmp = tmp.toprettyxml()
        tmp = re.sub('<\?xml.*?>', '', tmp)
        return tmp[1:]


class XmlSizeObject:

    def __init__(self, shape):
        self.width = shape[0]
        self.height = shape[1]
        self.depth = shape[2]

    def to_dict(self):
        return {
            'width': self.width,
            'height': self.height,
            'depth': self.depth
        }


class XmlModelObject:

    def __init__(self, bbox, name='checkbox'):
        self.bbox = bbox
        self.name = name

    def to_dict(self):
        return {
            'name': self.name,
            'bndbox': {
                'xmin': self.bbox[0],
                'ymin': self.bbox[1],
                'xmax': self.bbox[2],
                'ymax': self.bbox[3]
            }
        }
