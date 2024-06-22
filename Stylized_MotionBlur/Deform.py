import pymel.core as pm
from Stylized_MotionBlur import CreateCache

START_FRAME = int(pm.playbackOptions(query=True, minTime=True))
END_FRAME = int(pm.playbackOptions(query=True, maxTime=True))
DNT_grp = []  

class Deform:

    def __init__(self, sl_faces):
        self.sl_faces = sl_faces
        self.obj_shape = pm.listRelatives(self.sl_faces[0],p=True)[0]
        self.cache_creator = CreateCache.Create_Cache(self.sl_faces, self.obj_shape, START_FRAME, END_FRAME)
        self.cache = self.cache_creator.cache
        DNT_grp.append(self.cache_creator.DNT_ls)
        self.bifrost_shape = self._createBifrostGraph()
        self._create_bg_input(self.obj_shape, self.cache, self.bifrost_shape)
        self._set_default_attributes(self.bifrost_shape)
        self._connect_deform_node(self.bifrost_shape)
        self.output = self._createOutputMesh(self.obj_shape, self.bifrost_shape)
        self.DNT_deform_grp = self._create_DNT_grp(DNT_grp)
        pm.delete(self.cache_creator.duplicate)

    def _createBifrostGraph(self):
        
        bifrost_shape = pm.createNode("bifrostGraphShape")
        pm.addAttr(longName='Stylized_MotionBlur', dt='string', h=True)
        pm.setAttr(bifrost_shape + ".Stylized_MotionBlur", "Deform")
        pm.rename(bifrost_shape, "Deform_bifrost_shape")
        bifrost_graph = bifrost_shape.getParent()
        bifrost_graph.rename("Deform_bifrost_graph")
        DNT_grp.append(bifrost_graph)

        return bifrost_shape

    def _create_bg_input(self, obj_shape, cache, bifrost_shape):

        cache_shape = cache.getShape()
        fixed_text = "setOperation=+;active=true;channels=*;normalsPerFaceVertex=true;normalsPerPoint=true;normalsPerFace=false"
        mesh_port_options = f"pathinfo={{path=/{obj_shape.name(long=True)};{fixed_text}}}"
        cache_port_options = f"pathinfo={{path=/{cache_shape.name(long=True)};{fixed_text}}}"

        pm.vnnNode(bifrost_shape , "/input", createOutputPort=["mesh", "Object"], portOptions=mesh_port_options)
        pm.vnnNode(bifrost_shape , "/input", createOutputPort=["duplicate_mesh", "Object"], portOptions=cache_port_options)
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["min", "float"])
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["max", "float"])
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["random_seed", "int"])
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["speed_line_smears", "bool"])
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["rhythm", "bool"])

    def _set_default_attributes(self, bifrost_shape):

        pm.setAttr(bifrost_shape + ".min", 0.01)
        pm.setAttr(bifrost_shape + ".max", 0.03)
        pm.setAttr(bifrost_shape + ".random_seed", 234)
        pm.setAttr(bifrost_shape + ".speed_line_smears", 0)
        pm.setAttr(bifrost_shape + ".rhythm", 0)

    def _connect_deform_node(self, bifrost_shape):
        
        pm.vnnCompound( bifrost_shape, "/", addNode = "BifrostGraph,User::Compounds,deform")
        pm.vnnConnect( bifrost_shape, ".mesh", "/deform.in_mesh")
        pm.vnnConnect( bifrost_shape, ".duplicate_mesh", "/deform.duplicate_mesh")
        pm.vnnNode( bifrost_shape, "/output", createInputPort = ["out_mesh", "Object"])
        pm.vnnConnect( bifrost_shape, "/deform.out_mesh", ".out_mesh")
        pm.vnnConnect(bifrost_shape, ".min", "/deform.min")
        pm.vnnConnect(bifrost_shape, ".max", "/deform.max")
        pm.vnnConnect(bifrost_shape, ".random_seed", "/deform.random_seed")
        pm.vnnConnect(bifrost_shape, ".speed_line_smears", "/deform.speed_line_smears")
        pm.vnnConnect(bifrost_shape, ".rhythm", "/deform.rhythm")
        
    def _createOutputMesh(self, obj_shape, bifrost_shape):

        obj = obj_shape.getParent()
        pm.setAttr(obj + ".visibility", 0)
        output_transform, _ = pm.polyCube( sx=1, sy=1, sz=1, h=1, n=obj.name() + "_Deform" )
        output_shape = output_transform.getShape()
        pm.delete(output_transform, constructionHistory=True)
        bifrostToMayaNode = pm.createNode("bifrostGeoToMaya")
        bifrost_shape.out_mesh >> bifrostToMayaNode.bifrostGeo
        bifrostToMayaNode.mayaMesh[0] >> output_shape.inMesh

        return output_transform

    def _create_DNT_grp(self, objects):

        if pm.objExists('DNT_MotionBlur'):
            DNT_deform_grp = pm.group(objects, n="DNT_Deform")
            pm.parent(DNT_deform_grp, 'DNT_MotionBlur')
        else:
            DNT_deform_grp = pm.group(objects, n="DNT_Deform")
            DNT_MB_grp = pm.group(DNT_deform_grp, n='DNT_MotionBlur' )
            pm.setAttr(DNT_MB_grp.visibility, 0)

        return DNT_deform_grp

    def kill(self):
        obj = self.obj_shape.getParent()
        pm.setAttr(obj + ".visibility", 1)
        DNT_MB_grp = self.DNT_deform_grp.getParent()
        pm.delete(self.DNT_deform_grp)
        pm.delete(self.output)
        self.cache_creator.kill()
        DNT_obj = pm.listRelatives(DNT_MB_grp, c = True)
        if not DNT_obj:
            pm.delete(DNT_MB_grp)

  
    
 
    