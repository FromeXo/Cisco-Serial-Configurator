from time import sleep
import serial
from confs import EOL

sus_prompts = [
    b'Would you like to enter the initial configuration dialog? [yes/no]: \r\n',
    b'Would you like to enter the initial configuration dialog? [yes/no]: \r\n',
    b"% Please answer 'yes' or 'no'.\r\n"]

MODES_USER_EXEC = [b'Switch>\r\n', b'Router>\r\n']

def send_commands(serial_port, commands:list[str]):
    ser = serial.Serial(
        port     = serial_port,
        baudrate = 9600,
        parity   = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout  = 2)

    ser.isOpen()

    ser.write(str.encode(EOL))
    out = ser.readline()
    
    # Time To Loop
    TTL = 20
    while out not in MODES_USER_EXEC:
        print(out)    
        ser.write(str.encode(EOL))
        out = ser.readline()
        sleep(0.1)
        if out in sus_prompts:
            ser.write(str.encode('no' + EOL))
            out = ser.readline()
        if TTL == 0:
            break
        else:
            TTL -= 1
    
    
    for command in commands:
        ser.write(str.encode(command))
        out = bytes()
        sleep(0.1)
        out = ser.readline()
        out = out.decode('utf-8')
        
        print(out)
    
    ser.close()
    
