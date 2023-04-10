import sys
sys.path.append('../.')
sys.path.append('.')

from RoverUART import RoverUART
import time

if __name__ == "__main__":
    teensy_port = '/dev/ttyACM1' # <- check this
    uart = RoverUART(teensy_port=teensy_port)
    time.sleep(0.5)
    _ = uart.readAll()
    
    # rotation
    deg = input("enter value to rotate: ")
    print(f"testing uart.sendRotateCmd({deg})")
    uart.sendRotateCmd(deg)
    time.sleep(0.25)
    returned = uart.readAll()
    print(f"read \"{returned}\" from the teensy")

    # translation
    dist = input("enter value to translate: ")
    print(f"testing uart.sendTranslateCmd({dist})")
    uart.sendTranslateCmd(dist)
    time.sleep(0.25)
    returned = uart.readAll()
    print(f"read \"{returned}\" from the teensy")

    # magnetometer
    _ = input("hit enter to send magnetometer request ")
    print(f"testing uart.getMagneticAzm()")
    num = uart.getMagneticAzm()
    # returned = uart.readAll()
    print(f"read \"{num}\" from the teensy. Extra characters in serial buffer: ")

    # stop
    _ = input("hit enter to send stop request ")
    print(f"testing uart.sendStopCmd()")
    uart.sendStopCmd()
    returned = uart.readAll()
    print(f"read \"{returned}\" from the teensy")



