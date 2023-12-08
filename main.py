import datetime
from vlan import prompt_for_vlan
from configs import prompt_for_config, generate_vlan_conf

VERSION = '0.0.0-super-duper-beta-alpha'
YES: tuple[str] = ('yes', 'ye', 'y', 'ja', 'japp', 'fosho')
NO:  tuple[str] = ('no', 'n', 'nope', 'nej', 'stop', 'exit', '#metoo')

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

    hostname = f'R{host_number}'
    dt = datetime.datetime.now().strftime('%H:%M:%S %d %h %Y')

    host_number += 1
    num_routers -= 1

# Config Swiches
host_number = 1
while num_switches > 0:

    hostname = f'S{host_number}'
    dt = datetime.datetime.now().strftime('%H:%M:%S %d %h %Y')
    
    if vlans is not None:
        print('CONF VLAN')

    host_number += 1
    num_switches -= 1