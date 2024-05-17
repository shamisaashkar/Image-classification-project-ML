### main
from PyQt5.QtWidgets import QApplication
import predictor as pred
import UI as ui 
import sys

# load the pickle files
app = QApplication(sys.argv)
demo = ui.AppDemo()
demo.show()
sys.exit(app.exec_())