import time
from PyQt6.QtCore import QObject, QThread
from _app.template_controller import TemplateController
from modules.basler.basler_views import *
#from lensepy.pyqt6.widget_image_display import ImageDisplayWidget


class BaslerController(TemplateController):
    """

    """

    def __init__(self, parent=None):
        """
        :param parent:
        """
        super().__init__(parent)
        self.top_left = ImageDisplayWidget()
        self.bot_left = HistogramWidget()
        self.bot_right = QWidget()
        self.top_right = QWidget()
        # Setup widgets
        self.bot_left.set_background('white')
        if self.parent.variables['bits_depth'] is not None:
            self.bot_left.set_bits_depth(int(self.parent.variables['bits_depth']))
        else:
            self.bot_left.set_bits_depth(8)
        if self.parent.variables['image'] is not None:
            self.top_left.set_image_from_array(self.parent.variables['image'])
            self.bot_left.set_image(self.parent.variables['image'])
        self.bot_left.refresh_chart()
        # Variables
        self.camera_connected = False       # Camera is connected
        self.thread = None
        self.worker = None
        self.colormode = []
        self.colormode_bits_depth = []

        # Signals

        # Init Camera
        self.init_camera()
        self.top_right = CameraInfosWidget(self)
        self.top_right.update_infos()
        # Signals
        self.top_right.color_mode_changed.connect(self.handle_color_mode_changed)
        # Start thread
        self.start_live()

    def init_camera(self):
        """

        :return:
        """
        # Get color mode list
        colormode_get = self.parent.xml_app.get_sub_parameter('camera','colormode')
        colormode_get = colormode_get.split(',')
        for colormode in colormode_get:
            colormode_v = colormode.split(':')
            self.colormode.append(colormode_v[0])
            self.colormode_bits_depth.append(int(colormode_v[1]))
        print(f'Colormode: {self.colormode}')
        # Init Camera
        self.parent.variables["camera"] = BaslerCamera()
        self.camera_connected = self.parent.variables["camera"].find_first_camera()

    def start_live(self):
        """
        Start live acquisition from camera.
        """
        if self.camera_connected:
            self.thread = QThread()
            self.worker = ImageLive(self)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.image_ready.connect(self.handle_image_ready)
            self.worker.finished.connect(self.thread.quit)

            self.worker.finished.connect(self.worker.deleteLater)
            self.worker.finished.connect(self.thread.deleteLater)

            self.thread.start()

    def stop_live(self):
        """
        Stop live mode, i.e. continuous image acquisition.
        """
        if self.worker is not None:
            try:
                # Stopping worker
                self.worker.stop()
                # Wait end of thread
                if self.thread is not None:
                    self.thread.quit()
                    self.thread.wait(500)  # 500 ms wait
                # Cleaning worker
                self.worker = None
                self.thread = None
            except Exception as e:
                print(f"Error while stopping live: {e}")

    def handle_image_ready(self):
        """
        Action performed when an image is opened via the bot_right widget.
        :return:
        """
        # Update Image
        image = self.parent.variables['image']
        self.top_left.set_image_from_array(image)
        # Update Histo
        self.bot_left.set_image(image, checked=False)

    def display_image(self, image: np.ndarray):
        """
        Display the image given as a numpy array.
        :param image:   numpy array containing the data.
        :return:
        """
        self.top_left.set_image_from_array(image)

    def handle_color_mode_changed(self, event):
        """
        Action performed when the color mode changed.
        """
        try:
            camera = self.parent.variables["camera"]
            # Stop live safely
            self.stop_live()
            # Close camera
            camera.close()
            # Read available formats
            available_formats = []
            try:
                if camera.camera_device is not None:
                    camera.open()
                    available_formats = list(camera.camera_device.PixelFormat.Symbolics)
                    camera.close()
            except Exception as e:
                print(f"Unable to read PixelFormat.Symbolics: {e}")
            # Select new format
            idx = int(event)
            new_format = self.colormode[idx] if idx < len(self.colormode) else None

            if new_format is None:
                return
            if new_format in available_formats:
                camera.open()
                camera.set_parameter("PixelFormat", new_format)
                camera.initial_params["PixelFormat"] = new_format
                camera.close()
            else:
                print(f"Format {new_format} not in available formats: {available_formats}")
            # Change bits depth
            self.parent.variables['bits_depth'] = self.colormode_bits_depth[idx]
            self.bot_left.set_bits_depth(int(self.parent.variables['bits_depth']))
            self.top_left.set_bits_depth(int(self.parent.variables['bits_depth']))
            #self.bot_left.set_image(self.parent.variables['image'], checked=True)
            #self.top_left.set_image(self.parent.variables['image'])
            # Restart live
            camera.open()
            self.start_live()

        except Exception as e:
            print(f"Error in handle_color_mode_changed: {e}")


