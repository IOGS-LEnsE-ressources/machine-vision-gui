
from pypylon import pylon
from lensecam.basler.camera_basler import CameraBasler

import time
import numpy as np
from matplotlib import pyplot as plt

'''
from camera_list import CameraList

# Create a CameraList object
cam_list = CameraList()
# Print the number of camera connected
print(f"Test - get_nb_of_cam : {cam_list.get_nb_of_cam()}")
# Collect and print the list of the connected cameras
cameras_list = cam_list.get_cam_list()
print(f"Test - get_cam_list : {cameras_list}")

cam_id = 'a'
while cam_id.isdigit() is False:
    cam_id = input('Enter the ID of the camera to connect :')
cam_id = int(cam_id)
print(f"Selected camera : {cam_id}")

# Create a camera object
my_cam_dev = cam_list.get_cam_device(cam_id)
'''
my_cam_dev = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

my_cam = CameraBasler(my_cam_dev)
my_cam.init_camera()
my_cam.init_camera_parameters('params_Basler.txt')

if my_cam.set_frame_rate(5):
    print('FPS  OK')

# Change colormode to Mono12
my_cam.set_color_mode('Mono12')
my_cam.set_display_mode('Mono12')
print(my_cam.get_color_mode())

# Set AOI
w = 400
y0 = (1936 // 2) - (w // 2)
x0 = (1216 // 2) - (w // 2)
print(f'x0 = {x0} / y0 = {y0} / w = {w}')
if my_cam.set_aoi(x0, y0, w, w):
    print('AOI OK')
if my_cam.set_black_level(10):
    print('BL = 10')

# Test with different exposure time
expo_time_list = [20, 20000, 100000, 250000, 500000, 1000000, 1500000, 2000000]
mean_value = []
stddev_value = []

my_cam.set_exposure(20)
time.sleep(0.1)
image_0 = my_cam.get_images(1)
time.sleep(0.1)

m_v_0 = np.mean(image_0)
std_v_0 = np.std(image_0)

for expo_time in expo_time_list:
    print(expo_time)
    my_cam.set_exposure(expo_time)
    time.sleep(0.1)
    my_cam.camera_device.Open()
    print(f'FPS = {my_cam.camera_device.ResultingFrameRate.Value}')
    my_cam.camera_device.Close()
    time.sleep(0.1)
    images = my_cam.get_images(1)
    time.sleep(0.1)

    m_v = np.mean(images) - m_v_0
    std_v = np.std(images) - std_v_0
    mean_value.append(m_v)
    stddev_value.append(std_v)

    print(m_v)

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

'''
# display image
from matplotlib import pyplot as plt

plt.imshow(images[0], interpolation='nearest', cmap='gray')
plt.show()
'''

'''
if my_cam.set_aoi(200, 300, 500, 400):
    print('AOI OK')
    # Test to catch images
    st = time.time()
    images = my_cam.get_images()
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    print('\tExecution time:', elapsed_time, 'seconds')  
    print(images[0].shape)      
'''
'''
# Different exposure time
my_cam.reset_aoi()

t_expo = np.linspace(t_min, t_max/10000.0, 11)
for i, t in enumerate(t_expo):
    print(f'\tExpo Time = {t}us')
    my_cam.set_exposure(t)
    images = my_cam.get_images()
    plt.imshow(images[0], interpolation='nearest')
    plt.show()        
'''
'''
# Frame Rate
ft_act = my_cam.get_frame_rate()
print(f'Actual Frame Time = {ft_act} fps')
my_cam.set_frame_rate(20)
ft_act = my_cam.get_frame_rate()
print(f'New Frame Time = {ft_act} fps')

# BlackLevel
bl_act = my_cam.get_black_level()
print(f'Actual Black Level = {bl_act}')
my_cam.set_black_level(200)
bl_act = my_cam.get_black_level()
print(f'New Black Level = {bl_act}')
'''



'''



# Get all devices
tlFactory = pylon.TlFactory.GetInstance()
devices = tlFactory.EnumerateDevices()
camera_connected = False
my_cam = None

def get_node_info(cam, param):
    nodemap = cam.GetNodeMap()

    try:
        node = nodemap.GetNode(param)
        if hasattr(node, "GetValue"):
            val = node.GetValue()
            if hasattr(node, "GetDescription"):
                desc = node.GetDescription()
            else:
                desc = None
            return val, desc
        elif hasattr(node, "Execute"):
            return 'CMD', None
        else:
            return 'NOP', None
    except Exception:
        return 'NOP', None

def set_node_value(cam, param, value):
    nodemap = cam.GetNodeMap()
    node = nodemap.GetNode(param)
    if hasattr(node, "SetValue"):
        node.SetValue(value)
        print(f"{param} modified : {node.GetValue()}")
    else:
        print(f"{param} CAN'T BE MODIFIED")


# If almost 1 device connected...
if len(devices) > 0:
    if len(devices) == 1:
        my_dev = pylon.TlFactory.GetInstance()
    else:
        my_dev = pylon.TlFactory.GetInstance()[0]
    # Create camera object from the first devices
    my_cam = pylon.InstantCamera(my_dev.CreateFirstDevice())
    if my_cam is not None:
        camera_connected = True
        cam_info = my_cam.GetDeviceInfo()
        print(f'Camera Connected - {cam_info.GetModelName()} / ID : {cam_info.GetSerialNumber()}')
        print(f'\tType : {cam_info.GetDeviceClass()}')
        print(f'\tFirmWare : {cam_info.GetDeviceVersion()}\n')


if camera_connected:
    # Access to the different parameters
    my_cam.Open()
    cam_params = [x for x in dir(my_cam) if not x.startswith("__")]

    for attr in cam_params:
        value, desc = get_node_info(my_cam, attr)
        print(f"{attr} \t = {value}")
        if desc is not None:
            print(f"\tDesc : {desc}")

    set_node_value(my_cam, "BalanceWhiteAuto", "Off")


    my_cam.Close()

'''