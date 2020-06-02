import getpass
from netmiko import ConnectHandler
import os
import datetime

router_username = input("Enter Cisco username: ")
router_password = getpass.getpass(prompt='Enter Cisco password: ')


def remove_nac(switch, port):
    global router_username
    global router_password
    net_connect = ConnectHandler(device_type='cisco_ios', ip=switch, username=router_username,
                                 password=router_password, secret=router_password)
    net_connect.enable()
    net_connect.config_mode()
    port_info = 'int ' + port
    config_commands = [  port_info,
                         'authentication port-control auto',
                         'end', ]
    output = net_connect.send_config_set(config_commands)
    net_connect.send_command('write mem')
    net_connect.disconnect()
    print("Completed switch {} on port {}".format(switch, port))

with open('renacd-ports.log', 'a+') as renacd:
    renacd.write("Ports re-nac'd on {}\n".format(datetime.datetime.now()))
    print("-" * 60 + "\n")
    renacd.write(("-" * 60 + "\n"))
    with open('denac_list.txt', 'r') as nacfile:
        for line in nacfile:
            new_line = line.rstrip("\n")
            list = new_line.split(',')
            sw_ip, sw_port = (list[1], list[2])
            remove_nac(sw_ip, sw_port)
            renacd.write(line)


os.remove("denac_list.txt")




