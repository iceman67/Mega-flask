import netifaces

addrs = netifaces.ifaddresses('eth0')
print ( addrs[netifaces.AF_INET][0]['addr'])
