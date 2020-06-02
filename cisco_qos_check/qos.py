from netmiko import ConnectHandler
import getpass
from ciscoconfparse import CiscoConfParse

def confCheck():
    with open('tempfile.txt', 'r') as f:
        conf = f.readlines()

    parse = CiscoConfParse(conf)
    running_qos = ''
    qos_list = []
    device_name = (parse.find_objects("^hostname")[0].text)

    try:
        running_qos = (parse.find_objects("^policy-map SHAPE-"))
        # running_qos = (parse.find_objects("^policy-map SHAPE-")[0].text)
    except:
        pass

    return [device_name.split()[1], running_qos]


def get_info(device, username, password):
    dev_config = 'none'
    try:
        net_connect = ConnectHandler(device_type='cisco_ios', ip=device, username=username, password=password, secret=password)
        net_connect.enable()
        net_connect.send_command('terminal length 0')
        dev_config = net_connect.send_command('show run')
        net_connect.exit_enable_mode()
        net_connect.disconnect()
        return dev_config
    except:
        with open("error_devices.txt", '+a') as errlog:
            errlog.write("error connecting to " + device + "\n")
        return dev_config


username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")


for i in range(1, 175):
        dev_config = get_info("172.16.1." + str(i), username, password)
        if dev_config != 'none':
            with open('tempfile.txt', 'w') as f:
                f.writelines(dev_config)
            result = confCheck()
            # print(result)
            print('here: ---------------')
            print("Site # {} hostname:{} - {}".format(i, (result[0]).rstrip('\n'), result[1]))
            with open('results.txt', '+a') as f:
                f.writelines("Site # {} hostname:{} - {}".format(i, (result[0]).rstrip('\n'), result[1]))


    