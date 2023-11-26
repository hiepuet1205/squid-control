import os, time
from passlib.apache import HtpasswdFile
from .models import Proxy

ROUTE_SQUID_CONFIG = "/etc/squid/squid.conf"
ROUTE_HTPASSWD = "/etc/squid/.htpasswd"

squidconf = open(ROUTE_SQUID_CONFIG,"w")

header = """
acl localnet src 0.0.0.1-0.255.255.255	
acl localnet src 10.0.0.0/8		
acl localnet src 100.64.0.0/10		
acl localnet src 169.254.0.0/16 	
acl localnet src 172.16.0.0/12		
acl localnet src 192.168.0.0/16		
acl localnet src fc00::/7       	
acl localnet src fe80::/10      	

acl SSL_ports port 443
acl Safe_ports port 80		
acl Safe_ports port 21		
acl Safe_ports port 443		
acl Safe_ports port 70		
acl Safe_ports port 210		
acl Safe_ports port 1025-65535	
acl Safe_ports port 280		
acl Safe_ports port 488		
acl Safe_ports port 591		
acl Safe_ports port 777		

http_access deny !Safe_ports

http_access deny CONNECT !SSL_ports

http_access allow localhost manager
http_access deny manager

include /etc/squid/conf.d/*.conf

auth_param basic program /lib/squid/basic_ncsa_auth /etc/squid/.htpasswd
auth_param basic children 3
auth_param basic realm MySquidProxy
auth_param basic credentialsttl 1 hours
acl auth_users proxy_auth REQUIRED
http_access allow auth_users
"""

footer = """
http_access deny all
http_port 3128

coredump_dir /var/spool/squid

refresh_pattern ^ftp:		1440	20%	10080
refresh_pattern ^gopher:	1440	0%	1440
refresh_pattern -i (/cgi-bin/|\?) 0	0%	0
refresh_pattern \/(Packages|Sources)(|\.bz2|\.gz|\.xz)$ 0 0% 0 refresh-ims
refresh_pattern \/Release(|\.gpg)$ 0 0% 0 refresh-ims
refresh_pattern \/InRelease$ 0 0% 0 refresh-ims
refresh_pattern \/(Translation-.*)(|\.bz2|\.gz|\.xz)$ 0 0% 0 refresh-ims
refresh_pattern .		0	20%	4320
"""

main = ""

def reconfigure():
    os.system("sudo squid -k reconfigure")
    time.sleep(5)

def addAuthentication(username, password):
    htpasswd = HtpasswdFile(ROUTE_HTPASSWD)
    htpasswd.set_password(username, password)
    htpasswd.save()

def deleteAuthentication(username):
    htpasswd = HtpasswdFile(ROUTE_HTPASSWD)
    htpasswd.delete(username)
    htpasswd.save()

def limitBandwidth(): 
    all_proxies = Proxy.objects.all()

    acls = ""
    # http_access = ""
    delay = f"delay_pools {all_proxies.count()} \n"

    for index, proxy in enumerate(all_proxies):
        acls += f'acl {proxy.username} proxy_auth {proxy.username} \n'
        # http_access += f'http_access allow {proxy.username} \n'
        delay += f"delay_class {index + 1} 1 \ndelay_parameters {index + 1} {int(proxy.bandwidth / 8 * 1000000)}/{int(proxy.bandwidth / 8 * 1000000)} \ndelay_access {index + 1} allow {proxy.username}\n"

    # main = acls + '\n' + http_access + '\n' + delay + '\n'
    main = acls + '\n' + delay + '\n'

    squidconf = open(ROUTE_SQUID_CONFIG,"w")
    squidconf.write(header+main+footer)
    squidconf.close()
    time.sleep(1)
    print("Done.")