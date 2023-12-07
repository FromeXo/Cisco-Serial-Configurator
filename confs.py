
# End Of Line (cr)
EOL = '\r\n'

def slim_base_config(hostname, date_time) -> list[str]:
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
    user_pw = 'cisco'
    en_pw = 'class'
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
        'password ' + user_pw + EOL,
        'login' + EOL,
        'logging synchronous' + EOL,
        'exit' + EOL,
        'line vty 0 15' + EOL,
        'password ' + user_pw + EOL,
        'login' + EOL,
        'logging synchronous' + EOL,
        'end' + EOL,
        'wr'
    ]

def ssh_base_config(hostname, date_time) -> list[str]:
    user_pw = 'cisco'
    en_pw = 'class'
    banner = EOL + 'Authorized personnel only' + EOL
    return [
        EOL,
        'enable' + EOL,
        'clock set ' + date_time + EOL,
        'configure terminal' + EOL,
        'no ip domain-lookup' + EOL,
        'ip domain-name cisco.lab' + EOL,
        'crypto key generate rsa modulus 1024' + EOL,
        'ip ssh version 2' + EOL,
        'username admin secret class' + EOL,
        'banner motd #' + banner + '#' + EOL,
        'enable secret class' + EOL,
        'service password-encryption' + EOL,
        'hostname ' + hostname + EOL,
        'line console 0' + EOL,
        'password ' + user_pw + EOL,
        'login' + EOL,
        'logging synchronous' + EOL,
        'exit' + EOL,
        'line vty 0 15' + EOL,
        'transport input ssh' + EOL,
        #'password ' + user_pw + EOL,
        'login local' + EOL,
        'logging synchronous' + EOL,
        'end' + EOL,
        'wr'
    ]
