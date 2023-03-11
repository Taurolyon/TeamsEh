import ctypes
import time
import random
import psutil
import os
import subprocess

# Import the required DLLs
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
shell32 = ctypes.windll.shell32
advapi32 = ctypes.windll.advapi32

# Define constants for mouse and keyboard events
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002

# Define a subclass of ctypes.Structure for the LASTINPUTINFO structure
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', ctypes.c_uint),
        ('dwTime', ctypes.c_ulong)
    ]

# Define a function to check for keyboard and mouse activity
def check_activity():
    last_input_info = LASTINPUTINFO()
    last_input_info.cbSize = ctypes.sizeof(last_input_info)
    user32.GetLastInputInfo(ctypes.byref(last_input_info))
    elapsed_seconds = kernel32.GetTickCount() - last_input_info.dwTime
    countdown = 120 - elapsed_seconds // 1000
    if countdown >= 0:
        print(f"{countdown} seconds until activity needed...")
    return elapsed_seconds < 120000

# Define a function to simulate mouse movement
def move_mouse():
    x, y = random.randint(0, 65535), random.randint(0, 65535)
    user32.mouse_event(MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, x, y, 0, 0)

# Define a function to simulate keyboard input
def press_key(key):
    user32.keybd_event(key, 0, KEYEVENTF_EXTENDEDKEY, 0)
    user32.keybd_event(key, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

# Define a function to check if Teams is running
def is_teams_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'Teams.exe':
            return True
    return False

# Define a function to launch Teams
def launch_teams():
    username = get_current_user()
    command = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Teams', 'current', 'Teams.exe')
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.lpDesktop = 'winsta0\\default'
    with open(os.devnull, 'w') as output_file:
        subprocess.Popen([command], startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE, stdout=output_file, stderr=output_file)

# Define a function to get the current user
def get_current_user():
    output = subprocess.check_output('whoami')
    username = output.decode().strip().split('\\')[-1]
    return username

# Check if Teams is running on start, and launch Teams if it's not
if not is_teams_running():
    print("Teams is not running. Launching Teams...")
    launch_teams()
else:
    print("Teams is already running...")

# Loop indefinitely, simulating activity if no input is detected for 2 minutes
while True:
    if not is_teams_running():
        print("Teams is no longer running. Exiting program.")
        os._exit(1) # Exit the program
    elif not check_activity():
        print("No activity detected. Simulating Activity.")
        move_mouse()
        time.sleep(1)
        press_key(0x10) # Press the Shift key
        time.sleep(1)
    else:
        time.sleep(1)
