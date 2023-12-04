import serial
import time

arduino_port = 'COM3'
arduino_baudrate = 9600

ser = serial.Serial(arduino_port, arduino_baudrate, timeout=1)
time.sleep(2)

previous_status = None
isFull = False

try:
    while True:
        # Trigger the ultrasonic sensors
        ser.write(b'H')  # 'H' is just a signal to Arduino to start measuring
        # Read the parking status from Arduino
        arduino_data = ser.readline().rstrip()

        if arduino_data:
            status = int(arduino_data.decode('utf-8'))

            if status == 3:
                current_status = "Both Taken"
                isFull = True
            elif status == 2:
                current_status = "Space 1 Taken"
                isFull = False
            elif status == 1:
                current_status = "Space 2 Taken"
                isFull = False
            else:
                current_status = "None Taken"
                isFull = False

            if current_status != previous_status:
                print("Parking space status:", current_status)
                previous_status = current_status

        time.sleep(1)  # Adjust the delay as needed

except KeyboardInterrupt:
    print("Exiting program")

finally:
    ser.close()
