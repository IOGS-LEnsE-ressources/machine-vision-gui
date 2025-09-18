
from pypylon import pylon

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
