import omni.kit.commands
import omni.usd
import omni.kit.undo
from pxr import Gf, Sdf, Usd

class BoxMaker:
    def __init__(self) -> None:
        self._stage:Usd.Stage = omni.usd.get_context().get_stage()
        omni.kit.commands.execute('DeletePrims', paths=["/World/CB_Looks", "/World/Cornell_Box", "/World/defaultLight"])
   
        self.Create_Box()
        
    def Create_Panel(self):
        plane_prim_path = omni.usd.get_stage_next_free_path(self._stage, self.geom_xform_path.AppendPath("Plane"), False)
        omni.kit.commands.execute('CreateMeshPrimWithDefaultXform',prim_type='Plane')
        omni.kit.commands.execute('MovePrim',
            path_from='/World/Plane',
            path_to=plane_prim_path)        
       
        mtl_path = Sdf.Path(omni.usd.get_stage_next_free_path(self._stage, self.looks_scope_path.AppendPath("OmniPBR"), False))
        omni.kit.commands.execute('CreateMdlMaterialPrim',
            mtl_url='OmniPBR.mdl',
            mtl_name='OmniPBR',
            mtl_path=str(mtl_path))

        
        omni.kit.commands.execute('BindMaterial',
            prim_path=plane_prim_path,
            material_path=str(mtl_path),
            strength=['strongerThanDescendants'])
    



        plane_prim = self._stage.GetPrimAtPath(plane_prim_path)
        plane_prim.GetAttribute("xformOp:scale").Set(Gf.Vec3d(4,4,4))

        shader_prim = self._stage.GetPrimAtPath(mtl_path.AppendPath("Shader"))
        mtl_color_attr = shader_prim.CreateAttribute("inputs:diffuse_color_constant", Sdf.ValueTypeNames.Color3f)
        mtl_color_attr.Set((0.9, 0.9, 0.9)) 
        return plane_prim       



    def Create_Box(self):

        with omni.kit.undo.group():

            self.geom_xform_path = Sdf.Path(omni.usd.get_stage_next_free_path(self._stage, "/World/Cornell_Box", False))
            self.looks_scope_path = Sdf.Path(omni.usd.get_stage_next_free_path(self._stage, "/World/CB_Looks", False))
            self.geom_xform_path2 = Sdf.Path(omni.usd.get_stage_next_free_path(self._stage, "/World/Cornell_Box/Panels", False))
            omni.kit.commands.execute('CreatePrimWithDefaultXform', prim_type='Xform', prim_path=str(self.geom_xform_path))
            omni.kit.commands.execute('CreatePrimWithDefaultXform', prim_type='Xform', prim_path=str(self.geom_xform_path2))
            omni.kit.commands.execute('CreatePrimWithDefaultXform', prim_type='Scope', prim_path=str(self.looks_scope_path))



#create floor
            panel = self.Create_Panel()
            panel.GetAttribute("xformOp:scale").Set(Gf.Vec3d( 4, 4, 15))
            
#create back wall
            panel = self.Create_Panel()
            panel.GetAttribute("xformOp:rotateXYZ").Set(Gf.Vec3d(90, 0, 90))
            panel.GetAttribute("xformOp:translate").Set(Gf.Vec3d(0, 200, -400))
            

#create front wall 
            # panel = self.Create_Panel()
            # panel.GetAttribute("xformOp:rotateXYZ").Set(Gf.Vec3d(90, 0, 90))
            # panel.GetAttribute("xformOp:translate").Set(Gf.Vec3d(0, 100, 100))
            
#create ceiling 
            panel = self.Create_Panel()
            panel.GetAttribute("xformOp:translate").Set(Gf.Vec3d(0, 400, 0))
            panel.GetAttribute("xformOp:scale").Set(Gf.Vec3d(4, 4, 15))
            
#create colored wall 1
            panel = self.Create_Panel() 
            panel.GetAttribute("xformOp:rotateXYZ").Set(Gf.Vec3d(0, 0, 90))
            panel.GetAttribute("xformOp:translate").Set(Gf.Vec3d(-200, 200, 0))
            panel.GetAttribute("xformOp:scale").Set(Gf.Vec3d(4, 4, 15))



            
#create colored wall 2
            panel = self.Create_Panel()
            panel.GetAttribute("xformOp:rotateXYZ").Set(Gf.Vec3d(0, 0, 90))
            panel.GetAttribute("xformOp:translate").Set(Gf.Vec3d(200, 200, 0))
            panel.GetAttribute("xformOp:scale").Set(Gf.Vec3d(4, 4, 15))      

