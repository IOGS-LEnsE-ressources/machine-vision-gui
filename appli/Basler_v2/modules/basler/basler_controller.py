import time
from PyQt6.QtCore import QObject, QThread
from _app.template_controller import TemplateController
from modules.basler.basler_views import *
from lensepy.pyqt6.widget_image_display import ImageDisplayWidget


class BaslerController(TemplateController):
    """

    """

    def __init__(self, parent=None):
        """

        """
        super().__init__(parent)
        self.top_left = ImageDisplayWidget()
        self.bot_left = HistogramWidget()
        self.bot_right = QWidget()
        self.top_right = CameraInfosWidget()
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
        self.camera_acquiring = False       # Camera is acquiring
        self.thread = None
        self.worker = None

        # Signals

        # Init Camera
        self.init_camera()
        # Start thread
        self.start_live()

    def init_camera(self):
        """

        :return:
        """
        self.parent.variables["camera"] = BaslerCamera(self)
        self.camera_connected = self.parent.variables["camera"].find_first_camera()
        print(f'Camera =: {self.parent.variables["camera"]}')

    def start_live(self):
        """
        Start live acquisition from camera.
        """
        self.thread = QThread()
        self.worker = ImageLive(self)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.image_ready.connect(self.action_image_ready)
        self.worker.finished.connect(self.thread.quit)

        self.thread.start()

    def action_image_ready(self):
        """
        Action performed when an image is opened via the bot_right widget.
        :return:
        """
        # Update Image
        image = self.parent.variables['image']
        self.top_left.set_image_from_array(image)
        # Update Histo
        self.bot_left.set_image(image)

    def display_image(self, image: np.ndarray):
        """
        Display the image given as a numpy array.
        :param image:   numpy array containing the data.
        :return:
        """
        self.top_left.set_image_from_array(image)



class ImageLive(QObject):
    image_ready = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, controller: BaslerController):
        super().__init__()
        self.controller = controller
        self._running = True

    def run(self):
        camera = self.controller.parent.variables["camera"]
        while self._running:
            if not self.controller.camera_acquiring:
                print("Start ACQUISITION")
                camera.open()
                self.controller.camera_acquiring = True
            # Update image
            self.controller.parent.variables["image"] = camera.get_image()
            #time.sleep(0.001)
            self.image_ready.emit()
        self.finished.emit()

    def stop(self):
        camera = self.controller.parent.variables["camera"]
        camera.close()
        self._running = False

# TO MOVE TO LENSEPY v2

import os
from pypylon import pylon


class BaslerCamera:
    """
    Class to manage Basler camera.
    """

    def __init__(self, controller: BaslerController):
        """

        :param controller:  Basler controller.
        """
        self.controller = controller
        # Variables
        self.camera_device = None
        self.camera_nodemap = None
        self.opened = False
        self.initial_params = {}

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

        :return:
        """
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
        # Free memory
        grab_result.Release()
        return image

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
            node = self.camera_nodemap.GetNode(param)

            if node.GetAccessMode() == genicam.RW:
                if hasattr(node, "SetValue"):
                    node.SetValue(value)
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False