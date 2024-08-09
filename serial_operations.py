import serial
import time
import serial.tools.list_ports

def setup_serial_connection(port, baudrate, timeout=1):
    ser = serial.Serial(port, baudrate, timeout=timeout)
    time.sleep(2)
    return ser

def send_command(ser, command):
    ser.write(command.encode())

def read_response(ser):
    response = ser.readline().decode().strip()
    return response

def close_serial_connection(ser):
    ser.close()

def find_busy_tag_device():
    ports = serial.tools.list_ports.comports()
    for port_info in ports:
        port = port_info.device
        try:
            ser = serial.Serial(port, baudrate=115200, timeout=1)
            ser.write(b'AT+GDN\r\n')
            response = ser.readline().decode('utf-8').strip()
            ser.close()
            if response.startswith("+DN:busytag-"):
                return port
        except (serial.SerialException, UnicodeDecodeError):
            continue
    return None