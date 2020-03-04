import os
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QStandardItemModel

from xml_creator import xml_creator
from xml_creator.gui_utils import ImageItem, XmlModel, XmlModelObject, \
    XmlSizeObject


class XmlCreator(QtWidgets.QMainWindow, xml_creator.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.folder_select_button.clicked.connect(self.list_folder)
        self.images_list.doubleClicked.connect(self.display_selected_item)
        self.add_to_model_button.clicked.connect(self.add_to_model)
        self.save_schema_button.clicked.connect(self.save_model)
        self.delete_object_button.clicked.connect(self.delete_field)
        self.label.mousePressEvent = self.mouse_press
        self.label.mouseReleaseEvent = self.mouse_release
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.current_object = None
        self.selected_item = None
        self.xml_model = XmlModel()
        self.tree_view_model = None

    def list_folder(self):
        try:
            folder_path = QtWidgets.QFileDialog.getExistingDirectoryUrl(
                self, 'Select folder').path()
            files = sorted(os.listdir(folder_path))
            self.images_list.clear()
            for file in files:
                path = os.path.join(folder_path, file)
                ImageItem(path, self.images_list)
        except FileNotFoundError:
            pass

    def display_selected_item(self):
        self.selected_item = self.images_list.selectedItems()[0]
        img = self.selected_item.image
        pixmap = QPixmap(img)
        self.xml_model = XmlModel()
        self.xml_model.filename = self.selected_item.image_name
        self.xml_model.folder = self.selected_item.image_folder
        self.selected_item: ImageItem
        shape = [int(img.width()),
                 int(img.height()),
                 int(img.depth())]
        size = XmlSizeObject(shape)
        self.xml_model.size = size
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())
        self.label.show()

        self.tree_view_model = QStandardItemModel(0, 4, parent=self)
        self.tree_view_model.setHeaderData(0, Qt.Horizontal, 'xmin')
        self.tree_view_model.setHeaderData(1, Qt.Horizontal, 'ymin')
        self.tree_view_model.setHeaderData(2, Qt.Horizontal, 'xmax')
        self.tree_view_model.setHeaderData(3, Qt.Horizontal, 'ymax')
        self.objects_list_view.setModel(self.tree_view_model)
        self.objects_list_view.show()

    def mouse_press(self, event):
        self.begin = event.pos()

    def mouse_release(self, event):
        self.end = event.pos()
        self.current_object = XmlModelObject(
            [min(self.begin.x(), self.end.x()),
             min(self.begin.y(), self.end.y()),
             max(self.begin.x(), self.end.x()),
             max(self.begin.y(), self.end.y())],
            name=self.types_box.currentText()
        )
        # self.xml_model.objects.append(self.current_object)
        self.point_coords_output.setText('start: {}, {}\nend: {}, {}'.format(
            self.current_object.bbox[0], self.current_object.bbox[1],
            self.current_object.bbox[2], self.current_object.bbox[3]))

    def add_to_model(self):
        self.xml_model.objects.append(self.current_object)
        self.add_field_to_view_model(self.current_object.bbox)
        self.display_schema()

    def delete_field(self):
        if self.tree_view_model:
            index = self.objects_list_view.currentIndex().row()
            box = [int(self.tree_view_model.item(index, i).text()) for i in
                   range(4)]
            if box:
                for field in self.xml_model.objects:
                    if field.bbox == box:
                        self.xml_model.objects.remove(field)
                        self.tree_view_model.removeRow(index)
                        self.objects_list_view.show()
                        self.display_schema()

    def display_schema(self):
        self.schema_output.setText(self.xml_model.to_xml())

    def save_model(self):
        with open('1065dataset/annots/' + self.xml_model.filename.split('.')[0]
                  + '.xml', 'w') as f:
            f.writelines(self.xml_model.to_xml())

    def add_field_to_view_model(self, box):
        self.tree_view_model.insertRow(0)
        self.tree_view_model.setData(self.tree_view_model.index(0, 0), box[0])
        self.tree_view_model.setData(self.tree_view_model.index(0, 1), box[1])
        self.tree_view_model.setData(self.tree_view_model.index(0, 2), box[2])
        self.tree_view_model.setData(self.tree_view_model.index(0, 3), box[3])
        self.objects_list_view.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window_ = XmlCreator()
    window_.show()
    app.exec_()


if __name__ == '__main__':
    main()
