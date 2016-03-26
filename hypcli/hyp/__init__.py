from __future__ import print_function

"""Module docstring.

Create a RESTful command line interpreter to talk to hypd
"""
import cmd
import sys
import os
import getopt
import requests
import json
import urllib
import collections
from tabulate import tabulate
from hypd_completion import complete_show_packets

show_url_dict = {
    'debug': 'debug',
    'domains': 'domains',
    'hosts': 'hosts',
    'instances': 'instances',
    'interfaces': '',
    'packets': 'packets',
    'services': 'services',
    'subscriptions': 'subscribe',
    'subdomains': 'browse_domains',
    'summary': 'summary',
}
_AVAILABLE_SHOW_COMMANDS = show_url_dict.keys()


class HypShell(cmd.Cmd):
    intro = 'Welcome to the Hyp shell. Type help or ? to list commands.\n'
    prompt = '(hyp) '
    target = 'localhost'
    port = 8080
    base = 'http://%s:%d/' % (target, port)
    instance = 1
    height, width = os.popen('stty size', 'r').read().split()
    

    def print_unknown(self, cmd, line, completions):
        if line[0] != '?':
            print("%s command '%s' not recognized." % (cmd, line))
        print('Possible completions are:')
        print('    ' + ','.join(sorted(completions)))

    def do_set(self, line):
        'Set command options'
        args = line.split('=')
        if len(line) == 0:
            print("Current values:")
        elif len(args) < 2 or len(args[0]) == 0 or len(args[1]) == 0:
            print("set expecting name=value, got '%s'" % line)
        else:
            print('Setting %s = %s' % (args[0], args[1]))

    def complete_show(self, text, line, begidx, endidx):
        #print('text: ' + text, 'line: ' + line, begidx, endidx)
        words = line.split()
        if words[1] == 'packets':
            return complete_show_packets(text, line, begidx, endidx)

        return [i for i in _AVAILABLE_SHOW_COMMANDS if i.startswith(text)]
        
    def do_show(self, line):
        'Show command output'

        def print_debug(json_data, args):
            rows = []
            for d in json_data:
                rows.append([d.get('type'), d.get('size'), d.get('alloced'), d.get('freed'), d.get('inuse'),
                             d.get('bytes')])
            print(tabulate(rows, ["Type", "Size", "Allocated", "Freed", "In use", "Bytes"]) + '\n')

        def print_domains(json_data, args):
            rows = []
            for d in json_data:
                rows.append([d.get('name'), d.get('disabled'), d.get('lastRefresh'), d.get('timeout'),
                             d.get('discoveredViaHostname'), d.get('discoveredViaResolvConf'),
                             d.get('discoveredViaInAddrPtr'), d.get('browseable')])
            print(tabulate(rows, ["Name", "Admin Disabled", "Last Refreshed (sec)", "Timeout (sec)", "Hostname",
                                  "resolv.conf", "Address PTR", "Browseable"]) + '\n')

        def print_hosts(json_data, args):
            rows = []
            for d in json_data:
                rows.append([d.get('address'), d.get('query_sent'), d.get('query_received'), d.get('response_sent'),
                             d.get('response_received')])
            print(tabulate(rows, ["Address", "Queries Sent", "Queries Rcvd", "Responses Sent", "Responses Rcvd"]) + '\n')

        def print_instances(json_data, args):

            def show_flags(num):
                flag_map = {0x0001: 'WARN', 0x0002: 'PACKET', 0x0004: 'DECODE', 0x0008: 'CACHE',
                            0x0010: 'REST', 0x0020: 'DNS', 0x8000: 'DISABLED'}
                flags = []
                for flag in flag_map.keys():
                    if num & flag:
                        flags.append(flag_map[flag])
                return ','.join(flags)

            rows = []
            for d in json_data:
                rows.append([d.get('name'), d.get('index'), d.get('uuid'), show_flags(d.get('flags'))])
            print(tabulate(rows, ["Name", "Index", "UUID", "Flags"]) + '\n')

        def print_interfaces(json_data, args):

            def show_version(num):
                versions = {4: 'v4', 6: 'v6'}
                return versions.get(num, 'Unknown')

            rows = []
            for d in json_data:
                rows.append([d.get('name'), d.get('index'), show_version(d.get('family')), d.get('prefix'),
                             d.get('address'), d.get('flags'), d.get('subdomain'), d.get('dnsname'),
                             d.get('ncache')])
            print('Instance: %d' % self.instance)
            print(tabulate(rows, ["Name", "IfIndex", "Family", "Prefix", "Address", "Flags", "Subdomain Name",
                                  "Reverse DNS Name", "# Cache"]) + '\n')

        def print_packets(json_data, args_dict):
            print(urllib.urlencode(args_dict))
            print('print_packets')

        def print_services(json_data, args):
            rows = []
            for d in json_data:
                rows.append([d.get('instance'), d.get('service'), d.get('rrtype'), d.get('ttl'), d.get('rdata')[0:int(self.width)-1]])
            print(tabulate(rows, ["Instance", "Service", "Type", "TTL", "Data"]) + '\n')

        def print_subdomains(json_data, args):
            rows = []
            for d in json_data:
                rows.append([d.get('name'), d.get('ifName'), d.get('ifIndex'), d.get('disabled'),
                             d.get('discoveredViaDomainPtr'), d.get('NSActive'), d.get('discoveredViaLBInAddrPtr'),
                             d.get('browseable'), d.get('lastRefresh'), d.get('timeout'),
                             ])
            print(tabulate(rows, ["Subdomain", "IfName", "IfIndex", "Admin Disabled", "Domain PTR", "NS Active",
                                  "Browseable Net RevAddr", "Browseable", "Last Refreshed (sec)", "Timeout (sec)"]) + '\n')

        def print_subscriptions(json_data, args):
            rows = []
            for d in json_data:
                rows.append([d.get('active'), d.get('IfName'), d.get('IfIndex'), d.get('source'),
                             d.get('subscriber_name'), d.get('subscriber_addr'), d.get('type'),
                             d.get('service')])
            print(tabulate(rows, ["Active", "IfName", "IfIndex", "Source", "Subscriber Name", "Subscriber Address", "Type", "Service"]) + '\n')

        def print_summary(json_data, args):
            rows = []
            for d in json_data:
                rows.append([d.get('name'), d.get('value', '')])
            print(tabulate(rows, ["Name", "Value"]) + '\n')


        args = line.split()
        args_dict = collections.OrderedDict()
        if args[0] == 'interfaces':
            show_path = 'instances/%d/interfaces' % self.instance
        elif args[0] == 'services':
            if len(args) > 1:
                show_path = 'services/%s' % args[1]
            else:
                print('Must provide ifIndex as argument.')
                return
        elif args[0] == 'packets':
            for k in args[1:]:
                if '=' in k:
                    key, value = k.split('=')
                    if len(key) and len(value):
                        args_dict[key] = value
                else:
                    print('Arguments must contain operator: %s' % k)
            show_path = show_url_dict.get(args[0])
        elif args[0] == 'subscriptions':
            if len(args) > 1:
                show_path = 'subscribe/%s' % args[1]
            else:
                show_path = show_url_dict.get(args[0])
        else:
            show_path = show_url_dict.get(args[0])

        if show_path:
            show_func = {
                'services': print_services,
                'debug': print_debug,
                'domains': print_domains,
                'hosts': print_hosts,
                'instances': print_instances,
                'interfaces': print_interfaces,
                'packets': print_packets,
                'subdomains': print_subdomains,
                'subscriptions': print_subscriptions,
                'summary': print_summary,
            }
            url = self.base + show_path + '/'
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    func = show_func.get(args[0])
                    if func:
                        if len(args_dict):
                            func(r.json(), args_dict)
                        else:
                            func(r.json(), args[1:])
                    else:
                        self.print_unknown('show', line, show_url_dict.keys())
                else:
                    print('Error code: %d url: %s' % (r.status_code, url))
            except requests.exceptions.ConnectionError:
                print("Couldn't connect with URL: %s" % url)
        else:
            self.print_unknown('show', line, show_url_dict.keys())

    def do_shell(self, line):
        'Run a shell command'
        output = os.popen(line).read()
        print(output)
        self.last_output = output

    def do_exit(self, line):
        'Quit the shell.'
        return True

    def do_quit(self, line):
        'Quit the shell.'
        return True

    def do_EOF(self, line):
        return True



def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print(msg)
        print("for help use --help")
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)

    # process arguments
    if len(args) > 1:
        HypShell().onecmd(' '.join(args))
    else:
        HypShell().cmdloop()


if __name__ == "__main__":
    sys.exit(main())
