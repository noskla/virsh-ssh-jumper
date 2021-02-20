#!/usr/bin/python3
# virsh ssh jumper

import subprocess
from cursesmenu import *
from cursesmenu.items import *


def listDHCPLeases():
    r = subprocess.run(['virsh', 'net-dhcp-leases', 'default'],
        capture_output=True, text=True)
    lines = r.stdout.split('\n')[2:] # remove headers
    for i in range(0, len(lines) - 1):
        lines[i] = list(filter(None, lines[i].split(' ')))[4:][:-1]
        lines[i][0] = lines[i][0].split('/')[0] # remove CIDR from IPv4
    return lines

def runSSH(ipv4) {
    
}

def createCursesMenu(leases):
    menu = CursesMenu("SSH Jumper", "canterlot.intranet")
    for lease in leases:
        item = FunctionItem(lease[0] + " (" + lease[1] + ")", runSSH, [lease[0]])
        menu.append_item(item)
    return menu

if __name__ == "__main__":
    createCursesMenu(listDHCPLeases()).show()
