import pymel.core as pm
import os

class Create_Cache:

    def __init__(self, sl_faces, obj_shape, start_frame, end_frame):
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.duplicate = self._create_duplicate(obj_shape, sl_faces)
        self.folderPath = self._get_cache_folderpath()
        self.cachePath = self._create_cache_path(obj_shape, self.folderPath)
        self.cache = self._create_cache(self.duplicate)
        self.DNT_ls = [self.duplicate, self.cache]

    def _create_duplicate(self, obj_shape, sl_faces):

        obj = obj_shape.getParent()
        duplicate = pm.duplicate(obj, rr=True, ic=True)[0]
        duplicate_shape = duplicate.getShape()
        duplicated_faces = []

        for f in sl_faces:
            str(f)
            reaplace_obj = f.replace(obj.name(), duplicate.name())
            dupl_f = reaplace_obj.replace(obj_shape.name(), duplicate_shape.name())
            duplicated_faces.append(dupl_f)

        pm.select(duplicate.f, r=True)
        pm.select(duplicated_faces, d=True)
        pm.delete()

        return duplicate
    
    def _get_cache_folderpath(self):

        scene_path = pm.system.sceneName()
        ma_file = scene_path.split("/")[-1]
        filename = ma_file.split(".")[0]
        directory_path_ls = scene_path.split("/")[0:-2]
        directory_path = "/".join(directory_path_ls) + "/cache/alembic"
        new_folder_name = filename + "_cache"
        new_folder_path = os.path.join(directory_path, new_folder_name)

        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        return new_folder_path

    def _create_cache_path(self,obj_shape, folderPath):

        obj = obj_shape.getParent()
        version = 1
        cacheName = obj.name() + "_sel" + "_" + str(version)
        cachePath = folderPath + "/" + cacheName + ".abc"

        while os.path.exists(cachePath):
            version += 1
            cacheName = obj.name() + "_sel" + "_" + str(version) 
            cachePath = folderPath + "/" + cacheName + ".abc"
        
        return cachePath

    def _create_cache(self, duplicate):

        pm.select(duplicate)
        mel_cmd = "-frameRange " + str(self.start_frame) + " " + str(self.end_frame)\
                + " -dataFormat ogawa -root |" + duplicate.name() + " -file " + self.cachePath
        pm.AbcExport(j = mel_cmd)
        pm.importFile(self.cachePath, type="Alembic", ra=True)
        cache_file = self.cachePath.split("/")[-1]
        cache_name = cache_file[0:-4] + "_" + duplicate.name()
        pm.select(cache_name)
        cache = pm.ls(sl=True)[0]

        return cache
    
    def kill(self):
        os.remove(self.cachePath)
        if os.path.exists(self.folderPath):
            if len(self.folderPath) == 0:
                os.rmdir(self.folderPath)
        