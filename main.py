import datetime
from time import sleep
from vlan import prompt_for_vlan
from configs import prompt_for_config, generate_vlan_conf
from terrible_term import TerribleTerm

VERSION = '0.0.0-super-duper-beta-alpha'
YES: tuple[str] = ('yes', 'ye', 'y', 'ja', 'japp', 'fosho')
NO:  tuple[str] = ('no', 'n', 'nope', 'nej', 'stop', 'exit', '#metoo')

serial_port = input('Serial Ports [COM1]: ')

if '' == serial_port:
    serial_port = 'COM1'

print('Enter number of devices')
num_routers = ''
num_switches = ''

while not num_routers.isnumeric():
    num_routers = input('How many Routers [0]: ')
    if '' == num_routers:
        num_routers = '0'

while not num_switches.isnumeric():
    num_switches = input('How many Swiches [0]: ')
    if '' == num_switches:
        num_switches = '0'

num_routers = int(num_routers)
num_switches = int(num_switches)
tot_devices = num_routers + num_switches

if tot_devices < 1:
    print('No devices to conf.')
    print('Exiting script')
    exit()

vlans = None
if num_switches > 0:
    print('Do you want to add VLANs to the switches?')
    add_vlans = input('Yes/no [no]> ')
    if add_vlans in YES:
        vlans = generate_vlan_conf(prompt_for_vlan())


config = None
while config is None:
    config = prompt_for_config()

# Config Routers
host_number = 1
while num_routers > 0:

    
    tt = TerribleTerm(serial_port)
    hostname = f'R{host_number}'

    print(f'Press Enter to configure {hostname}')
    rdy = input()
    

    TTL = 10
    while tt.mode != 'USER EXEC':
        if TTL < 1:
            break

        print('Not in USER EXEC mode')
        print('Attempting to enter mode')
        tt.go_to_user_exec()
        sleep(0.2)
        
        TTL -= 1
        
    
    hostname = f'R{host_number}'
    dt = datetime.datetime.now().strftime('%H:%M:%S %d %h %Y')
    for cmd in config(hostname, dt):
        tt.send_command(cmd)

    tt.close()
    host_number += 1
    num_routers -= 1

# Config Swiches
host_number = 1
while num_switches > 0:
    
    tt = TerribleTerm(serial_port)
    hostname = f'S{host_number}'
    dt = datetime.datetime.now().strftime('%H:%M:%S %d %h %Y')

    print(f'Press Enter to configure {hostname}')
    rdy = input()

    TTL = 10
    while tt.mode != 'USER EXEC':
        if TTL < 1:
            break

        print('Not in USER EXEC mode Attempting to enter mode')
        print('We are in ' + tt.mode)
        tt.go_to_user_exec()
        tt.send_command()
        TTL -= 1

    if tt.mode != 'USER EXEC':
        print('Error: Could not enter USER EXEC mode')
        tt.close()
        break
    else:
        print('We are in USER EXEC mode')

    for cmd in config(hostname, dt):
        tt.send_command(cmd)
        
    if vlans is not None:
        print(f'Configure VLAN on {hostname}?')
        rdy = input('Yes/No [Yes]: ')
        if rdy in YES or rdy == '':
            tt.go_to_priv_exec()
            tt.send_command('conf t')
            for vlan_cmd in vlans:
                tt.send_command(vlan_cmd)
    
    tt.close()
    tt = None
    host_number += 1
    num_switches -= 1
