import omni.ext
import omni.ui as ui
import omni.kit.commands
import omni.usd
from pxr import Gf, Sdf
from .box_maker import BoxMaker
from omni.ui import color as cl
from omni.ui import constant as fl

WINDOW_TITLE = "Cornell Box Maker"

SPACING = 4


combo_sub = None
options = ["Classic", "SIGGRAPH 1984", "NVIDIA Omniverse"]

class CornellBoxWindow(ui.Window):
    def __init__(self, title, menu_path):
        super().__init__(title, width=450, height=280)
        self._menu_path = menu_path
        self.set_visibility_changed_fn(self._on_visibility_changed)
        self.frame.set_build_fn(self._build_window)

        

#color widget variables
        self._color_model = None
        self._color_model_2 = None
        self._color_changed_subs = []
        self._color_changed_subs_2 = []
        self._path_model = None 
        self._path_model_2 = None
        self._change_info_path_subscription = None
        self._change_info_path_subscription_2 = None
        self._stage = omni.usd.get_context().get_stage()
        self._OmniPBR_Path_03 = "/World/CB_Looks/OmniPBR_03/Shader.inputs:diffuse_color_constant"
        self._OmniPBR_Path_04 = "/World/CB_Looks/OmniPBR_04/Shader.inputs:diffuse_color_constant" 
        

#subscribe mat 1
        attr_path = self._OmniPBR_Path_03
        color_attr = self._stage.GetAttributeAtPath(attr_path)
        if color_attr:
            self._change_info_path_subscription = omni.usd.get_watcher().subscribe_to_change_info_path(
                     attr_path, 
                     self._on_mtl_attr_changed)


#subscribe mat 2
        attr_path_2 = self._OmniPBR_Path_04 
        color_attr_2 = self._stage.GetAttributeAtPath(attr_path_2)
        if color_attr_2:
            self._change_info_path_subscription_2 = omni.usd.get_watcher().subscribe_to_change_info_path(
                    attr_path_2, self._on_mtl_attr_changed_2)        

#combox group variables 
        self.combo_sub = None
#main ui Window
    def _build_window(self):
        
        #with self.frame:
        with ui.ScrollingFrame():
            
            with ui.VStack(height=0):
                def on_click():
                    BoxMaker()

                with ui.HStack(height=0, spacing=SPACING):
                        ui.Label("Start Here: ", height=40, width=0)
                        ui.Button("Make Box", clicked_fn=lambda: on_click()) 
                                    
                                    
                with ui.CollapsableFrame("Color", name="group", height=50):
                    with ui.VStack(height=0, spacing=SPACING):           
                        with ui.HStack(height=0, spacing=SPACING):
                                ui.Label("Colored Wall #1: ", height=0, width=0)
                                self._color_model = ui.ColorWidget(0.9, 0.0, 0.0, height=0).model
                                for item in self._color_model.get_item_children():
                                    component = self._color_model.get_item_value_model(item)
                                    self._color_changed_subs.append(component.subscribe_value_changed_fn(self._on_color_changed))
                                    #ui.FloatDrag(component)
                                                
                        self._path_model = self._OmniPBR_Path_03                        
                        
                        with ui.HStack(height=0, spacing=SPACING):
                                ui.Label("Colored Wall #2: ", height=0, width=0)  
                                self._color_model_2 = ui.ColorWidget(0.0, 0.9, 0.2, height=0).model
                                for item in self._color_model_2.get_item_children():
                                    component = self._color_model_2.get_item_value_model(item)
                                    self._color_changed_subs_2.append(component.subscribe_value_changed_fn(self._on_color_changed_2))
                                    #ui.FloatDrag(component)

                        self._path_model_2 = self._OmniPBR_Path_04            

