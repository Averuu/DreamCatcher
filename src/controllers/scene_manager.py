class SceneManager:
    def __init__(self):
        self.current_scene = "MENU"
        self.active_controller = None

    def switch_to(self, scene, controller=None):
        self.current_scene = scene
        self.active_controller = controller