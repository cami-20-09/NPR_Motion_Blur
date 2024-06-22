import pymel.core as pm
import maya.cmds as mc
from Stylized_MotionBlur import CreateCache

START_FRAME = int(pm.playbackOptions(query=True, minTime=True))
END_FRAME = int(pm.playbackOptions(query=True, maxTime=True))
DNT_grp = []  

class MultipleShapes:

    def __init__(self, sl_faces):
        self.sl_faces = sl_faces
        self.obj_shape = pm.listRelatives(self.sl_faces[0],p=True)[0]
        self.cache_creator = CreateCache.Create_Cache(self.sl_faces, self.obj_shape, START_FRAME, END_FRAME)
        self.cache = self.cache_creator.cache
        self.instance_paths = self._create_snapshot(self.cache)
        self.bifrost_shape = self._create_bifrost_graph()
        self._create_bg_input(self.obj_shape, self.instance_paths, self.bifrost_shape)
        self._set_default_attributes(self.bifrost_shape)
        self._connect_MS_node(self.bifrost_shape)
        self.output = self._createOutputMesh(self.obj_shape, self.bifrost_shape)
        self.DNT_MS_grp = self._create_DNT_grp(DNT_grp)
        pm.delete(self.cache_creator.DNT_ls)

    def _create_snapshot(self, obj):

        pm.select(obj)
        snapshot_grp = pm.snapshot(increment=1, constructionHistory=1, startTime=START_FRAME, endTime=END_FRAME, update="animCurve")[0]
        DNT_grp.append(snapshot_grp)
        instances = pm.listRelatives(snapshot_grp, c=True)
        instance_paths = ""

        for i in instances:
                mc.componentTag([ str(i) + '.f[*]'], cr=True, ntn='all')
                instance_attr = ("", i.getParent().name(), str(i), i.getShape().name())
                instance_attr_joined = "/".join(instance_attr) + " "
                instance_paths += instance_attr_joined

        return instance_paths      

    def _create_bifrost_graph(self, ):

        bifrost_shape = pm.createNode("bifrostGraphShape")
        pm.addAttr(longName='Stylized_MotionBlur', dt='string', h=True)
        pm.setAttr(bifrost_shape + ".Stylized_MotionBlur", "MultipleShapes")
        pm.rename(bifrost_shape, "MS_bifrost_shape")
        bifrost_graph = bifrost_shape.getParent()
        bifrost_graph.rename("MS_bifrost_graph")
        DNT_grp.append(bifrost_graph)

        return bifrost_shape

    def _create_bg_input(self, obj_shape, instance_paths, bifrost_shape):

        fixed_text = "setOperation=+;active=true;channels=*;normalsPerFaceVertex=true;normalsPerPoint=true;normalsPerFace=false"
        snapshot_port_options = f"pathinfo={{path=/{instance_paths};{fixed_text}}}"
        mesh_port_options = f"pathinfo={{path=/{obj_shape.name(long=True)};{fixed_text}}}"
        pm.vnnNode(bifrost_shape , "/input", createOutputPort=["mesh", "Object"], portOptions=mesh_port_options)
        pm.vnnNode(bifrost_shape , "/input", createOutputPort=["snapshot_meshes", "array<Object>"], portOptions=snapshot_port_options)
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["thickness", "float"])
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["count", "int"])
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["velocity_influence", "bool"])
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["velocity_factor", "float"])

    def _connect_MS_node(self, bifrost_shape):

        pm.vnnCompound(bifrost_shape, "/", addNode = "BifrostGraph,User::Compounds,multiple_shape")
        pm.vnnConnect(bifrost_shape, ".snapshot_meshes", "/multiple_shape.snapshot_meshes")
        pm.vnnConnect(bifrost_shape, ".mesh", "/multiple_shape.in_mesh")
        pm.vnnNode(bifrost_shape, "/output", createInputPort = ["out_mesh", "Object"])
        pm.vnnConnect(bifrost_shape, "/multiple_shape.out_mesh", ".out_mesh")
        pm.vnnCompound(bifrost_shape, "/multiple_shape", setIsReferenced = False)

        pm.vnnConnect(bifrost_shape, ".thickness", "/multiple_shape.thickness")
        pm.vnnConnect(bifrost_shape, ".count", "/multiple_shape.count")
        pm.vnnConnect(bifrost_shape, ".velocity_influence", "/multiple_shape.velocity_influence")
        pm.vnnConnect(bifrost_shape, ".velocity_factor", "/multiple_shape.velocity_factor")

    def _set_default_attributes(self, bifrost_shape):

        pm.setAttr(bifrost_shape + ".thickness", 0.2)
        pm.setAttr(bifrost_shape + ".count", 3)
        pm.setAttr(bifrost_shape + ".velocity_influence", 0)
        pm.setAttr(bifrost_shape + ".velocity_factor", 0.5)

    def _createOutputMesh(self, obj_shape, bifrost_shape):

        obj = obj_shape.getParent()
        output_transform, _ = pm.polyCube( sx=1, sy=1, sz=1, h=1, n=obj.name() + "_Multiple_shape" )
        output_shape = output_transform.getShape()
        pm.delete(output_transform, constructionHistory=True)
        bifrostToMayaNode = pm.createNode("bifrostGeoToMaya")
        bifrost_shape.out_mesh >> bifrostToMayaNode.bifrostGeo
        bifrostToMayaNode.mayaMesh[0] >> output_shape.inMesh

        return output_transform

    def _create_DNT_grp(self, objects):

        if pm.objExists('DNT_MotionBlur'):
            DNT_MS_grp = pm.group(objects, n="DNT_MultipleShapes")
            pm.parent(DNT_MS_grp, 'DNT_MotionBlur')
        else:
            DNT_MS_grp = pm.group(objects, n="DNT_MultipleShapes")
            DNT_MB_grp = pm.group(DNT_MS_grp, n='DNT_MotionBlur' )
            pm.setAttr(DNT_MB_grp.visibility, 0)

        return DNT_MS_grp
    
    def kill(self):
        DNT_MB_grp = self.DNT_MS_grp.getParent()
        pm.delete(self.DNT_MS_grp)
        pm.delete(self.output)
        self.cache_creator.kill()
        DNT_obj = pm.listRelatives(DNT_MB_grp, c = True)
        if not DNT_obj:
            pm.delete(DNT_MB_grp)

    



