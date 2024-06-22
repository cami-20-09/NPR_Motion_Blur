import pymel.core as pm
import os

START_FRAME = int(pm.playbackOptions(query=True, minTime=True))
END_FRAME = int(pm.playbackOptions(query=True, maxTime=True))
DNT_grp = []  

class MotionTrails: 

    def __init__(self, sl_edges):
        self.sl_edges = sl_edges
        self.obj_shape = pm.listRelatives(self.sl_edges[0],p=True)[0]
        self.instance_paths = self._create_snapshot(self.obj_shape)
        self.bifrost_shape = self._create_Bifrost_Graph()
        self._create_bg_input(self.obj_shape, self.instance_paths, self.bifrost_shape)
        self._set_default_attributes(self.bifrost_shape)
        self._connect_MT_node(self.bifrost_shape)
        self.DNT_MT_grp = self._create_DNT_grp(DNT_grp)
        self.output = self._createOutputMesh(self.obj_shape, self.bifrost_shape)
        self.surfaceShader = SurfaceShader()
        self._assign_shader(self.output, self.surfaceShader.shadingEngine)

    def _create_snapshot(self, obj_shape):

        obj = obj_shape.getParent()
        obj_curve = pm.polyToCurve(form=2, degree=3, conformToSmoothMeshPreview=1, n=obj.name() + "_curve")
        snapshot_grp_name = obj.name() + "_snapshot"
        pm.select(obj_curve)
        snapshot_grp = pm.snapshot(increment=1, constructionHistory=1, startTime=START_FRAME, endTime=END_FRAME, update="animCurve", n=snapshot_grp_name)[0]
        DNT_grp.append(obj_curve)
        DNT_grp.append(snapshot_grp)
        instances = pm.listRelatives(snapshot_grp, c=True)
        instance_paths = ""

        for i in instances:
            instance_attr = ("", i.getParent().name(), str(i), i.getShape().name())
            instance_attr_joined = "/".join(instance_attr) + " "
            instance_paths += instance_attr_joined

        return instance_paths

    def _create_Bifrost_Graph(self):

        bifrost_shape = pm.createNode("bifrostGraphShape")
        pm.addAttr(longName='Stylized_MotionBlur', dt='string', h=True)
        pm.setAttr(bifrost_shape + ".Stylized_MotionBlur", "MotionTrails")
        pm.rename(bifrost_shape, "MT_bifrost_shape")
        bifrost_graph = bifrost_shape.getParent()
        bifrost_graph.rename("MT_bifrost_graph")
        DNT_grp.append(bifrost_graph)

        return bifrost_shape

    def _create_bg_input(self, obj_shape, instance_paths, bifrost_shape):

        fixed_text = "setOperation=+;active=true;channels=*;normalsPerFaceVertex=true;normalsPerPoint=true;normalsPerFace=false"
        mesh_port_options = f"pathinfo={{path=/{obj_shape.name(long=True)};{fixed_text}}}"
        strands_port_options = f"pathinfo={{path=/{instance_paths};{fixed_text}}}"

        pm.vnnNode(bifrost_shape , "/input", createOutputPort=["mesh", "Object"], portOptions=mesh_port_options)
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["strands", "Object"], portOptions=strands_port_options)
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["velocity_factor", "float"])
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["velocity_influence", "bool"])
        pm.vnnNode(bifrost_shape, "/input", createOutputPort=["length", "long"])

    def _set_default_attributes(self, bifrost_shape):

        pm.setAttr(bifrost_shape + ".length", 3)
        pm.setAttr(bifrost_shape + ".velocity_influence", 0)
        pm.setAttr(bifrost_shape + ".velocity_factor", 0.5)

    def _connect_MT_node(self, bifrost_shape):

        pm.vnnCompound(bifrost_shape, "/", addNode = "BifrostGraph,User::Compounds,motiontrail")
        pm.vnnConnect(bifrost_shape, ".strands", "/motiontrail.snapshot_meshes")
        pm.vnnConnect( bifrost_shape, ".mesh", "/motiontrail.in_mesh")
        pm.vnnNode(bifrost_shape, "/output", createInputPort = ["out_mesh", "Object"])
        pm.vnnConnect(bifrost_shape, "/motiontrail.out_mesh", ".out_mesh")
        pm.vnnCompound(bifrost_shape, "/motiontrail", setIsReferenced = False)
        pm.vnnNode(bifrost_shape, "/motiontrail/value7", setPortDefaultValues = ["value", str(END_FRAME)])
        pm.vnnConnect(bifrost_shape, ".velocity_factor", "/motiontrail.velocity_factor")
        pm.vnnConnect(bifrost_shape, ".velocity_influence", "/motiontrail.velocity_influence")
        pm.vnnConnect(bifrost_shape, ".length", "/motiontrail.length")

    def _create_DNT_grp(self, objects):

        if pm.objExists('DNT_MotionBlur'):
            DNT_MT_grp = pm.group(objects, n="DNT_Motion_Trails")
            pm.parent(DNT_MT_grp, 'DNT_MotionBlur')
        else:
            DNT_MT_grp = pm.group(objects, n="DNT_Motion_Trails")
            DNT_MB_grp = pm.group(DNT_MT_grp, n='DNT_MotionBlur' )
            pm.setAttr(DNT_MB_grp.visibility, 0)

        return DNT_MT_grp

    def _assign_shader(self, obj, shadingEngine):

        pm.sets(shadingEngine, e=True, forceElement=obj)

    def _createOutputMesh(self, obj_shape, bifrost_shape):

        obj = obj_shape.getParent()
        output_transform, _ = pm.polyCube( sx=1, sy=1, sz=1, h=1, n=obj.name() + "_MotionTrail" )
        output_shape = output_transform.getShape()
        pm.delete(output_transform, constructionHistory=True)
        bifrostToMayaNode = pm.createNode("bifrostGeoToMaya")
        bifrost_shape.out_mesh >> bifrostToMayaNode.bifrostGeo
        bifrostToMayaNode.mayaMesh[0] >> output_shape.inMesh

        return output_transform
    
    def kill(self):
        DNT_MB_grp = self.DNT_MT_grp.getParent()
        pm.delete(self.DNT_MT_grp)
        pm.delete(self.output)
        self.surfaceShader.kill()
        DNT_obj = pm.listRelatives(DNT_MB_grp, c = True)
        if not DNT_obj:
            pm.delete(DNT_MB_grp)


