import serial
import re
from time import sleep

HOSTNAME_PATTERN = '[A-z][\-A-z0-9]{0,62}'
MODE_PATTERNS = [
    {
        'name': 'USER EXEC',
        'pattern': HOSTNAME_PATTERN + '>'
    },
    {
        'name': 'PRIVILEGED EXEC',
        'pattern': HOSTNAME_PATTERN + '#'
    },
    {
        'name': 'GLOBAL CONFIGURATION',
        'pattern': HOSTNAME_PATTERN + '\(config\)#'
    },
    {
        'name': 'LINE',
        'pattern': HOSTNAME_PATTERN + '\(config\-line\)#'
    },
    {
        'name': 'INTERFACE',
        'pattern': HOSTNAME_PATTERN + '\(config-if\)#'
    },
    {
        'name': 'VLAN',
        'pattern': HOSTNAME_PATTERN + '\(config-VLAN\)#'
    }
]

class TerribleTerm:

    sh: serial.Serial
    mode: str = ''
    output: str = ''
    
    def __init__(self, port):
        # Our Serial Connection
        self.sh = serial.Serial(
            port = port,
            baudrate = 9600,
            parity   = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout  = 6
        )
        # Open connection if it's not open
        self.open()
        
        # Send <cr> to populate the class/obj
        self.send_command()

    def go_to_user_exec(self):
        if self.mode == 'PRIVILEGED EXEC':
            self.send_command('exit')
            self.send_command()
            
        elif self.mode == 'USER EXEC':
            return None
        else:
            self.send_command('end')
            self.send_command('exit')
    
    def go_to_priv_exec(self):
        if self.mode == 'PRIVILEGED EXEC':
            return None
        elif self.mode == 'USER EXEC':
            self.send_command('enable')
        else:
            self.send_command('end')
        
    # Update the mode attribute to reflect our current position.
    def set_mode(self, output):
        
        for pattern in MODE_PATTERNS:
            if re.match(pattern['pattern'], output) is not None:
                self.mode = pattern['name']
                break

    # Send command over the conection.
    def send_command(self, cmd='', EOL='\r'):
        if self.sh.isOpen():
            cmd += EOL
            self.sh.write(cmd.encode('utf-8', 'strict'))
            sleep(0.3)
            self.read_output()
            sleep(0.1)
            
    # Read the output and store it in output attribute.
    def read_output(self):
        out = self.sh.read(self.sh.in_waiting)
        self.output = str(out.decode('utf-8', 'strict')).strip()
        self.set_mode(self.output)
        print(self.output)
        

    # Close the Connection if it's open
    def close(self):
        if self.sh.isOpen():
            self.sh.close()
    # Open the Connection if it's closed.
    def open(self):
        if not self.sh.isOpen():
            self.sh.open()
            

