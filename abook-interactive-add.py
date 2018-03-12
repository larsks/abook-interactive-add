#!/usr/bin/env python3 

import argparse
import email
import inquirer
import os
import subprocess
import sys


message_template='''From: {address}
To: nobody@example.com
Subject: dummy message for abook

This is a dummy message.
'''

header_template='''{hr}
Add addresses to address book
{hr}

Use arrow keys (↑, ↓) to move and the space bar to select/unselect. Press
enter to confirm your selection.

'''


def get_terminal_width():
    try:
        width = int(subprocess.check_output(['tput', 'cols']))
    except (OSError, subprocess.CalledProcessError, ValueError):
        width = 0

    return width


def parse_args():
    p = argparse.ArgumentParser()
    return p.parse_args()


def header():
    width = get_terminal_width()
    subprocess.call(['clear'])
    print(header_template.format(hr='=' * width))
    print


def main():
    args = parse_args()

    header()

    # read message from stdin
    msg = email.message_from_file(sys.stdin)

    # reopen /dev/tty as stdin
    tty = open('/dev/tty')
    os.dup2(tty.fileno(), sys.stdin.fileno())

    froms = msg.get_all('from', [])
    tos = msg.get_all('to', [])
    ccs = msg.get_all('cc', [])
    addrs = email.utils.getaddresses(froms + tos + ccs)
    addrs = {addr[1]: addr[0] for addr in addrs}

    questions = [
        inquirer.Checkbox('selected',
                          message='Select addresses to add',
                          choices=addrs.keys(),
                          ),
    ]

    answers = inquirer.prompt(questions)
    added = 0
    for address in answers['selected']:
        try:
            subprocess.check_call(['abook', '--mutt-query', address],
                                  stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            pass
        else:
            print(f'Address {address} already exsists in your address '
                  'book (skipping)')
            continue

        print(f'Adding address {address} to your address book')
        added += 1
        address_fmt = email.utils.formataddr((addrs[address], address))
        msg = message_template.format(address=address_fmt).encode()
        abook = subprocess.run(['abook', '--add-email-quiet'],
                               input=msg,
                               check=True)

    print(f'Added {added} addresses to your address book')

if __name__ == '__main__':
    main()