class SurfaceShader():

    #creates a Surface Shader
    surfaceShader = ""
    shadingEngine = ""

    def __init__(self):
        self.surfaceShader = self._createSurfaceShader()
        self.shadingEngine = self._createShadingEngine()
        self._connectShadingEngine()
        self.texture = self._create_texture_node()
        self.transparency = self._constructTransparency(self.texture)

    def _createSurfaceShader(self):
        surfaceShader = pm.shadingNode("surfaceShader", asShader=True)
        pm.setAttr(surfaceShader.outColor, (1,1,1))
        return surfaceShader

    def _createShadingEngine(self):
        shadingEngine = pm.shadingNode('shadingEngine', asUtility=True)
        return shadingEngine
    
    def _connectShadingEngine(self):
        self.surfaceShader.outColor >> self.shadingEngine.surfaceShader
        pm.connectAttr(self.shadingEngine + ".partition", ":renderPartition.sets", nextAvailable=True)

    def _create_texture_node(self):
        MT_file = pm.shadingNode('file', asTexture=True, isColorManaged=True)
        scene_path = pm.sceneName()
        directory_path = scene_path.split("/")[0:-2] 
        self.MT_file_path = os.path.join("/".join(directory_path), "sourceimages/motiontrails/") 
        pm.setAttr(MT_file + '.fileTextureName', self.MT_file_path + "1.png", type='string')

        return MT_file

    def _constructTransparency(self, texture):
        rampTransparency = pm.shadingNode("ramp", asTexture=True )
        pm.setAttr(rampTransparency + ".type", 1);
        pm.setAttr(rampTransparency + ".interpolation", 6)
        pm.setAttr(rampTransparency.colorEntryList[1].color, (1,1,1))
        pm.setAttr(rampTransparency.colorEntryList[0].color, (0,0,0))
        pm.setAttr(rampTransparency.colorEntryList[0].position, 1)

        colorMath =  pm.shadingNode('colorMath', asUtility=True)
        pm.setAttr(colorMath + ".operation", 5)

        rampTransparency.outColor >> colorMath.colorA
        texture.outColor >> colorMath.colorB
        colorMath.outColor >> self.surfaceShader.outTransparency

        return rampTransparency
    
    def kill(self):
        all_nodes = pm.listConnections(self.surfaceShader)
        for n in all_nodes:
            if pm.nodeType(n) == 'defaultShaderList':
                continue
            pm.delete(n)
        pm.delete(self.surfaceShader)



