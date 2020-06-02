mac1 = '0050.b6df.ef71'
mac2 = 'B4-B6-76-B1-76-0B'
mac3 = 'a0:ce:c8:0c:1a:dc'
mac4 = 'A0:CE:C8:0C:1A:DC'
allowed_string = '0123456789ABCD:'


def clean_mac(mac):
    clean_mac_addr = ''
    mac1_beta = filter(lambda x: x not in " .-:", mac)
    for x in mac1_beta:
        clean_mac_addr += x

    print(any(i in clean_mac_addr.upper() for i in allowed_string))

mac_input = clean_mac(mac2)