class ImageLive(QObject):
    image_ready = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, controller: BaslerController):
        super().__init__()
        self.controller = controller
        self._running = False

    def run(self):
        camera = self.controller.parent.variables["camera"]
        self._running = True
        camera.open()
        camera.camera_acquiring = True
        # Running worker
        while self._running:
            try:
                if not self._running:
                    break
                # Image acquisition
                self.controller.parent.variables["image"] = camera.get_image()
                self.image_ready.emit()
            except Exception as e:
                print(f"Get Image Error : {e}")
                break
            time.sleep(0.001)
        # Close worker
        try:
            camera.close()
        except Exception as e:
            print(f"Closing error : {e}")
        camera.camera_acquiring = False
        self.finished.emit()

    def stop(self):
        """
        Stop the worker.
        """
        self._running = False
        time.sleep(0.01)
        try:
            camera = self.controller.parent.variables["camera"]
            if camera.is_open:
                camera.close()
        except Exception as e:
            print(f"Camera close error during stop: {e}")


# TO MOVE TO LENSEPY v2

import os
from pypylon import pylon, genicam


class BaslerCamera:
    """
    Class to manage Basler camera.
    """

    def __init__(self):
        """
        Basler Camera constructor.
        """
        # Variables
        self.camera_device = None
        self.camera_nodemap = None
        self.opened = False
        self.camera_acquiring = False
        self.list_params = {}
        self.initial_params = {}

    @property
    def is_open(self):
        return self.opened and self.camera_device is not None and self.camera_device.IsOpen()

    def find_first_camera(self) -> bool:
        """

        :return:
        """
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()
        # Check if almost one camera is available.
        if not devices:
            return False
        else:
            # Create an instance of a Basler Camera (using pypylon wrapper).
            self.camera_device = pylon.InstantCamera(tl_factory.CreateDevice(devices[0]))
            self.camera_nodemap = self.camera_device.GetNodeMap()
            self._list_parameters()
            # self.init_camera_parameters('./config/camera.ini')
            return True

    def get_image(self):
        """
        Get image from the camera.
        :return:    Array containing the image.
        """
        if self.camera_acquiring:
            # Test if the camera is opened
            if not self.camera_device.IsOpen():
                self.camera_device.Open()
            # Test if the camera is grabbing images
            if not self.camera_device.IsGrabbing():
                self.camera_device.StopGrabbing()

            # Create a list of images
            self.camera_device.StartGrabbingMax(1)
            grab_result = self.camera_device.RetrieveResult(100000, pylon.TimeoutHandling_ThrowException)

            if grab_result.GrabSucceeded():
                image = grab_result.Array
            else:
                image = None
            print(f'Init Image Type = {image.dtype}')
            # Free memory
            grab_result.Release()
            if image is not None and image.size > 0:
                if 'PixelFormat' in self.initial_params:
                    pixel_format = self.initial_params['PixelFormat']
                    if "Bayer" in pixel_format:
                        image = cv2.cvtColor(image, cv2.COLOR_BAYER_RG2RGB)
            return image
        return None

    def disconnect(self):
        """
        Disconnect the camera.
        """
        self.camera_device = None

    def open(self):
        """
        Open camera.
        """
        if self.camera_device is not None:
            if not self.opened:
                self.camera_device.Open()
                self.opened = True

    def close(self):
        """
        Open camera.
        """
        if self.camera_device is not None:
            if self.opened:
                self.camera_device.Close()
                self.opened = False

    def init_camera_parameters(self, filepath: str):
        """
        Initialize camera accessible parameters of the camera from a file.
        The txt file should have the following format:
        # comment
        key_1;value1;type1
        key_2;value2;type2

        :param filepath:    Name of a txt file containing the parameters to setup.
        """
        self.open()
        self.initial_params = {}
        if os.path.exists(filepath):
            # Read the CSV file, ignoring lines starting with '//'
            data = np.genfromtxt(filepath, delimiter=';',
                                 dtype=str, comments='#', encoding='UTF-8')
            # Populate the dictionary with key-value pairs from the CSV file
            for key, value, typ in data:
                match typ:
                    case 'I':
                        self.initial_params[key.strip()] = int(value.strip())
                    case 'F':
                        self.initial_params[key.strip()] = float(value.strip())
                    case 'B':
                        self.initial_params[key.strip()] = value.strip() == "True"
                    case _:
                        self.initial_params[key.strip()] = value.strip()
                self.set_parameter(key, self.initial_params[key.strip()])
        else:
            print('File error')
        self.close()

    def _list_parameters(self):
        """
        Update the list of accessible parameters of the camera.
        """
        self.open()
        self.list_params = [x for x in dir(self.camera_device) if not x.startswith("__")]
        print(self.list_params)

        for attr in self.list_params:
            try:
                node = self.camera_nodemap.GetNode(attr)
                if hasattr(node, "GetValue"):
                    pass
                elif hasattr(node, "Execute"):
                    self.list_params.remove(attr)
                else:
                    self.list_params.remove(attr)
            except Exception as e:
                self.list_params.remove(attr)
        self.close()

    def get_list_parameters(self) -> list:
        """
        Get the list of the accessible parameters of the camera.
        :return:    List of the accessible parameters of the camera.
        """
        return self.list_params

    def get_parameter(self, param):
        """
        Get the value of a camera parameter.
        The accessibility of the parameter is verified beforehand.
        :param param:   Name of the parameter.
        :return:        Value of the parameter if exists, else None.
        """
        if param in self.list_params:
            node = self.camera_nodemap.GetNode(param)
            if hasattr(node, "GetValue"):
                return node.GetValue()
            else:
                return None
        else:
            return None

    def set_parameter(self, param, value):
        """
        Set a camera parameter to a specific value.
        The accessibility of the parameter is verified beforehand.
        :param param:   Name of the parameter.
        :param value:   Value to give to the parameter.
        """
        if param in self.list_params:
            self.open()
            node = self.camera_nodemap.GetNode(param)
            try:
                if hasattr(node, "GetAccessMode") and node.GetAccessMode() == genicam.RW:
                    if hasattr(node, "SetValue"):
                        node.SetValue(value)
                        self.close()
                        return True
                    else:
                        print(f"Node {param} has no SetValue()")
                else:
                    print(f"Node {param} not writable or invalid access mode")
            except Exception as e:
                print(f"Error setting parameter {param}: {e}")
        else:
            print(f"Parameter {param} not found in list_params")
        self.close()
        return False


if __name__ == "__main__":
    camera = BaslerCamera()
    camera.find_first_camera()
    camera.set_parameter('ExposureTime', 10000)
    camera.set_parameter('PixelFormat', 'Mono12')
    camera.camera_acquiring = True
    image = camera.get_image()
    camera.camera_acquiring = False

    print(f'Image Shape = {image.shape} / Dtype = {image.dtype}')
    camera.disconnect()

    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(image)


    hist, bins = np.histogram(image, bins=4096, range=(0, 4095))

    # Affichage
    plt.figure(figsize=(8,4))
    plt.bar(bins[:-1], hist, width=1, color='black')
    plt.title("Histogramme de l'image")
    plt.xlabel("Intensité des pixels")
    plt.ylabel("Nombre de pixels")
    plt.show()
