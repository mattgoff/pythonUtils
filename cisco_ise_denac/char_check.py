mac1 = '0050b6dfef71'
mac2 = 'B4-B6-76-B1-76-0B'
mac3 = 'a0:ce:c8:0c:1a:dc'
mac4 = 'A0:CE:C8:0C:1A:DC'
allowed_string = '0123456789ABCDEF:'


def char_check(mac):
    for c in mac:
        if c not in allowed_string:
            return("nvm")
        else:
            return("valid")


valid_check = char_check(mac1.upper())
if valid_check == "valid":
    print(valid_check)
else:
    print("bad mac")