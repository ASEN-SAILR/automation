import sys
sys.path.append('../.')
sys.path.append('.')

from RoverUART import RoverUART

if __name__ == "__main__":
    teensy_port = '/dev/ttyACM0' # <- check this
    uart = RoverUART(teensy_port=teensy_port)

    # rotation
    deg = input("enter value to rotate: ")
    print(f"testing uart.sendRotateCmd({deg})")
    uart.sendRotateCmd(deg)
    returned = uart.readLine()
    print(f"read \"{returned}\" from the teensy")

    # translation
    dist = input("enter value to translate: ")
    print(f"testing uart.sendTranslateCmd({dist})")
    uart.sendTranslateCmd(dist)
    returned = uart.readLine()
    print(f"read \"{returned}\" from the teensy")

    # magnetometer
    _ = input("hit enter to send magnetometer request ")
    print(f"testing uart.getMagneticAzm()")
    uart.getMagneticAzm()
    returned = uart.readLine()
    print(f"read \"{returned}\" from the teensy")

    # stop
    _ = input("hit enter to send stop request ")
    print(f"testing uart.sendStopCmd()")
    uart.sendStopCmd()
    returned = uart.readLine()
    print(f"read \"{returned}\" from the teensy")



