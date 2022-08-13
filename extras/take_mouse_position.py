import time
from pynput.mouse import Controller
mouse = Controller()

time.sleep(1)
position = mouse.position
print(position)

time.sleep(20)
