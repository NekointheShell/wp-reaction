import logging, time
from ipwhois.ipwhois import IPWhois
from .ban_ip import ban_ip


def nginx_logs(filename, ban_cloud_providers, ban_xmlrpc_users, ban_rest_route_users):
    log = logging.getLogger(__name__)
    log.info('Starting nginx logs filter...')
    file = open(filename, 'r')

    while(True):
        line = file.readline()
        if(line != '' and line != "\n"):
            linearray = line.split()
            toban = linearray[0]
            path = linearray[6]
            log.debug(path)
            if(toban == '127.0.0.1'): continue

            if(ban_xmlrpc_users == 'True' and 'xmlrpc.php' in path): ban_ip('nginx_logs', toban)
            if(ban_rest_route_users == 'True' and 'rest_route' in path): ban_ip('nginx_logs', toban)

            if(ban_cloud_providers == 'True'):
                try:
                    lookup = IPWhois(toban).lookup_whois()
                    name = lookup['nets'][0]['name'].lower()

                    if('digitalocean' in name or 'amazon' in name or 'microsoft' in name or 'dreamhost' in name or 'linode' in name or 'ovh' in name): ban_ip('nginx_logs', toban)

                except Error as e:
                    log.error(e)

        time.sleep(1)

    file.close()