#combobox group
    
                        with ui.HStack(height=0, spacing=SPACING):
                            ui.Label("Select Preset Style:",  height=0, width=0)
                            
                            
                            
                            combo_model: ui.AbstractItemModel = ui.ComboBox(0, *options).model

                            def combo_changed(item_model: ui.AbstractItemModel, item: ui.AbstractItem):
                                value_model = item_model.get_item_value_model(item)
                                current_index = value_model.as_int
                                option = options[current_index] 
                                #print(f"Selected '{option}' at index {current_index}.")                           
                                if option == "Classic":
                                     mtl_path_1 = "/World/CB_Looks/OmniPBR_03/Shader"
                                     shader_prim_1 = self._stage.GetPrimAtPath(mtl_path_1)
                                     mtl_color_attr_1 = shader_prim_1.CreateAttribute("inputs:diffuse_color_constant", Sdf.ValueTypeNames.Color3f)
                                     mtl_color_attr_1.Set((0.9, 0.0, 0.0))

                                     mtl_path_2 = "/World/CB_Looks/OmniPBR_04/Shader"
                                     shader_prim_2 = self._stage.GetPrimAtPath(mtl_path_2)
                                     mtl_color_attr_2 = shader_prim_2.CreateAttribute("inputs:diffuse_color_constant", Sdf.ValueTypeNames.Color3f)
                                     mtl_color_attr_2.Set((0.0, 0.9, 0.2))

                                if option == "SIGGRAPH 1984":
                                     mtl_path_1 = "/World/CB_Looks/OmniPBR_03/Shader"
                                     shader_prim_1 = self._stage.GetPrimAtPath(mtl_path_1)
                                     mtl_color_attr_1 = shader_prim_1.CreateAttribute("inputs:diffuse_color_constant", Sdf.ValueTypeNames.Color3f)
                                     mtl_color_attr_1.Set((0.9, 0.0, 0.0))

                                     mtl_path_2 = "/World/CB_Looks/OmniPBR_04/Shader"
                                     shader_prim_2 = self._stage.GetPrimAtPath(mtl_path_2)
                                     mtl_color_attr_2 = shader_prim_2.CreateAttribute("inputs:diffuse_color_constant", Sdf.ValueTypeNames.Color3f)
                                     mtl_color_attr_2.Set((0.0, 0.0, 0.9))

                                if option == "NVIDIA Omniverse":
                                     mtl_path_1 = "/World/CB_Looks/OmniPBR_03/Shader"
                                     shader_prim_1 = self._stage.GetPrimAtPath(mtl_path_1)
                                     mtl_color_attr_1 = shader_prim_1.CreateAttribute("inputs:diffuse_color_constant", Sdf.ValueTypeNames.Color3f)
                                     mtl_color_attr_1.Set((0.069, 0.069, 0.069))
                                    #  self._color_model.Set((0.069, 0.069, 0.069))

                                     mtl_path_2 = "/World/CB_Looks/OmniPBR_04/Shader"
                                     shader_prim_2 = self._stage.GetPrimAtPath(mtl_path_2)
                                     mtl_color_attr_2 = shader_prim_2.CreateAttribute("inputs:diffuse_color_constant", Sdf.ValueTypeNames.Color3f)
                                     mtl_color_attr_2.Set((0.4, 0.8, 0.0))

                            
                            self.combo_sub = combo_model.subscribe_item_changed_fn(combo_changed)

                            ui.Spacer(width=1)

                ui.Spacer(width=0,height=0)

