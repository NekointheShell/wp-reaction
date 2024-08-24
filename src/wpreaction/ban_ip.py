import logging, ipaddress, subprocess


log = logging.getLogger(__name__)


def ban_ip(ip):
    log = logging.getLogger(__name__)

    try:
        ipaddress.ip_address(str(ip))

    except ValueError:
        log.error('{} is not a valid IP! This could be a command injection attempt!')
        return False

    log.info('Banning {}'.format(ip))
    iptables80 = subprocess.run('iptables -A INPUT -p tcp --dport 80 -s {} -j DROP'.format(ip).split())
    iptables443 = subprocess.run('iptables -A INPUT -p tcp --dport 443 -s {} -j DROP'.format(ip).split())

    if(iptables80.returncode != 0 or iptables443.returncode != 0):
        log.error('Unable to ban {}!'.format(ip))
        return False
