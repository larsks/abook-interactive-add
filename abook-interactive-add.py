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


def parse_args():
    p = argparse.ArgumentParser()
    return p.parse_args()


def main():
    subprocess.call(['clear'])
    args = parse_args()

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
    for address in answers['selected']:
        try:
            subprocess.check_call(['abook', '--mutt-query', address],
                                  stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            pass
        else:
            print(f'Address {address} already exsists in abook (skipping)')
            continue

        print(f'Adding address {address} to abook')
        address_fmt = email.utils.formataddr((addrs[address], address))
        msg = message_template.format(address=address_fmt).encode()
        abook = subprocess.run(['abook', '--add-email-quiet'],
                               input=msg,
                               check=True)

if __name__ == '__main__':
    main()