#move panels


            omni.kit.commands.execute('MovePrim',
                path_from='/World/Cornell_Box/Plane',
                path_to='/World/Cornell_Box/Panels/Plane')
            
            omni.kit.commands.execute('MovePrim',
                path_from='/World/Cornell_Box/Plane_01',
                path_to='/World/Cornell_Box/Panels/Plane_01')            

            omni.kit.commands.execute('MovePrim',
                path_from='/World/Cornell_Box/Plane_02',
                path_to='/World/Cornell_Box/Panels/Plane_02')

            omni.kit.commands.execute('MovePrim',
                path_from='/World/Cornell_Box/Plane_03',
                path_to='/World/Cornell_Box/Panels/Plane_03')

            omni.kit.commands.execute('MovePrim',
                path_from='/World/Cornell_Box/Plane_04',
                path_to='/World/Cornell_Box/Panels/Plane_04')
                        
#make wall red
            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path('/World/CB_Looks/OmniPBR_03/Shader.inputs:diffuse_color_constant'),
                value=Gf.Vec3f(1.0, 0.0, 0.0),
                prev=Gf.Vec3f(0.9, 0.9, 0.9))


#make wall green
            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path('/World/CB_Looks/OmniPBR_04/Shader.inputs:diffuse_color_constant'),
                value=Gf.Vec3f(0.0, 1.0, 0.2),
                prev=Gf.Vec3f(0.9, 0.9, 0.9))


#create rectangle light

            light_prim_path = omni.usd.get_stage_next_free_path(self._stage, self.geom_xform_path.AppendPath("RectLight"), False)
            omni.kit.commands.execute('CreatePrim',prim_type='RectLight', attributes={'width': 150, 'height': 100, 'intensity': 20000})

            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path('/World/RectLight.xformOp:translate'),
                value=Gf.Vec3d(0.0, 399.9000, 125),
                prev=Gf.Vec3d(0.0, 0.0, 0.0))



            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path('/World/RectLight.xformOp:rotateXYZ'),
                value=Gf.Vec3d(0.0, -90.0, -90.0),
                prev=Gf.Vec3d(0.0, 0.0, 0.0))

            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path('/World/RectLight.visibleInPrimaryRay'),
                value=True,
                prev=None)

            omni.kit.commands.execute('MovePrim',
                path_from='/World/RectLight',
                path_to='/World/Cornell_Box/RectLight')

            light_prim = self._stage.GetPrimAtPath(light_prim_path)
# visible light
            #light_prim.GetAttribute("xformOp:scale").Set(Gf.Vec3d(4,4,4))
            light_prim.CreateAttribute("visibleInPrimaryRay", Sdf.ValueTypeNames.Bool).Set(True)



#create Camera
            omni.kit.commands.execute('CreatePrimWithDefaultXform',
                prim_type='Camera',
                attributes={'focusDistance': 400, 'focalLength': 27.5})


            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path('/World/Camera.xformOp:translate'),
                value=Gf.Vec3d(0.0, 200.0, 1180.10002),
                prev=Gf.Vec3d(0.0, 200.0, 1200.0))


            omni.kit.commands.execute('MovePrim',
                path_from='/World/Camera',
                path_to='/World/Cornell_Box/Camera')

