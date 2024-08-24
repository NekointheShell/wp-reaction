import logging, configparser
from systemd import journal
from threading import Thread

from .login_failures import login_failures
from .nginx_logs import nginx_logs
from .log_coordinates import log_coordinates


log = logging.getLogger(__name__)
log.addHandler(journal.JournalHandler())
log.setLevel(logging.INFO)


def main():
    config = configparser.ConfigParser()
    config.read('/etc/systemd/wp-reaction.conf')

    if(config['login_failures']['enabled'] == 'True'):
        login_failures_thread = Thread(target = login_failures, args = [config['login_failures']['file']])

    if(config['nginx_logs']['enabled'] == 'True'):
        nginx_logs_thread = Thread(target = nginx_logs, args = [
            config['nginx_logs']['file'],
            config['nginx_logs']['ban_cloud_providers'],
            config['nginx_logs']['ban_xmlrpc_users'],
            config['nginx_logs']['ban_rest_route_users']
        ])

    if(config['log_coordinates']['enabled'] == 'True'):
        log_coordinates_thread = Thread(target = log_coordinates, args = [
            config['log_coordinates']['file'],
            config['log_coordinates']['north_limit'],
            config['log_coordinates']['south_limit'],
            config['log_coordinates']['east_limit'],
            config['log_coordinates']['west_limit']
        ])

    threads = ['login_failures_thread', 'nginx_logs_thread', 'log_coordinates_thread']
    for thread in threads:
        if(thread in locals()):
            locals()[thread].run()

    
if __name__ == '__main__': main()
