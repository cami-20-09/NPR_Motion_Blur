import pymel.core as pm
from Stylized_MotionBlur import CreateCache

START_FRAME = int(pm.playbackOptions(query=True, minTime=True))
END_FRAME = int(pm.playbackOptions(query=True, maxTime=True))
DNT_grp = []  

class Multiples:

    def __init__(self, sl_faces):
        self.sl_faces = sl_faces
        self.obj_shape = pm.listRelatives(sl_faces[0],p=True)[0]
        self.cache_creator = CreateCache.Create_Cache(sl_faces, self.obj_shape, START_FRAME, END_FRAME)
        self.multiple_path = self.cache_creator.cachePath
        self.bifrost_shape = self._createBifrostGraph()
        self._create_bg_input(self.obj_shape, self.bifrost_shape)
        self._connect_multiples_node(self.bifrost_shape, self.multiple_path)
        self._set_default_attributes(self.bifrost_shape)
        self.output = self._createOutputMesh(self.obj_shape, self.bifrost_shape)
        self.DNT_multiples_grp = self._create_DNT_grp(DNT_grp)
        pm.delete(self.cache_creator.DNT_ls)

    def _createBifrostGraph(self):
        
        bifrost_shape = pm.createNode("bifrostGraphShape")
        pm.addAttr(longName='Stylized_MotionBlur', dt='string', h=True)
        pm.setAttr(bifrost_shape + ".Stylized_MotionBlur", "Multiples")
        pm.rename(bifrost_shape, "Multiples_bifrost_shape")
        bifrost_graph = bifrost_shape.getParent()
        bifrost_graph.rename("Multiples_bifrost_graph")
        DNT_grp.append(bifrost_graph)

        return bifrost_shape

    def _create_bg_input(self, obj_shape, bifrost_shape):

        fixed_text = "setOperation=+;active=true;channels=*;normalsPerFaceVertex=true;normalsPerPoint=true;normalsPerFace=false"
        port_options = f"pathinfo={{path=/{obj_shape.name(long=True)};{fixed_text}}}"
        pm.vnnNode(bifrost_shape , "/input", createOutputPort=["mesh", "Object"], portOptions=port_options)
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["count", "int"])
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["distance", "float"])
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["velocity_influence", "bool"])
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["velocity_factor", "float"])


    def _connect_multiples_node(self, bifrost_shape, multiple_path):
        
        pm.vnnCompound(bifrost_shape, "/", addNode = "BifrostGraph,User::Compounds,multiples")
        pm.vnnCompound(bifrost_shape, "/multiples", setIsReferenced=False)
        pm.vnnNode(bifrost_shape, "/multiples/value2", setPortDefaultValues=["value", multiple_path])
        pm.vnnNode(bifrost_shape, "/output", createInputPort = ["out_mesh", "Object"])
        pm.vnnConnect(bifrost_shape, ".mesh", "/multiples.in_mesh")
        pm.vnnConnect(bifrost_shape, "/multiples.out_mesh", ".out_mesh")
        pm.vnnConnect(bifrost_shape, ".count", "/multiples.count")
        pm.vnnConnect(bifrost_shape, ".distance", "/multiples.distance")
        pm.vnnConnect(bifrost_shape, ".velocity_influence", "/multiples.velocity_influence")
        pm.vnnConnect(bifrost_shape, ".velocity_factor", "/multiples.velocity_factor")

    def _set_default_attributes(self, bifrost_shape):

        pm.setAttr(bifrost_shape + ".count", 2)
        pm.setAttr(bifrost_shape + ".distance", 1.5)
        pm.setAttr(bifrost_shape + ".velocity_influence", 0)
        pm.setAttr(bifrost_shape + ".velocity_factor", 0.5)
        
    def _createOutputMesh(self, obj_shape, bifrost_shape):

        obj = obj_shape.getParent()
        output_transform, _ = pm.polyCube( sx=1, sy=1, sz=1, h=1, n=obj.name() + "_Multiples" )
        output_shape = output_transform.getShape()
        pm.delete(output_transform, constructionHistory=True)
        bifrostToMayaNode = pm.createNode("bifrostGeoToMaya")
        bifrost_shape.out_mesh >> bifrostToMayaNode.bifrostGeo
        bifrostToMayaNode.mayaMesh[0] >> output_shape.inMesh

        return output_transform

    def _create_DNT_grp(self, objects):

        if pm.objExists('DNT_MotionBlur'):
            DNT_multiples_grp = pm.group(objects, n="DNT_Multiples")
            pm.parent(DNT_multiples_grp, 'DNT_MotionBlur')
        else:
            DNT_multiples_grp = pm.group(objects, n="DNT_Multiples")
            DNT_MB_grp = pm.group(DNT_multiples_grp, n='DNT_MotionBlur' )
            pm.setAttr(DNT_MB_grp.visibility, 0)

        return DNT_multiples_grp
    
    def kill(self):
        DNT_MB_grp = self.DNT_multiples_grp.getParent()
        pm.delete(self.DNT_multiples_grp)
        pm.delete(self.output)
        self.cache_creator.kill()
        DNT_obj = pm.listRelatives(DNT_MB_grp, c = True)
        if not DNT_obj:
            pm.delete(DNT_MB_grp)
        


    