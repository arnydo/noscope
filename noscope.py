#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOSCOPE - A tool for scoping IP addresses and domains based on defined ranges.
Author: Kyle Parrish
Version: 0.1
License: GPL
Copyright (C) 2024, NOSCOPE
Contact: github@arnydo.com
"""

import ipaddress
import dns
from dns import resolver
import argparse
from tabulate import tabulate

class Logo:
    def __init__(self, script):
        self.script = script
        self.c = Color()

    def print(self):
        print(self.c.GREEN + self.get_logo() + '\n')

        print('' + self.c.YELLOW +
              '''💾 https://github.com/arnydo/noscope''' + self.c.WHITE)
        print('' + self.c.BLUE +
              '''🐦 https://twitter.com/kyle_parrish_\n''' + self.c.WHITE)

    def get_logo(self):
        if self.script == 'default':
            return '''
┏━┓╋┏┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
┃┃┗┓┃┃┏━┓┃┏━┓┃┏━┓┃┏━┓┃┏━┓┃┏━━┛
┃┏┓┗┛┃┃╋┃┃┗━━┫┃╋┗┫┃╋┃┃┗━┛┃┗━━┓
┃┃┗┓┃┃┃╋┃┣━━┓┃┃╋┏┫┃╋┃┃┏━━┫┏━━┛
┃┃╋┃┃┃┗━┛┃┗━┛┃┗━┛┃┗━┛┃┃╋╋┃┗━━┓
┗┛╋┗━┻━━━┻━━━┻━━━┻━━━┻┛╋╋┗━━━┛'''

class Color:
    def __init__(self):
        self.BRED = '\033[1;31;20m'
        self.RED = '\033[0;31;20m'
        self.BRED_BLACK = '\033[1;30;41m'
        self.RED_BLACK = '\033[0;30;41m'
        self.BGREEN = '\033[1;32;20m'
        self.GREEN = '\033[0;32;20m'
        self.BGREEN_BLACK = '\033[1;30;42m'
        self.GREEN_BLACK = '\033[0;30;42m'
        self.BYELLOW = '\033[1;33;20m'
        self.YELLOW = '\033[0;33;20m'
        self.BBLUE = '\033[1;34;20m'
        self.BLUE = '\033[0;34;20m'
        self.BMAGENTA = '\033[1;35;20m'
        self.MAGENTA = '\033[0;35;20m'
        self.BCYAN = '\033[1;36;20m'
        self.CYAN = '\033[0;36;20m'
        self.BWHITE = '\033[1;37;20m'
        self.WHITE = '\033[0;37;20m'

    def ansy(self):
        self.BRED = ''
        self.RED = ''
        self.BRED_BLACK = ''
        self.RED_BLACK = ''
        self.BGREEN = ''
        self.GREEN = ''
        self.BGREEN_BLACK = ''
        self.GREEN_BLACK = ''
        self.BYELLOW = ''
        self.YELLOW = ''
        self.BBLUE = ''
        self.BLUE = ''
        self.BMAGENTA = ''
        self.MAGENTA = ''
        self.BCYAN = ''
        self.CYAN = ''
        self.BWHITE = ''
        self.WHITE = ''
   

def read_file(filename):
    """Reads lines from a file and returns them as a list."""
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def read_cidr_ranges(filename):
    """Reads CIDR ranges from a file and returns them as a list."""
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def parse_ip_from_domain_entry(entry):
    """Parses IP address from domain entry."""
    return entry.split(':')[1]

def get_domain_ips(domain):
    """Retrieves IP addresses associated with a domain."""
    try:
        result = dns.resolver.resolve(domain, 'A')
        return [str(ipval) for ipval in result]
    except dns.resolver.NoAnswer:
        print("No DNS response received for:", domain)
        return []

def is_ip_in_cidr(ip_address, scope):
    """Checks if an IP address is within the defined CIDR range."""
    try:
        ip = ipaddress.ip_address(ip_address)
        for cidr in scope:
            network = ipaddress.ip_network(cidr)
            if ip in network:
                return True
        return False
    except ValueError:
        return False
    
def scope_domains(domains, scope):
    """Scopes domains based on defined CIDR ranges."""
    scoped_domains = []
    for domain_entry in domains:
        ip_addresses = get_domain_ips(domain_entry)
        for ip_address in ip_addresses:
            if is_ip_in_cidr(ip_address, scope):
                scoped_domains.append((domain_entry, ip_address))
                break
    return scoped_domains

def scope_ips(ips, scope):
    """Scopes IPs based on defined CIDR ranges."""
    scoped_ips = []
    for ip in ips:
        if is_ip_in_cidr(ip, scope):
            scoped_ips.append(ip)
    return scoped_ips

def main():
    parser = argparse.ArgumentParser(description='NOSCOPE: A tool for scoping IP addresses and domains based on defined ranges.')
    domain_group = parser.add_mutually_exclusive_group()
    ip_group = parser.add_mutually_exclusive_group()

    domain_group.add_argument(
        "-d",
        "--domain",
        type=str,
        nargs='+',
        help="Domain(s) to lookup",
    )

    domain_group.add_argument(
        "-dL",
        "--domain-list",
        type=str,
        help="List of domains to lookup from a file",
    )

    parser.add_argument(
        "-s",
        "--scope-file",
        required=True,
        type=str,
        help="File containing list of CIDR scopes",
    )

    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        help="File to save output to",
    )

    ip_group.add_argument(
        "-ip",
        type=str,
        nargs='+',
        help="IP(s) to lookup",
    )

    ip_group.add_argument(
        "-iL",
        "--i-list",
        type=str,
        help="List of IPs to lookup from a file",
    )
    
    args = parser.parse_args()

    # Check if neither domain nor IP options are provided
    if not (args.domain or args.domain_list or args.ip or args.i_list):
        parser.error("At least one of --domain or --domain-list or --ip or --i-list must be specified.")

    scope = read_cidr_ranges(args.scope_file)

    scoped_data = []

    if hasattr(args, "domain") and args.domain:
        domains = args.domain
        scoped_data.extend(scope_domains(domains, scope))
    elif hasattr(args, "domain_list") and args.domain_list:
        domains = read_file(args.domain_list)
        scoped_data.extend(scope_domains(domains, scope))

    if hasattr(args, "ip") and args.ip:
        ips = args.ip
        scoped_data.extend([(ip, "") for ip in scope_ips(ips, scope)])
    elif hasattr(args, "ip_list") and args.ip_list:
        ips = read_file(args.ip_list)
        scoped_data.extend([(ip, "") for ip in scope_ips(ips, scope)])

    if args.output_file:
        with open(args.output_file, 'w') as outfile:
            for domain, ip in scoped_data:
                outfile.write(f"{domain}:{ip}\n")

    # Print output in tabular format
    if len(scoped_data) > 0:
        print(tabulate(scoped_data, headers=["Domain", "IP"], tablefmt="grid"))
    else:
        print("None of the provided items are not in scope.")

if __name__ == "__main__":
    logo = Logo('default')
    logo.print()
    main()
