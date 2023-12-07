import time
import datetime
import terrible_term
import confs



serial_port = input('Serial Ports [COM1]: ')

if '' == serial_port:
    serial_port = 'COM1'

print('Enter number of devices')
num_routers = ''
num_swiches = ''
tot_devices = 0

while not num_routers.isnumeric():
    num_routers = input('How many Routers [0]: ')
    if '' == num_routers:
        num_routers = '0'

while not num_swiches.isnumeric():
    num_swiches = input('How many Swiches [0]: ')
    if '' == num_swiches:
        num_swiches = '0'

num_routers = int(num_routers)
num_swiches = int(num_swiches)
tot_devices = num_routers + num_swiches

if tot_devices < 1:
    print('No devices to conf.')
    print('Exiting script')
    exit()

while tot_devices > 0:

    r_hostname = 1
    s_hostname = 1
    
    while num_routers > 0:
        hostname = 'R' + str(r_hostname)
        dt = datetime.datetime.now().strftime('%H:%M:%S %d %h %Y')

        print('Select config')
        print('1: Slim Base Conf')
        print('2: Base Conf')
        print('3: Base Conf with SSH')
        conf = int(input('Conf [1]: '))
        if conf == 1 or conf == 0:
            config =  confs.slim_base_config(hostname, dt) 
        elif conf == 2:
            config =  confs.base_config(hostname, dt) 
        elif conf == 3:
            config =  confs.ssh_base_config(hostname, dt) 
        
        print(f'Connect {hostname} to serial port, then press enter')
        input()

        terrible_term.send_commands(serial_port, config)
        
        r_hostname += 1
        num_routers -= 1

    while num_swiches > 0:
        hostname = 'S' + str(s_hostname)
        dt = datetime.datetime.now().strftime('%H:%M:%S %d %h %Y')

        print('Select config')
        print('1: Slim Base Conf')
        print('2: Base Conf')
        print('3: Base Conf with SSH')
        conf = int(input('Conf [1]: '))
        if conf == 1 or conf == 0:
            config =  confs.slim_base_config(hostname, dt) 
        elif conf == 2:
            config =  confs.base_config(hostname, dt) 
        elif conf == 3:
            config =  confs.ssh_base_config(hostname, dt) 
        
        print(f'Connect {hostname} to serial port, then press enter')
        input()

        terrible_term.send_commands(serial_port, config)
        
        s_hostname += 1
        num_swiches -= 1

    tot_devices -= 1
#
print('#############################')
print('User PW: cisco')
print('Enable PW: class')
print('SSH User: admin')
print('SSH Pass: class')
print('#############################')
