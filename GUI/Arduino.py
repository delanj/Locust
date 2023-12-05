import threading

import pyfirmata
from playsound import playsound
from pyfirmata import Arduino, util, STRING_DATA
import serial.tools.list_ports
import time

def find_arduino_port():
    try:
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "usbmodem" in port.device.lower():
                return port.device
    except Exception as e:
        print(f"Error finding Arduino port: {e}")
    return None

def connect_to_arduino(port):
    try:
        board = Arduino(port)
        return board
    except Exception as e:
        print(f"Error connecting to Arduino: {e}")
        return None

arduino_port = find_arduino_port()
#board = Arduino("/dev/cu.usbmodem14201")
arduino_board = None
if arduino_port is not None:
    board = connect_to_arduino(arduino_port)
    # RBG LED PIN
    red_pin = 10
    green_pin = 9
    blue_pin = 6

    # Set up the RGB LED
    board.digital[red_pin].mode = pyfirmata.PWM  # Corrected line
    board.digital[green_pin].mode = pyfirmata.PWM  # Corrected line
    board.digital[blue_pin].mode = pyfirmata.PWM  # Corrected line


    def set_rgb_color(red, green, blue):
        board.digital[red_pin].write(red / 255)
        board.digital[green_pin].write(green / 255)
        board.digital[blue_pin].write(blue / 255)


    def arduino_controller(color):
        if color == "red":
            set_rgb_color(255, 0, 0)
            time.sleep(5)
            set_rgb_color(0, 0, 0)
        if color == "green":
            set_rgb_color(0, 255, 0)
            time.sleep(5)
            set_rgb_color(0, 0, 0)


    def run_arduino_controller(color):
        arduino_thread = threading.Thread(target=arduino_controller, args=(color,))
        arduino_thread.start()
else:
    print("running without arduino")



#