#Create Cubes
        
            omni.kit.commands.execute('CreateMeshPrimWithDefaultXform',
                prim_type='Cube')



            omni.kit.commands.execute('TransformPrimSRT',
                path=Sdf.Path('/World/Cube'),
                new_translation=Gf.Vec3d(0.0, 50.0, 100.0),
                new_rotation_euler=Gf.Vec3d(0.0, 0.0, 0.0),
                new_rotation_order=Gf.Vec3i(0, 1, 2),
                new_scale=Gf.Vec3d(1.0, 1.0, 1.0),
                old_translation=Gf.Vec3d(0.0, 0.0, 0.0),
                old_rotation_euler=Gf.Vec3d(0.0, 0.0, 0.0),
                old_rotation_order=Gf.Vec3i(0, 1, 2),
                old_scale=Gf.Vec3d(1.0, 1.0, 1.0))


            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path('/World/Cube.xformOp:rotateXYZ'),
                value=Gf.Vec3d(0.0, -45, 0.0),
                prev=Gf.Vec3d(0.0, 0.0, 0.0))



            omni.kit.commands.execute('BindMaterial',
                material_path='/World/CB_Looks/OmniPBR',
                prim_path=['/World/Cube'],
                strength=['weakerThanDescendants'])


            omni.kit.commands.execute('CopyPrims',
                paths_from=['/World/Cube'],
                duplicate_layers=False,
                combine_layers=False,
                flatten_references=False)



            omni.kit.commands.execute('TransformPrimSRT',
                path=Sdf.Path('/World/Cube_01'),
                new_translation=Gf.Vec3d(99.8525344330427, 49.99999999997604, -83.82421861450064),
                new_rotation_euler=Gf.Vec3d(0.0, -45.0, 0.0),
                new_rotation_order=Gf.Vec3i(0, 1, 2),
                new_scale=Gf.Vec3d(1.0, 1.0, 1.0),
                old_translation=Gf.Vec3d(0.0, 50.0, 100.0),
                old_rotation_euler=Gf.Vec3d(0.0, -45.0, 0.0),
                old_rotation_order=Gf.Vec3i(0, 1, 2),
                old_scale=Gf.Vec3d(1.0, 1.0, 1.0))



            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path('/World/Cube_01.xformOp:scale'),
                value=Gf.Vec3d(1.0, 1.5, 1.0),
                prev=Gf.Vec3d(1.0, 1.598320722579956, 1.0))


            omni.kit.commands.execute('TransformPrimSRT',
                path=Sdf.Path('/World/Cube_01'),
                new_translation=Gf.Vec3d(99.85253443304272, 74.75868843615456, -100.0),
                new_rotation_euler=Gf.Vec3d(0.0, -45.0, 0.0),
                new_rotation_order=Gf.Vec3i(0, 1, 2),
                new_scale=Gf.Vec3d(1.0, 1.5, 1.0),
                old_translation=Gf.Vec3d(99.8525344330427, 49.99999999997604, -83.82421861450064),
                old_rotation_euler=Gf.Vec3d(0.0, -45.0, 0.0),
                old_rotation_order=Gf.Vec3i(0, 1, 2),
                old_scale=Gf.Vec3d(1.0, 1.5, 1.0))



            omni.kit.commands.execute('CopyPrims',
                paths_from=['/World/Cube_01'],
                duplicate_layers=False,
                combine_layers=False,
                flatten_references=False)



            omni.kit.commands.execute('TransformPrimSRT',
                path=Sdf.Path('/World/Cube_02'),
                new_translation=Gf.Vec3d(-100.31094017767478, 74.75868843615382, -200.65476487048673),
                new_rotation_euler=Gf.Vec3d(0.0, -45.0, 0.0),
                new_rotation_order=Gf.Vec3i(0, 1, 2),
                new_scale=Gf.Vec3d(1.0, 1.5, 1.0),
                old_translation=Gf.Vec3d(99.85253443304272, 74.75868843615456, -100.0),
                old_rotation_euler=Gf.Vec3d(0.0, -45.0, 0.0),
                old_rotation_order=Gf.Vec3i(0, 1, 2),
                old_scale=Gf.Vec3d(1.0, 1.5, 1.0))


            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path('/World/Cube_02.xformOp:scale'),
                value=Gf.Vec3d(1.0, 2.0, 1.0),
                prev=Gf.Vec3d(1.0, 1.5, 1.0))


            omni.kit.commands.execute('TransformPrimSRT',
                path=Sdf.Path('/World/Cube_02'),
                new_translation=Gf.Vec3d(-100.31094017767478, 100.0, -200.65476487048673),
                new_rotation_euler=Gf.Vec3d(0.0, -45.0, 0.0),
                new_rotation_order=Gf.Vec3i(0, 1, 2),
                new_scale=Gf.Vec3d(1.0, 2.0, 1.0),
                old_translation=Gf.Vec3d(-100.31094017767478, 74.75868843615382, -200.65476487048673),
                old_rotation_euler=Gf.Vec3d(0.0, -45.0, 0.0),
                old_rotation_order=Gf.Vec3i(0, 1, 2),
                old_scale=Gf.Vec3d(1.0, 2.0, 1.0))


            omni.kit.commands.execute('MovePrim',
                path_from='/World/Cube',
                path_to='/World/Cornell_Box/Cube')

            omni.kit.commands.execute('MovePrim',
                path_from='/World/Cube_01',
                path_to='/World/Cornell_Box/Cube_01')
            omni.kit.commands.execute('MovePrim',
                path_from='/World/Cube_02',
                path_to='/World/Cornell_Box/Cube_02')
