
#from .box_maker_2 import BoxMaker2
from .box_maker import BoxMaker
import omni.ext
import omni.ui as ui
import omni.kit.commands
from pxr import Gf
import omni.usd

WINDOW_TITLE = "Cornell Box Maker"

SPACING = 4

class CornellBoxWindow(ui.Window):
    def __init__(self, title, menu_path):
        super().__init__(title, width=450, height=300)
        self._menu_path = menu_path
        self.set_visibility_changed_fn(self._on_visibility_changed)
        self._build_ui()

#color widget variables


    def on_shutdown(self):
        self._win = None

    def show(self):
        self.visible = True
        self.focus()    
    
    def hide(self):
        self.visible = False

    def _build_ui(self):
        
        with self.frame:
            
            with ui.VStack():
                def on_click():
                    BoxMaker()

                with ui.HStack(height=0, spacing=SPACING):
                        ui.Label("Start Here: ", height=0, width=0)
                        ui.Button("Make Box", clicked_fn=lambda: on_click()) 
                                    
                                    
                with ui.CollapsableFrame("Color *not working yet...*", name="group"):
                    with ui.VStack(height=0, spacing=SPACING):           
                        with ui.HStack(height=0, spacing=SPACING):
                                ui.Label("color wall 1: ", height=0, width=0)
                                color_model = ui.ColorWidget(0.9, 0.0, 0.0, height=0).model
                                for item in color_model.get_item_children():
                                    component = color_model.get_item_value_model(item)
                                    #ui.FloatDrag(component)
                        
                        with ui.HStack(height=0, spacing=SPACING):
                                ui.Label("color wall 2: ", height=0, width=0)  
                                color_model2 = ui.ColorWidget(0.0, 0.9, 0.2, height=0).model
                                for item in color_model2.get_item_children():
                                    component = color_model2.get_item_value_model(item)
                                    #ui.FloatDrag(component)
#disabled checkbox group
                        # with ui.HStack(height=0, spacing=SPACING):
                        #         ui.Label("Select preset style:",  height=0, width=0)
                        #         ui.ComboBox(0, "Classic", "SIGGRAPH 1984", "NVIDIA Omniverse", height=0)
                        #         ui.Spacer(width=1)

                ui.Spacer(width=0,height=0)
                self._slider_model_x = ui.SimpleFloatModel()
                self._slider_model_y = ui.SimpleFloatModel()
                self._slider_model_z = ui.SimpleFloatModel()
                self._source_prim_model = ui.SimpleStringModel()  
                with ui.CollapsableFrame("Scale", name="group"):
                    with ui.VStack(height=0, spacing=SPACING):
                        with ui.HStack():
                            ui.Spacer(width=5)
                            ui.Label("box width: ", height=0, width=0)
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
                            ui.Label("box height: ", height=0, width=0)
                            #ui.Spacer(width=5)
                            ui.FloatSlider(self._slider_model_y,  min=1.0, max=10, step=0.05)
                            #ui.Spacer(width=10)

                        def update_scale_y(prim_name, value):
                            usd_context = omni.usd.get_context()
                            stage = usd_context.get_stage()
                            cube_prim = stage.GetPrimAtPath("/World/Cornell_Box/Panels")
                            scale_attr = cube_prim.GetAttribute("xformOp:scale")
                            scale = scale_attr.Get()
                            scale_attr.Set(Gf.Vec3d(scale[0], value, scale[2]))



                        if self._slider_model_y:
                            self._slider_subscription_y = None
                            self._slider_model_y.as_float = 1.0
                            self._slider_subscription = self._slider_model_y.subscribe_value_changed_fn(
                                lambda m, #the following is where we change from self.model to self._source_prim_model
                                p=self._source_prim_model: update_scale_y(p, m.as_float)
                            )  


                        with ui.HStack():
                            ui.Spacer(width=5)
                            ui.Label("box length: ", height=0, width=0)
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





    def _on_visibility_changed(self, visible):
        omni.kit.ui.get_editor_menu().set_value(self._menu_path, visible)