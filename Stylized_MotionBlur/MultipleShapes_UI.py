from PySide2.QtWidgets import *
from PySide2.QtCore import Qt 
from  maya.OpenMayaUI import MQtUtil
from shiboken2 import wrapInstance
import pymel.core as pm
import importlib
import Stylized_MotionBlur.MultipleShapes as MS

maya_win = wrapInstance(int(MQtUtil.mainWindow()), QWidget)

class MyWin(QMainWindow):
    #instance = None
    def __init__(self):
        #if MyWin.instance is not None:
            #MyWin.instance.close()
        MyWin.instance = self
        super().__init__(parent=maya_win)
        self.setWindowTitle("Multiple Shapes")
        self.setGeometry(250, 250, 350, 250) 
        self._create_widgets()
        self._create_layout()
        self._connect_widgets()
        self.show()
    
    def _create_widgets(self):
        self.apply_label = QLabel("Please select requested Faces.")
        self.apply_label.resize(200, 100)
        self.apply_button = QPushButton("Create Multiple Shapes")
        self.thickness_layout = Create_attribute_layout("Thickness", 0, 10)
        self.count_layout = Create_attribute_layout("Count", 0, 10)
        self.velocity_button = QCheckBox("Velocity Influence")
        self.velocity_layout = Create_attribute_layout("Velocity Factor", 0, 100)
        self.kill_button = QPushButton("Delete Multiple Shapes")
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
        vbox.addLayout(self.thickness_layout.hlayout)
        vbox.addLayout(self.count_layout.hlayout)
        vbox.addWidget(self.velocity_button)
        vbox.addLayout(self.velocity_layout.hlayout)
        vbox.addWidget(self.kill_button)
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)
    
    def _connect_widgets(self):
        self.apply_button.clicked.connect(self._create)
        self.thickness_layout.slider.valueChanged.connect(self._set_thickness_value)
        self.count_layout.slider.valueChanged.connect(self._set_count_value)
        self.velocity_button.stateChanged.connect(self._set_velocity_influence)
        self.velocity_layout.slider.valueChanged.connect(self._set_velocity_value)
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
        self.MS = MS.MultipleShapes(sl_faces)

    def _set_thickness_value(self):
        thickness = int(self.thickness_layout.slider.value()) / 50
        pm.setAttr(self.MS.bifrost_shape + ".thickness", thickness)
        self.thickness_layout.lineedit.setText(str(self.thickness_layout.slider.value()))

    def _set_count_value(self):
        pm.setAttr(self.MS.bifrost_shape + ".count", int(self.count_layout.slider.value()))
        self.count_layout.lineedit.setText(str(self.count_layout.slider.value()))

    def _set_velocity_influence(self):
        if self.velocity_button.isChecked():
            pm.setAttr(self.MS.bifrost_shape + ".velocity_influence", 1)
        else:
            pm.setAttr(self.MS.bifrost_shape + ".velocity_influence", 0)

    def _set_velocity_value(self):
        v_value = int(self.velocity_layout.slider.value()) / 100
        pm.setAttr(self.MS.bifrost_shape + ".velocity_factor", v_value)
        self.velocity_layout.lineedit.setText(str(self.velocity_layout.slider.value()))

    def _kill(self):
        self.MS.kill()


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
    importlib.reload(MS)
    MyWin()