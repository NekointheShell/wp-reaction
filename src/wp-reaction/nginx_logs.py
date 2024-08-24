import logging
from ipwhois.ipwhois import IPWhois
from ban_ip import ban_ip


def nginx_logs(file, ban_cloud_providers, ban_xmlrpc_users, ban_rest_route_users):
    log = logging.getLogger(__name__)
    file = open(filename, 'r')

    while(True):
        line = file.readline()
        if(line != '' and line != "\n"):
            linearray = line.split()
            toban = linearray[0]
            path = linearray[6]

            if(ban_xmlrpc_users and 'xmlrpc.php' in path): ban_ip(toban)
            if(ban_rest_route_users and 'rest_route' in path): ban_ip(toban)

            if(ban_cloud_providers):
                lookup = IPWhois(toban).ip_lookup()
                name = lookup['nets'][0]['name'].lower()

                if('digitalocean' in name or 'amazon' in name or 'microsoft' in name or 'dreamhost' in name or 'linode' in name or 'ovh' in name): ban_ip(toban)

    file.close()
