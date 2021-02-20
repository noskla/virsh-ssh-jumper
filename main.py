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
        try:
            lines[i][0] = lines[i][0].split('/')[0] # remove CIDR from IPv4
        except IndexError:
            continue
    return lines

def createCursesMenu(leases, username):
    menu = CursesMenu("SSH Jumper", username+"@canterlot.intranet")
    for lease in leases:
        if not lease:
            continue
        item = CommandItem(username+"@"+lease[1] + " (" + lease[0] + ")", "/bin/sh -c \"ssh -v -o StrictHostKeychecking=no "+username+"@"+lease[0]+"; echo -n 'Session ended'; read -s -n 1 -p '...'\"")
        menu.append_item(item)
    return menu

if __name__ == "__main__":
    print("canterlot.intranet jumper")
    username = input("Log in as user >> ")
    if not username:
        print("Using \"root\"...")
        username = "root"
    createCursesMenu(listDHCPLeases(), username).show()