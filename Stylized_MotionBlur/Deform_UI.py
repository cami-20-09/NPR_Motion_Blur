from PySide2.QtWidgets import *
from PySide2.QtCore import Qt 
from  maya.OpenMayaUI import MQtUtil
from shiboken2 import wrapInstance
import pymel.core as pm
import random
import importlib
from Stylized_MotionBlur import Deform 

maya_win = wrapInstance(int(MQtUtil.mainWindow()), QWidget)

class MyWin(QMainWindow):

    def __init__(self):
        MyWin.instance = self
        super().__init__(parent=maya_win)
        self.setWindowTitle("Deformation")
        self.setGeometry(250, 250, 350, 250) 
        self._create_widgets()
        self._create_layout()
        self._connect_widgets()
        self.show()
    
    def _create_widgets(self):
        self.apply_label = QLabel("Please select requested Faces.")
        self.apply_label.resize(200, 100)
        self.apply_button = QPushButton("Create Smearframes")
        self.min_layout = Create_attribute_layout("Min", 0, 10)
        self.max_layout = Create_attribute_layout("Max", 0, 10)
        self.speedLine_button = QCheckBox("Speed Line Smears")
        self.rhythm_button = QCheckBox("Rhythm")
        self.rand_button = QPushButton("Change Deform Order")
        self.kill_button = QPushButton("Delete Smearframes")
        self.safe_message = QMessageBox()
        self.safe_message.setText("Please safe your scene first.")
        self.select_message = QMessageBox()
        self.select_message.setText("Please select requested Faces first.")
        self.edges_message = QMessageBox()
        self.edges_message.setText("Please make sure to only select Polyfaces.")

    def _create_layout(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.apply_label)
        vbox.addWidget(self.apply_button)
        vbox.addLayout(self.min_layout.hlayout)
        vbox.addLayout(self.max_layout.hlayout)
        vbox.addWidget(self.speedLine_button)
        vbox.addWidget(self.rhythm_button)
        vbox.addWidget(self.rand_button)
        vbox.addWidget(self.kill_button)
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)
    
    def _connect_widgets(self):
        self.apply_button.clicked.connect(self._create)
        self.min_layout.slider.valueChanged.connect(self._set_min_value)
        self.max_layout.slider.valueChanged.connect(self._set_max_value)
        self.speedLine_button.stateChanged.connect(self._set_speedLine)
        self.rhythm_button.stateChanged.connect(self._set_rhythm)
        self.rand_button.clicked.connect(self._set_random)
        self.kill_button.clicked.connect(self._kill)
        
    def _create(self):
        sl_faces = pm.ls(sl=True)
        scene_path = pm.system.sceneName()
        if scene_path == "":
            self.safe_message.exec_()
            return None
        elif len(sl_faces) == 0: 
            self.select_message.exec_()
            return None
        else:
            for e in sl_faces:
                if not isinstance(e, pm.MeshFace):
                    self.edges_message.exec_()
                    return None
        self.Deform = Deform.Deform(sl_faces)

    def _set_min_value(self):
        min = int(self.min_layout.slider.value()) / 50
        pm.setAttr(self.Deform.bifrost_shape + ".min", min)
        self.min_layout.lineedit.setText(str(self.min_layout.slider.value()))

    def _set_max_value(self):
        max = int(self.max_layout.slider.value()) / 50
        pm.setAttr(self.Deform.bifrost_shape + ".max", max)
        self.max_layout.lineedit.setText(str(self.max_layout.slider.value()))

    def _set_speedLine(self):
        if self.speedLine_button.isChecked():
            pm.setAttr(self.Deform.bifrost_shape.getParent() + ".speed_line_smears", 1)
        else:
            pm.setAttr(self.Deform.bifrost_shape.getParent() + ".speed_line_smears", 0)

    def _set_rhythm(self):
        if self.rhythm_button.isChecked():
            pm.setAttr(self.Deform.bifrost_shape + ".rhythm", 1)
        else:
            pm.setAttr(self.Deform.bifrost_shape + ".rhythm", 0)

    def _set_random(self):
        rand = random.randint(1, 500)
        pm.setAttr(self.Deform.bifrost_shape + ".random_seed", rand)

    def _kill(self):
        self.Deform.kill()


class Create_attribute_layout():
        
    def __init__(self, attr, min, max):
        self.hlayout = QHBoxLayout()
        self.label = QLabel(attr)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.lineedit = QLineEdit()
        self.lineedit.setReadOnly(True)
        self.lineedit.setFixedWidth(60)
        self.hlayout.addWidget(self.label)
        self.hlayout.addWidget(self.slider)
        self.hlayout.addWidget(self.lineedit)

def apply():
    importlib.reload(Deform)
    MyWin()