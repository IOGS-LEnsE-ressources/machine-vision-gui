from pypylon import pylon, genicam
import numpy as np
import os

class CameraBasler:
    """
    Basler Camera Wrapper, using pypylon package.

    """
    def __init__(self):
        self.tl_factory = pylon.TlFactory.GetInstance()
        self.camera = None
        self.is_open = False
        # Parameters
        self.parameters_value = {}
        self.parameters_type = {}
        self.camera_nodemap = None

    def find_first_camera(self):
        devices = self.tl_factory.EnumerateDevices()
        if len(devices) == 0:
            return False
        self.camera = pylon.InstantCamera(self.tl_factory.CreateDevice(devices[0]))
        self.camera_nodemap = self.camera.GetNodeMap()
        self.camera.DeviceReset()
        return True

    def open(self):
        if self.camera is None:
            return False
        if not self.is_open:
            self.camera.Open()
            self.is_open = True
            return True
        return False

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

    def grab_frame(self, timeout=3000000):
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

    def is_connected(self):
        return self.camera is not None

    def is_opened(self):
        return self.is_open

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
        if param in self.parameters_value:
            node = self.camera_nodemap.GetNode(param)

            if node.GetAccessMode() == genicam.RW:
                if hasattr(node, "SetValue"):
                    node.SetValue(value)
                    return True
                else:
                    print(f"Parameter {param} was not modified.")
                    return False
            else:
                print(f"Parameter {param} is not writable.")
                return False
        else:
            return False

    def init_camera_parameters(self, filepath: str):
        """
        Initialize camera accessible parameters of the camera from a file.
        The txt file should have the following format:
        # comment
        key_1;value1;type1
        key_2;value2;type2

        :param filepath:    Name of a txt file containing the parameters to setup.
        """
        self.parameters_value = {}
        self.parameters_type = {}
        self.camera.Open()
        if os.path.exists(filepath):
            # Read the CSV file, ignoring lines starting with '//'
            data = np.genfromtxt(filepath, delimiter=';',
                                 dtype=str, comments='#', encoding='UTF-8')
            # Populate the dictionary with key-value pairs from the CSV file
            for key, value, typ in data:
                match typ:
                    case 'I':
                        self.parameters_value[key.strip()] = int(value.strip())
                        self.parameters_type[key.strip()] = 'I'
                    case 'F':
                        self.parameters_value[key.strip()] = float(value.strip())
                        self.parameters_type[key.strip()] = 'F'
                    case 'B':
                        self.parameters_value[key.strip()] = value.strip() == "True"
                        self.parameters_type[key.strip()] = 'B'
                    case _:
                        self.parameters_value[key.strip()] = value.strip()
                        self.parameters_type[key.strip()] = 'N'
                self.set_parameter(key, self.parameters_value[key.strip()])
        else:
            print('File error')
        self.camera.Close()


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    my_cam = CameraBasler()

    if my_cam.find_first_camera():
        print('Camera connected')

    if my_cam.is_connected():
        print('Connecté')
        my_cam.init_camera_parameters('../config/initial_params.txt')

        my_cam.start_grabbing()
        frame = my_cam.grab_frame()
        print(f'Frame : {frame.dtype} / {frame.shape}')
        my_cam.stop_grabbing()

        plt.imshow(frame)
        plt.show()

        ### Camera response
        # Test with different exposure time
        expo_time_list = [20, 20000, 100000, 250000, 500000, 1000000, 1500000, 2000000]
        mean_value = []
        stddev_value = []

        my_cam.open()
        my_cam.start_grabbing()
        for expo_time in expo_time_list:
            my_cam.set_parameter('ExposureTime', expo_time)
            frame = my_cam.grab_frame()

            m_v = np.mean(frame)
            std_v = np.std(frame)
            mean_value.append(m_v)
            stddev_value.append(std_v)

        my_cam.stop_grabbing()
        my_cam.close()

        expo_times = np.array(expo_time_list)
        mean_value = np.array(mean_value)
        mean_value = mean_value - mean_value[0]

        plt.figure()
        plt.plot(expo_times, mean_value)
        plt.title('Mean value of intensity')
        plt.figure()
        plt.plot(expo_times, np.array(stddev_value))
        plt.title('Standard deviation value of intensity')
        plt.show()