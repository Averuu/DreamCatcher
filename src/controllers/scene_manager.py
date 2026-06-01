class SceneManager:
    def __init__(self):
        self.current_scene = "MENU"
    
    def switch_to(self, new_scene):
        self.current_scene = new_scene