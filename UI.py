### qt drag and drop file
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout , QProgressBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.models import load_model


# Path to your saved model
model_path = r'C:\python\COMPUTER VISION\tensorflow\image_classification\model_checkpoint.h5'

celebrity_dict = {
    6: "Ali_Daei",
    4: "Mehran_Ghafoorian",
    7: "Reza_Attaran",
    0: "sogol_khaligh",
    8: "Ali_Beyranvand",
    5: "java_Razavian",
    14: "sahar dolatshahi",
    1: "Mohsen_chavoshi",
    12: "bahram_radan",
    9: "mohammad_esfahani",
    3: "Tarane_Alidosti",
    2: "Bahare_KianAfshar",
    10: "Jalal_Hosseini",
    11: "Homayoon_Shajarian",
    13: "Nazanin_Bayati"
}

# Load the trained model
loaded_model = load_model(model_path)

def predict(image):

    image = cv2.imread(image)
    image = cv2.resize(image , (256 , 256))
    image = image / 255
    result = loaded_model.predict(np.expand_dims(image , 0))
    print(np.argmax(result))
    prediction = celebrity_dict[np.argmax(result)]
    return prediction


class ImageLabel(QLabel):

    def __init__(self):

        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setMaximumWidth(600)
        self.setMinimumHeight(500)
        self.setMaximumHeight(900)
        self.setScaledContents(True)
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

class AppDemo(QWidget):

    def __init__(self):

        super().__init__()
        self.resize(600, 600)
        self.setAcceptDrops(True)

        # setting the necessary labels 
        self.label = QLabel("SIMILAR FACE FINDER")
        self.percentage = QLabel("")

        # Set the font style for the label
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.label.setFont(font)
        self.percentage.setFont(font)
        mainLayout = QVBoxLayout()
        self.photoViewer = ImageLabel()

        #putting the elements in layouts
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.percentage)
        mainLayout.addWidget(self.photoViewer)
        self.setLayout(mainLayout)

    def dragEnterEvent(self, event):

        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):

        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()

            self.set_image(file_path)
            answer = predict(file_path)
            self.label.setText(answer)

            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))