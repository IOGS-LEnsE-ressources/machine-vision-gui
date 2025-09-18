from PyQt6.QtCore import QTimer

class CameraController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Connexion des boutons
        self.view.btn_start.clicked.connect(self.start_camera)
        self.view.btn_stop.clicked.connect(self.stop_camera)
        self.view.btn_quit.clicked.connect(self.quit_app)

    def start_camera(self):
        try:
            self.model.find_first_camera()
            self.model.open()
            self.model.start_grabbing()
            self.timer.start(30)  # ms → ~33 fps
        except Exception as e:
            print("Erreur start_camera:", e)

    def stop_camera(self):
        self.timer.stop()
        self.model.stop_grabbing()
        self.model.close()

    def update_frame(self):
        try:
            frame = self.model.grab_frame()
            self.view.update_image(frame)
            self.view.update_histogram(frame)
        except Exception as e:
            print("Erreur update_frame:", e)
            self.stop_camera()

    def quit_app(self):
        self.stop_camera()
        self.view.close()
