
# End Of Line (cr)
EOL = '\r\n'

def slim_config(hostname, date_time) -> list[str]:
    return [
        EOL,
        'enable' + EOL,
        'clock set ' + date_time + EOL,
        'configure terminal' + EOL,
        'no ip domain-lookup' + EOL,
        'hostname ' + hostname + EOL,
        'line console 0' + EOL,
        'logging synchronous' + EOL,
        'exit' + EOL,
        'line vty 0 15' + EOL,
        'logging synchronous' + EOL,
        'end' + EOL,
        'wr'
    ]

def base_config(hostname, date_time) -> list[str]:
    banner = EOL + 'Authorized personnel only' + EOL
    return [
        EOL,
        'enable' + EOL,
        'clock set ' + date_time + EOL,
        'configure terminal' + EOL,
        'no ip domain-lookup' + EOL,
        'banner motd #' + banner + '#' + EOL,
        'enable secret class' + EOL,
        'service password-encryption' + EOL,
        'hostname ' + hostname + EOL,
        'line console 0' + EOL,
        'password cisco' + EOL,
        'login' + EOL,
        'logging synchronous' + EOL,
        'exit' + EOL,
        'line vty 0 15' + EOL,
        'password cisco' + EOL,
        'login' + EOL,
        'logging synchronous' + EOL,
        'end' + EOL,
        'wr'
    ]

def ssh_config(hostname, date_time) -> list[str]:
    banner = EOL + 'Authorized personnel only' + EOL

    banner = EOL + 'Authorized personnel only' + EOL
    return [
        EOL,
        f'enable{EOL}'
        f'clock set {date_time}{EOL}',
        'configure terminal' + EOL,
        'no ip domain-lookup' + EOL,
        'ip domain-name cisco.lab' + EOL,
        'crypto key generate rsa modulus 1024' + EOL,
        'ip ssh version 2' + EOL,
        'username admin secret cisco' + EOL,
        'banner motd #' + banner + '#' + EOL,
        'enable secret class' + EOL,
        'service password-encryption' + EOL,
        'hostname ' + hostname + EOL,
        'line console 0' + EOL,
        'password cisco' + EOL,
        'login' + EOL,
        'logging synchronous' + EOL,
        'exit' + EOL,
        'line vty 0 15' + EOL,
        'transport input ssh' + EOL,
        'login local' + EOL,
        'logging synchronous' + EOL,
        'end' + EOL,
        'wr'
    ]

def generate_vlan_conf(vlans:dict[int, str]) -> list[str]:
    config = []
    for vlan_id, vlan_name in vlans.items():
        config.append(f'vlan {vlan_id}{EOL}')
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

