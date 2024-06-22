from PySide2.QtWidgets import *
from  maya.OpenMayaUI import MQtUtil
from shiboken2 import wrapInstance
from importlib import reload
import Stylized_MotionBlur.Deform_UI as deform
import Stylized_MotionBlur.Multiples_UI as multiples
import Stylized_MotionBlur.MultipleShapes_UI as ms
import Stylized_MotionBlur.ShapeTrails_UI as st
import Stylized_MotionBlur.MotionTrails_UI as mt


maya_win = wrapInstance(int(MQtUtil.mainWindow()), QWidget)

class MyWin(QMainWindow):
    instance = None
    def __init__(self):
        if MyWin.instance is not None:
            MyWin.instance.close()
        MyWin.instance = self
        super().__init__(parent=maya_win)
        self.setWindowTitle("Stylized Motion Blur")
        self.setGeometry(200, 200, 350, 220) 
        self._create_widgets()
        self._create_layout()
        self._connect_widgets()
        self.show()
    
    def _create_widgets(self):
        self.my_label = QLabel("Choose your desired Motion Blur.")
        self.deform_button = QPushButton("Smearframes")
        self.deform_button.resize(400, 100)
        self.multiples_button = QPushButton("Multiples")
        self.multipleShapes_button = QPushButton("Multiple Shapes")
        self.shapeTrails_button = QPushButton("Shape Trails")
        self.motionTrails_button = QPushButton("Motion Trails")

    def _create_layout(self):
        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.my_label)
        vbox.addWidget(self.deform_button)
        vbox.addWidget(self.multiples_button)
        vbox.addWidget(self.multipleShapes_button)
        vbox.addWidget(self.shapeTrails_button)
        vbox.addWidget(self.motionTrails_button)
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)
    
    def _connect_widgets(self):
        self.deform_button.clicked.connect(self._create_deform)
        self.multiples_button.clicked.connect(self._create_multiples)
        self.multipleShapes_button.clicked.connect(self._create_ms)
        self.shapeTrails_button.clicked.connect(self._create_st)
        self.motionTrails_button.clicked.connect(self._create_mt)

    def _create_deform(self):
        reload(deform)
        deform.apply()

    def _create_multiples(self):
        reload(multiples)
        multiples.apply()
    
    def _create_ms(self):
        reload(ms)
        ms.apply()

    def _create_st(self):
        reload(st)
        st.apply()

    def _create_mt(self):
        reload(mt)
        mt.apply()

def apply():
    MyWin()