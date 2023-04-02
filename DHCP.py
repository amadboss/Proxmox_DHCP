import os
import subprocess

dhcp_conf_template = '''
default-lease-time infinite;
max-lease-time infinite;
ddns-update-style none;
authoritative;
log-facility local7;

subnet 10.0.0.0 netmask 255.255.255.0 {
    range 10.0.0.2 10.0.0.253;
    option routers 10.0.0.1;
    option domain-name-servers 8.8.8.8;
}

'''


def get_vm_info():
    output = []
    vm_list = []
    commande = "ssh -p 2200 root@10.0.0.1 qm list | tail -n +2 | cut -d' ' -f 8"
    output.append(os.popen(commande).read())
    for line in '\n'.join(output).split('\n'):
        vm_list.append(line)
    return vm_list[:-1]

def get_mac_address():
    mac = []
    tmp = []
    command = [
    "ssh", "-p", "2200", "root@10.0.0.1",
    'perl -ne \'BEGIN{$/="\\n\\n"} print if !/^\[/m\' /etc/pve/nodes/pve/qemu-server/* | grep "^net0:" | sed -n -E "s/.*net0:.*(([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}).*/\\1/p"'
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    tmp.append(stdout.decode('utf-8').strip())

    for line in '\n'.join(tmp).split('\n'):
        mac.append(line)
    return mac

def var_maker(vm, dhcp_conf_template, mac):
    dhcp_conf_template += f''' host vm-{vm} {{
    hardware ethernet {mac};
    fixed-address 10.0.0.{int(vm) + 2};
    }}

    '''
    return dhcp_conf_template

def conf_writer(dhcp_conf_template):
    fichier = "/etc/dhcp/dhcpd.conf"
    try:
        f = open(fichier, "w")
    except FileNotFoundError:
        print(f"Le fichier {fichier} n'a pas été trouvé.")
    f.write(dhcp_conf_template)
    f.close()

vm = get_vm_info()
mac = get_mac_address()

for i in range(len(vm)):
    dhcp_conf_template = var_maker(vm[i], dhcp_conf_template, mac[i])

conf_writer(dhcp_conf_template)

os.system('systemctl restart dhcpd')