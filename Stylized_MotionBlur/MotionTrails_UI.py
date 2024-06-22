from PySide2.QtWidgets import *
from PySide2.QtCore import Qt 
from  maya.OpenMayaUI import MQtUtil
from shiboken2 import wrapInstance
import pymel.core as pm
import importlib
import Stylized_MotionBlur.MotionTrails as MT

maya_win = wrapInstance(int(MQtUtil.mainWindow()), QWidget)

class MyWin(QMainWindow):

    def __init__(self):
        MyWin.instance = self
        super().__init__(parent=maya_win)
        self.setWindowTitle("Motion Trails")
        self.setGeometry(200, 200, 350, 250) 
        self._create_widgets()
        self._create_layout()
        self._connect_widgets()
        self.show()
    
    def _create_widgets(self):
        self.apply_label = QLabel("Please select requested Edges.")
        self.apply_label.resize(200, 100)
        self.apply_button = QPushButton("Create Motion Trails")
        self.length_layout = Create_attribute_layout("Length", 0, 10)
        self.velocity_button = QCheckBox("Velocity Influence")
        self.velocity_layout = Create_attribute_layout("Velocity Factor", 0, 100)
        self.style_box = QComboBox()
        self.style_label = QLabel("Style:")
        self.style_label.resize(200, 100)
        self.style_box.addItems(["1", "2", "3", "4"])
        self.transparency_layout = Create_attribute_layout("Transparency", 0, 99)
        self.kill_button = QPushButton("Delete Motion Trails")
        self.select_message = QMessageBox()
        self.select_message.setText("Please select requested Edges first.")
        self.edges_message = QMessageBox()
        self.edges_message.setText("Please make sure to only select Polyedges.")

    def _create_layout(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.apply_label)
        vbox.addWidget(self.apply_button)
        vbox.addLayout(self.length_layout.hlayout)
        vbox.addWidget(self.velocity_button)
        vbox.addLayout(self.velocity_layout.hlayout)
        vbox.addWidget(self.style_label)
        vbox.addWidget(self.style_box)
        vbox.addLayout(self.transparency_layout.hlayout)
        vbox.addWidget(self.kill_button)
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)
    
    def _connect_widgets(self):
        self.apply_button.clicked.connect(self._create)
        self.length_layout.slider.valueChanged.connect(self._set_length_value)
        self.velocity_button.stateChanged.connect(self._set_velocity_influence)
        self.velocity_layout.slider.valueChanged.connect(self._set_velocity_value)
        self.style_box.currentTextChanged.connect(self._set_style)
        self.transparency_layout.slider.valueChanged.connect(self._set_transparency)
        self.kill_button.clicked.connect(self._kill)
        
    def _create(self):
        sl_edges = pm.ls(sl=True)
        if len(sl_edges) == 0: 
            self.select_message.exec_()
            return None
        else:
            for e in sl_edges:
                if not isinstance(e, pm.MeshEdge):
                    self.edges_message.exec_()
                    return None
        self.MT = MT.MotionTrails(sl_edges)

    def _set_length_value(self):
        pm.setAttr(self.MT.bifrost_shape + ".length", int(self.length_layout.slider.value()))
        self.length_layout.lineedit.setText(str(self.length_layout.slider.value()))

    def _set_velocity_influence(self):
        if self.velocity_button.isChecked():
            pm.setAttr(self.MT.bifrost_shape + ".velocity_influence", 1)
        else:
            pm.setAttr(self.MT.bifrost_shape + ".velocity_influence", 0)

    def _set_velocity_value(self):
        v_value = int(self.velocity_layout.slider.value()) / 100
        pm.setAttr(self.MT.bifrost_shape + ".velocity_factor", v_value)
        self.velocity_layout.lineedit.setText(str(self.velocity_layout.slider.value()))

    def _set_style(self, style_idx):
        texture_node = self.MT.surfaceShader.texture
        MT_file_path = self.MT.surfaceShader.MT_file_path + style_idx + ".png"
        pm.setAttr(texture_node + '.fileTextureName', MT_file_path, type='string')

    def _set_transparency(self):
        transparency_ramp = self.MT.surfaceShader.transparency
        t_value = int(self.transparency_layout.slider.value()) / 100
        pm.setAttr(transparency_ramp + ".colorEntryList[1].position", t_value)
        self.transparency_layout.lineedit.setText(str(self.transparency_layout.slider.value()))

    def _kill(self):
        self.MT.kill()

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
    importlib.reload(MT)
    MyWin()


