import getpass
import xmltodict
from netmiko import ConnectHandler
import requests
from requests.auth import HTTPBasicAuth

allowed_string = '0123456789ABCDEF:'


def get_switch_info(mac_search):
    ise_username = input("Enter ISE username: ")
    ise_password = getpass.getpass(prompt='Enter ISE password: ')
    url_string = 'https://ise/admin/API/mnt/Session/MACAddress/{}'.format(mac_search)
    r = requests.get(url_string, auth=HTTPBasicAuth(ise_username, ise_password))
    ise_dict = xmltodict.parse(r.text)
    try:
        switch_name = (ise_dict['sessionParameters']['network_device_name'])
        switch_ip = (ise_dict['sessionParameters']['nas_ip_address'])
        switch_port = (ise_dict['sessionParameters']['nas_port_id'])
        print("Switch Name = {}".format(switch_name))
        print("Switch IP = {}".format(switch_ip))
        print("Switch Port = {}".format(switch_port))
        return switch_name, switch_ip, switch_port
    except:
        switch_name, switch_ip, switch_port = '1.1.1.1', '1.1.1.1', '1.1.1.1'
        return switch_name, switch_ip, switch_port


def remove_nac(switch, port):
    router_username = input("Enter Cisco username: ")
    router_password = getpass.getpass(prompt='Enter Cisco password: ')

    net_connect = ConnectHandler(device_type='cisco_ios', ip=switch, username=router_username,
                                 password=router_password, secret=router_password)
    net_connect.enable()
    net_connect.config_mode()
    port_info = 'int ' + port
    config_commands = [  port_info,
                         'authentication port-control force-authorized',
                         'end', ]
    output = net_connect.send_config_set(config_commands)
    net_connect.send_command('write mem')
    net_connect.disconnect()
    print("Completed switch {} on port {}".format(switch, port))
    return router_username


def save_list_of_denacd_ports(sw_name, sw_ip, sw_port, mac, who):
    with open('denac_list.txt', 'a+') as nac_list:
        nac_list.write("{},{},{},{},{}\n".format(sw_name, sw_ip, sw_port, mac, who))


def clean_up_mac_addr(mac):
    clean_mac = ''
    mac1_beta = filter(lambda x: x not in " .-:", mac)
    for x in mac1_beta:
        clean_mac += x

    new_mac = clean_mac.upper()[:2] + ':' + clean_mac.upper()[2:4] + ':' + clean_mac.upper()[4:6] + ':' + \
              clean_mac.upper()[6:8] + ':' + clean_mac.upper()[8:10] + ':' + clean_mac.upper()[10:]
    return new_mac


def char_check(mac):
    for c in mac:
        if c not in allowed_string or (len(mac) != 17):
            return("nvm")
        else:
            return("valid")


raw_mac_to_search = input("Enter the MAC address to de-nac (format 11:22:33:44:55:66): ")
mac_to_search = clean_up_mac_addr(raw_mac_to_search)
valid_check = char_check(mac_to_search)

if valid_check == 'valid':
    switch_name, switch_ip_to_denac, port_to_denac = get_switch_info(mac_to_search)

    if switch_name == '1.1.1.1':
        print("Mac Address {} not found in NAC (maybe try the phone mac) ".format(mac_to_search))
    else:
        who_did_it = remove_nac(switch_ip_to_denac, port_to_denac)
        save_list_of_denacd_ports(switch_name, switch_ip_to_denac, port_to_denac, mac_to_search, who_did_it)
else:
    print("Not a valid MAC address, try again: ")
