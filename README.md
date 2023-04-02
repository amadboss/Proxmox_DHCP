# Proxmox_DHCP

## How it work
This script will allow you to automatically give proxmox VMs IPs depending on their number.
It gather machine number and mac address from the host and change /etc/dhcp/dhcpd.conf as follow :

```
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

 host vm-100 {
    hardware ethernet 76:6B:74:08:6B:7B;
    fixed-address 10.0.0.102;
    }

     host vm-101 {
    hardware ethernet 82:6D:0C:B0:98:35;
    fixed-address 10.0.0.103;
    }

     host vm-102 {
...
```
In my case it run on a container and make ssh command to host to gather informations.
Make sure that it denied all shh connetion attempts.
