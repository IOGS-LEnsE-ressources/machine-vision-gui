from pypylon import pylon

class CameraBasler:
    def __init__(self):
        self.tl_factory = pylon.TlFactory.GetInstance()
        self.camera = None
        self.is_open = False

    def find_first_camera(self):
        devices = self.tl_factory.EnumerateDevices()
        if len(devices) == 0:
            raise Exception("Aucune caméra Basler détectée")
        self.camera = pylon.InstantCamera(self.tl_factory.CreateDevice(devices[0]))
        return True

    def open(self):
        if self.camera is None:
            raise Exception("Aucune caméra sélectionnée. Appeler find_first_camera().")
        if not self.is_open:
            self.camera.Open()
            self.is_open = True

    def close(self):
        if self.camera and self.is_open:
            self.camera.Close()
            self.is_open = False

    def start_grabbing(self, strategy=pylon.GrabStrategy_LatestImageOnly):
        if self.camera is None:
            raise Exception("Aucune caméra sélectionnée.")
        self.camera.StartGrabbing(strategy)

    def stop_grabbing(self):
        if self.camera and self.camera.IsGrabbing():
            self.camera.StopGrabbing()

    def grab_frame(self, timeout=1000):
        if self.camera is None or not self.camera.IsGrabbing():
            raise Exception("La caméra n’est pas en mode capture.")
        grab_result = self.camera.RetrieveResult(timeout, pylon.TimeoutHandling_ThrowException)
        if grab_result.GrabSucceeded():
            img = grab_result.Array
            grab_result.Release()
            return img
        else:
            grab_result.Release()
            raise Exception("Échec de la capture d’image.")
