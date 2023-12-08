# Validate a VLAN id
def is_valid_vlan_num(vlan:int) -> bool:

    if vlan >= 2 or vlan <= 3967:
        return True

    if vlan >= 4048 or vlan <= 4093:
        return True

    return False

# Validate a VLAN name
def is_valid_vlan_name(name:str) -> bool:

    if name == '':
        return True

    if len(name) > 32 or not name.isalnum():
        return False

    return True

# Run validations on a VLAN id, and prompt for a new id it's not a valid id.
def get_vlan_id(existing_vlan:str|None = None) -> int:

    ret: int = 0
    
    while ret == 0:

        if existing_vlan is None:
            # Ask for VLAN id
            vlan_number = input('Vlan Number: ')
        else:
            vlan_number = existing_vlan
            existing_vlan = None

        if not vlan_number.isnumeric():
            print('Input Error: Must be a number.')
            continue

        vlan_number = int(vlan_number)

        while not is_valid_vlan_num(vlan_number):
            print('Input Error: Invalid vlan range.')
            print('Allowed vlan range is 2-1005, 1006-3967 and 4048-4093')
            continue
        
        ret = vlan_number

    return ret

# Prompts user for a VLAN name.
def  get_vlan_name() -> str:

    name:str|None = None

    while name is None:
        # Ask for VLAN name
        vlan_name = input('Vlan Name: ')

        # Make sure it's valid.
        if not is_valid_vlan_name(vlan_name):
            print('Input Error: Invalid vlan name.')
            print('Allowed vlan name format is 0-32 alphanumeric characters')
            continue

        # All good!
        name = vlan_name

    return name


# Print VLANS as a table.
def print_vlan_table(vlans:dict[int, str]) -> None:
    
    print('== VLANs ============================')
    
    if len(vlans) > 0:
    
        print('Id   | Name')
    
        for k,v in vlans.items():
    
            print('------------------------------------------')
    
            # Padding makes everything look pretty.    
            padding: str = ' ' * (4 - len(str(k)))
        
            print(f"{k}{padding} | {v}")
    else:
        print('\nNo VLANs defined.')
    
# Make sure we have an existing and valid vlan id 
def delete_vlan(action: list[str], vlans:list[int]) -> int|None:

    if len(action) < 2 or not action[1].isnumeric():
        print('Input Error: Unknown VLAN Id')
        return None

    vlan_id = int(action[1])

    if vlan_id not in vlans:
        print('Error: VLAN id is not defined.')
        return None
    
    return vlan_id

# Create a new VLAN
def mk_vlan(action: list[str]) -> dict[int, str]:
    
    vlan:dict[int, str] = dict()

    if len(action) > 1:
        vlan_id = get_vlan_id(action[1])
    else:
        vlan_id = get_vlan_id()

    vlan_name = get_vlan_name()

    vlan.update({vlan_id: vlan_name})

    return vlan

# Guess
def print_vlan_menu() -> None:
    print('\n== Menu ============================')
    print('show | sh       - Print VLAN table.')
    print('del {vlan id}   - Remove VLAN.')
    print('vlan {vlan id}  - Add a new VLAN.')
    print('menu | help | ? - Show this menu.')
    print('exit            - Stop manageing VLANS.\n')

# Main function to navigate this spaghetti
def prompt_for_vlan(existing_vlans: dict[int, str]|None = None) -> dict[int, str]:
    
    vlans:dict[int, str] = dict()
    
    if existing_vlans is not None:
        vlans.update(existing_vlans)

    print_vlan_table(vlans)
    print_vlan_menu()
    
    
    while True:

        action = input('> ')
        action = action.lower().split(' ')
        
        match action[0]:
            case 'help' | '?' | 'menu':
                print_vlan_menu()

            case 'show' | 'sh':
                print_vlan_table(vlans)

            case 'del':
                key = delete_vlan(action, vlans.keys)
                if key is not None:
                    del vlans[key]

            case 'vlan' | 'add':
                new_vlan = mk_vlan(action)

                if len(new_vlan) > 0:
                    vlans.update(new_vlan)
                    print_vlan_table(vlans)
                    print('')

            case 'exit':
                return vlans
            case _:
                print('Unknown command.')
