import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog, 
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PIL import Image 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import ImageFilter
from PIL.ImageQt import ImageQt
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)

app = QApplication([])
window = QWidget()
window.setWindowTitle('Easy Editor')
window.resize(700, 500)

lb_image = QLabel('Картинка')
btn_folder = QPushButton('Папка')
lw_files = QListWidget()

left_btn = QPushButton('Лево')
right_btn = QPushButton('Право')
mirror_btn = QPushButton('Зеркало')
color_btn = QPushButton('Ч/б')
sharp_btn = QPushButton('Резкость')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_folder)
col1.addWidget(lw_files)

col2.addWidget(lb_image, 95)

row_tools = QHBoxLayout()
row_tools.addWidget(left_btn)
row_tools.addWidget(right_btn)
row_tools.addWidget(mirror_btn)
row_tools.addWidget(color_btn)
row_tools.addWidget(sharp_btn)

col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)

window.setLayout(row)

workdir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extension):
    result = list()
    for i in files:
        for ex in extension:
            if i.endswith(ex):
                result.append(i)
    return result

def showFilenamesList():
    extension = ['.png', '.jpg', '.jpeg', '.gif']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extension)
    lw_files.clear()
    for i in filenames:
        lw_files.addItem(i)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'
    
    def LoadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    
    def ShowImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
    
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveimage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.ShowImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveimage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.ShowImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveimage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.ShowImage(image_path)

    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveimage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.ShowImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveimage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.ShowImage(image_path)


    def saveimage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)

        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
        

work_image = ImageProcessor()

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        work_image.LoadImage(workdir, filename) 
        image_path = os.path.join(work_image.dir, work_image.filename)
        work_image.ShowImage(image_path)

lw_files.currentRowChanged.connect(showChosenImage)

btn_folder.clicked.connect(showFilenamesList)
color_btn.clicked.connect(work_image.do_bw)
sharp_btn.clicked.connect(work_image.do_sharpen)
mirror_btn.clicked.connect(work_image.do_mirror)
left_btn.clicked.connect(work_image.do_left)
right_btn.clicked.connect(work_image.do_right)


window.show()
app.exec_()
