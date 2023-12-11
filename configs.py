
def slim_config(hostname, date_time) -> list[str]:
    return [
        'enable',
        'clock set ' + date_time,
        'configure terminal',
        'no ip domain-lookup',
        'hostname ' + hostname,
        'line console 0',
        'logging synchronous',
        'exit',
        'line vty 0 15',
        'logging synchronous',
        'end',
        'wr'
    ]

def base_config(hostname, date_time) -> list[str]:
    banner = '\nAuthorized personnel only\n'
    return [
        'enable',
        'clock set ' + date_time,
        'configure terminal',
        'no ip domain-lookup',
        'banner motd #' + banner + '#',
        'enable secret class',
        'service password-encryption',
        'hostname ' + hostname,
        'line console 0',
        'password cisco',
        'login',
        'logging synchronous',
        'exit',
        'line vty 0 15',
        'password cisco',
        'login',
        'logging synchronous',
        'end',
        'wr'
    ]

def ssh_config(hostname, date_time) -> list[str]:
    banner = '\nAuthorized personnel only\n'
    return [
       ,
        f'enable{EOL}'
        f'clock set {date_time}{EOL}',
        'configure terminal',
        'no ip domain-lookup',
        'ip domain-name cisco.lab',
        'crypto key generate rsa modulus 1024',
        'ip ssh version 2',
        'username admin secret cisco',
        'banner motd #' + banner + '#',
        'enable secret class',
        'service password-encryption',
        'hostname ' + hostname,
        'line console 0',
        'password cisco',
        'login',
        'logging synchronous',
        'exit',
        'line vty 0 15',
        'transport input ssh',
        'login local',
        'logging synchronous',
        'end',
        'wr'
    ]

def generate_vlan_conf(vlans:dict[int, str]) -> list[str]:
    config = []
    for vlan_id, vlan_name in vlans.items():
        config.append(f'vlan {vlan_id}{EOL}')
        if len(vlan_name) > 0:
            config.append(f'name {vlan_name}{EOL}')
    return config

def prompt_for_config():
    
    print('Select Config')
    print('1: Slim - clock, domain-lookup, hostname, logging, wr')
    print('2: Base - Slim + banner, enable pw, pw-encrypt, vty/con password and login')
    print('3: SSH  - Base + domain, crypto, username, transport, login local')
    
    while True:
        conf = input('> ')
        match conf.lower():
            case '1'|'slim':
                return slim_config
            case '2'|'base':
                return base_config
            case '3'|'ssh':
                return ssh_config
            case _:
                print('Input Error: Unknown config.')

