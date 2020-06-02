"""
Given a file 'acl.txt' containing the output from a Cisco ASA acl show
Removes the hitcount* trailer
prepends no and reverses order
outputting to the screen
"""

with open("acl.txt", 'r') as file:
    lines = file.readlines()
    # with open("acl-reversed.txt", 'w') as new_file:
    for str_line in reversed(lines):
        line_clean = "no " + str_line.split('(hit', 1)[0]
            # line_clean = "no " + str_line.split('(hit', 1)[0] + "\n"
        print(line_clean)
            # new_file.write(line_clean)
