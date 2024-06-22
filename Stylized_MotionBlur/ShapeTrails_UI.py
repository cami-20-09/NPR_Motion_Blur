from PySide2.QtWidgets import *
from PySide2.QtCore import Qt 
from  maya.OpenMayaUI import MQtUtil
from shiboken2 import wrapInstance
import pymel.core as pm
import random
import importlib
import Stylized_MotionBlur.ShapeTrails as st

maya_win = wrapInstance(int(MQtUtil.mainWindow()), QWidget)

class MyWin(QMainWindow):

    def __init__(self):
        MyWin.instance = self
        super().__init__(parent=maya_win)
        self.setWindowTitle("Shape Trails")
        self.setGeometry(200, 200, 350, 400) 
        self.setMaximumHeight(400)
        self.setMaximumWidth(400)
        self._create_widgets()
        self._create_layout()
        self._connect_widgets()
        self.show()
    
    def _create_widgets(self):
        self.apply_label = QLabel("Please select requested Faces.")
        self.apply_label.resize(200, 100)
        self.apply_button = QPushButton("Create Shape Trails")
        self.tail_layout = Create_attribute_layout("Tail", 0, 20)
        self.head_layout = Create_attribute_layout("Head", 0, 20)
        self.strandCount_layout = Create_attribute_layout("Strand Count", 0, 10)
        self.sides_layout = Create_attribute_layout("Sides", 3, 10)
        self.size_layout = Create_attribute_layout("Size", 0, 20)
        self.divisions_layout = Create_attribute_layout("Divisions", 0, 10)
        self.strands_button = QCheckBox("Strands")
        self.strandsSize_layout = Create_attribute_layout("Strands Size", 0, 100)
        self.velocity_button = QCheckBox("Velocity Influence")
        self.velocity_layout = Create_attribute_layout("Velocity Factor", 0, 100)
        self.rand_button = QPushButton("New Trails")
        self.kill_button = QPushButton("Delete Shape Trails")
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
        vbox.addLayout(self.tail_layout.hlayout)
        vbox.addLayout(self.head_layout.hlayout)
        vbox.addLayout(self.strandCount_layout.hlayout)
        vbox.addLayout(self.sides_layout.hlayout)
        vbox.addLayout(self.size_layout.hlayout)
        vbox.addLayout(self.divisions_layout.hlayout)
        vbox.addWidget(self.strands_button)
        vbox.addLayout(self.strandsSize_layout.hlayout)
        vbox.addWidget(self.velocity_button)
        vbox.addLayout(self.velocity_layout.hlayout)
        vbox.addWidget(self.rand_button)
        vbox.addWidget(self.kill_button)
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)
    
    def _connect_widgets(self):
        self.apply_button.clicked.connect(self._create)
        self.tail_layout.slider.valueChanged.connect(self._set_tail_value)
        self.head_layout.slider.valueChanged.connect(self._set_head_value)
        self.strandCount_layout.slider.valueChanged.connect(self._set_strandCount_value)
        self.sides_layout.slider.valueChanged.connect(self._set_sides_value)
        self.size_layout.slider.valueChanged.connect(self._set_size_value)
        self.divisions_layout.slider.valueChanged.connect(self._set_divisions_value)
        self.strands_button.stateChanged.connect(self._set_strands)
        self.strandsSize_layout.slider.valueChanged.connect(self._set_strandsSize_value)
        self.velocity_button.stateChanged.connect(self._set_velocity_influence)
        self.velocity_layout.slider.valueChanged.connect(self._set_velocity_value)
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
        self.ST = st.ShapeTrails(sl_faces)
        vtx_number = self.ST.vtx_number
        if vtx_number > 30:
            self.strandCount_layout.slider.setMaximum(30)
        else:
            self.strandCount_layout.slider.setMaximum(vtx_number)

    def _set_tail_value(self):
        pm.setAttr(self.ST.bifrost_shape + ".tail", int(self.tail_layout.slider.value()))
        self.tail_layout.lineedit.setText(str(self.tail_layout.slider.value()))

    def _set_head_value(self):
        pm.setAttr(self.ST.bifrost_shape + ".head", int(self.head_layout.slider.value()))
        self.head_layout.lineedit.setText(str(self.head_layout.slider.value()))

    def _set_strandCount_value(self):
        pm.setAttr(self.ST.bifrost_shape + ".strand_count", int(self.strandCount_layout.slider.value()))
        self.strandCount_layout.lineedit.setText(str(self.strandCount_layout.slider.value()))

    def _set_sides_value(self):
        pm.setAttr(self.ST.bifrost_shape + ".sides", int(self.sides_layout.slider.value()))
        self.sides_layout.lineedit.setText(str(self.sides_layout.slider.value()))

    def _set_size_value(self):
        size = int(self.size_layout.slider.value()) / 10
        pm.setAttr(self.ST.bifrost_shape + ".size", size)
        self.size_layout.lineedit.setText(str(self.size_layout.slider.value()))

    def _set_divisions_value(self):
        pm.setAttr(self.ST.bifrost_shape + ".divisions", int(self.divisions_layout.slider.value()))
        self.divisions_layout.lineedit.setText(str(self.divisions_layout.slider.value()))

    def _set_strands(self):
        if self.strands_button.isChecked():
            pm.setAttr(self.ST.bifrost_shape.getParent() + ".visibility", 1)
        else:
            pm.setAttr(self.ST.bifrost_shape.getParent() + ".visibility", 0)

    def _set_strandsSize_value(self):
        size = int(self.strandsSize_layout.slider.value()) / 1000
        pm.setAttr(self.ST.bifrost_shape + ".strands_size", size)
        self.strandsSize_layout.lineedit.setText(str(self.strandsSize_layout.slider.value()))

    def _set_velocity_influence(self):
        if self.velocity_button.isChecked():
            pm.setAttr(self.ST.bifrost_shape + ".velocity_influence", 1)
        else:
            pm.setAttr(self.ST.bifrost_shape + ".velocity_influence", 0)

    def _set_velocity_value(self):
        v_value = int(self.velocity_layout.slider.value()) / 100
        pm.setAttr(self.ST.bifrost_shape + ".velocity_factor", v_value)
        self.velocity_layout.lineedit.setText(str(self.velocity_layout.slider.value()))

    def _set_random(self):
        rand = random.randint(1, 500)
        pm.setAttr(self.ST.bifrost_shape + ".random_seed", rand)

    def _kill(self):
        self.ST.kill()


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
    importlib.reload(st)
    MyWin()