#scale sliders for cornell box xform
                self._slider_model_x = ui.SimpleFloatModel()
                self._slider_model_y = ui.SimpleFloatModel()
                self._slider_model_z = ui.SimpleFloatModel()
                self._source_prim_model = ui.SimpleStringModel()  
                with ui.CollapsableFrame("Scale", name="group", height=100,):
                    with ui.VStack(height=0, spacing=SPACING):
                        with ui.HStack():
                            ui.Spacer(width=5)
                            ui.Label("Box Width: ", height=0, width=0)
                            #ui.Spacer(width=5)
                            #ui.FloatDrag(self._slider_model,  min=0.1, max=5)
                            ui.FloatSlider(self._slider_model_x,  min=0.1, max=10, step=0.05)
                            #ui.Spacer(width=10)


                        def update_scale_x(prim_name, value):
                            usd_context = omni.usd.get_context()
                            stage = usd_context.get_stage()
                            cube_prim = stage.GetPrimAtPath("/World/Cornell_Box/Panels")
                            scale_attr = cube_prim.GetAttribute("xformOp:scale")
                            scale = scale_attr.Get()
                            scale_attr.Set(Gf.Vec3d(value, scale[1], scale[2]))



                        if self._slider_model_x:
                            self._slider_subscription_x = None
                            self._slider_model_x.as_float = 1.0
                            self._slider_subscription_x = self._slider_model_x.subscribe_value_changed_fn(
                                lambda m, #the following is where we change from self.model to self._source_prim_model
                                p=self._source_prim_model: update_scale_x(p, m.as_float)
                            )   


                        with ui.HStack():
                            ui.Spacer(width=5)
                            ui.Label("Box Height: ", height=0, width=0)
                            #ui.Spacer(width=5)
                            ui.FloatSlider(self._slider_model_y,  min=0.1, max=10, step=0.05)
                            #ui.Spacer(width=10)

                        def update_scale_y(prim_name, value):
                            usd_context = omni.usd.get_context()
                            stage = usd_context.get_stage()
                            cube_prim = stage.GetPrimAtPath("/World/Cornell_Box/Panels")
                            scale_attr = cube_prim.GetAttribute("xformOp:scale")
                            scale = scale_attr.Get()
                            scale_attr.Set(Gf.Vec3d(scale[0], value, scale[2]))

                            #usd_context = omni.usd.get_context()
                            #stage = usd_context.get_stage()
                            light_prim = stage.GetPrimAtPath("/World/Cornell_Box/RectLight")
                            trans_attr = light_prim.GetAttribute("xformOp:translate")
                            trans = trans_attr.Get()
                            trans_attr.Set(Gf.Vec3d(trans[0], ((399.9) * value), trans[2]))



                        if self._slider_model_y:
                            self._slider_subscription_y = None
                            self._slider_model_y.as_float = 1.0
                            self._slider_subscription = self._slider_model_y.subscribe_value_changed_fn(
                                lambda m, #the following is where we change from self.model to self._source_prim_model
                                p=self._source_prim_model: update_scale_y(p, m.as_float)
                            )  


                        with ui.HStack():
                            ui.Spacer(width=5)
                            ui.Label("Box Length: ", height=0, width=0)
                            #ui.Spacer(width=5)
                            ui.FloatSlider(self._slider_model_z,  min=0.1, max=10, step=0.05)
                            #ui.Spacer(width=10)

                        def update_scale_z(prim_name, value):
                            usd_context = omni.usd.get_context()
                            stage = usd_context.get_stage()
                            cube_prim = stage.GetPrimAtPath("/World/Cornell_Box/Panels")
                            scale_attr = cube_prim.GetAttribute("xformOp:scale")
                            scale = scale_attr.Get()
                            scale_attr.Set(Gf.Vec3d(scale[0], scale[1], value))


                        if self._slider_model_z:
                            self._slider_subscription_z = None
                            self._slider_model_z.as_float = 1.0
                            self._slider_subscription_z = self._slider_model_z.subscribe_value_changed_fn(
                                lambda m, #the following is where we change from self.model to self._source_prim_model
                                p=self._source_prim_model: update_scale_z(p, m.as_float))

#dock
        super().dock_in_window("Environments", ui.DockPosition.SAME)  

#functions for color picker

    def _on_mtl_attr_changed(self, path):
        color_attr = self._stage.GetAttributeAtPath(path)
        color_model_items = self._color_model.get_item_children()
        if color_attr:     
            color = color_attr.Get()
            for i in range(len(color)):
                component = self._color_model.get_item_value_model(color_model_items[i])
                component.set_value(color[i])

    def _on_mtl_attr_changed_2(self, path):
        color_attr = self._stage.GetAttributeAtPath(path)
        color_model_items = self._color_model_2.get_item_children()
        if color_attr:
            color = color_attr.Get()
            for i in range(len(color)):
                component = self._color_model_2.get_item_value_model(color_model_items[i])
                component.set_value(color[i])



    def _on_color_changed(self, model):
        values = []
        for item in self._color_model.get_item_children():
            component = self._color_model.get_item_value_model(item)
            values.append(component.as_float)

        if Sdf.Path.IsValidPathString(self._path_model):
            attr_path = Sdf.Path(self._path_model)
            color_attr = self._stage.GetAttributeAtPath(attr_path)
            if color_attr:
                color_attr.Set(Gf.Vec3f(*values[0:3]))


    def _on_color_changed_2(self, model):
        values = []
        for item in self._color_model_2.get_item_children():
            component = self._color_model_2.get_item_value_model(item)
            values.append(component.as_float)


        if Sdf.Path.IsValidPathString(self._path_model_2):
            attr_path = Sdf.Path(self._path_model_2)
            color_attr = self._stage.GetAttributeAtPath(attr_path)
            if color_attr:
                color_attr.Set(Gf.Vec3f(*values[0:3]))



    def _on_visibility_changed(self, visible):
        omni.kit.ui.get_editor_menu().set_value(self._menu_path, visible)


    def destroy(self) -> None:
        self._change_info_path_subscription = None
        self._color_changed_subs = None
        return super().destroy()

    def on_shutdown(self):
        self._win = None

    def show(self):
        self.visible = True
        self.focus()    
    
    def hide(self):
        self.visible = False