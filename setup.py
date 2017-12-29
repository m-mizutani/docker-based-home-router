#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import json
import logging
import argparse
import random
import string

logger = logging.getLogger()
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def create_kea_config(config):
    IN_FILE = os.path.join(BASE_DIR, 'kea', 'kea-config.template.json')
    OUT_FILE = os.path.join(BASE_DIR, 'kea', 'kea-config.json')
    logger.info('creating kea config file: %s', OUT_FILE)

    settings = json.load(open(IN_FILE, 'rt'))

    # Set parameters.
    settings['Dhcp4']['lease-database']['password'] = config['kea-db']['passwd']
    settings['Dhcp4']['interfaces-config']['interfaces'] = \
        config['dhcp']['interfaces']

    net = {
        'pools': [{'pool': x} for x in config['dhcp']['pools']],
        'subnet': config['network']['subnet'],
        'option-data': [
            {
                'data': config['network']['internal_gateway'],
                'name': 'routers',
            },
            {
                'data': config['network']['internal_gateway'],
                'name': 'domain-name-servers',
            },
        ]
    }
    settings['Dhcp4']['subnet4'] = [net]
    json.dump(settings, open(OUT_FILE, 'wt'), indent=4)

    


def create_fluentd_config(config):
    IN_FILE = os.path.join(BASE_DIR, 'fluentd', 'fluent.template.conf')
    OUT_FILE = os.path.join(BASE_DIR, 'fluentd', 'fluent.conf')
    logger.info('creating fluentd config: %s', OUT_FILE)

    ofd = open(OUT_FILE, 'wt')
    for line in open(IN_FILE, 'rt'):
        ofd.write(line)

    template = '''
<match system.**>
  @type s3
  aws_key_id {0}
  aws_sec_key {1}
  s3_region {2}
  s3_bucket {3}
  s3_object_key_format %{{path}}%{{time_slice}}_%{{index}}.%{{file_extension}}

  path system/
  buffer_path /var/log/fluentd/buffer_system
  time_slice_format %Y%m%d%H
  time_slice_wait 10m
  buffer_chunk_limit 256m
</match>
'''
    ofd.write(template.format(
        config['s3']['key'],
        config['s3']['secret'],
        config['s3']['region'],
        config['s3']['bucket_name']
    ))

              
def create_mysql_env(config):
    OUT_FILE = os.path.join(BASE_DIR, 'mysql.env')
    logger.info('creating env file for mysql: %s', OUT_FILE)

    with open(OUT_FILE, 'wt') as ofd:
        ofd.write('MYSQL_DATABASE=dhcpdb\n')
        ofd.write('MYSQL_ROOT_PASSWORD={}\n'.format(config['kea-db']['passwd']))
    

def mkpasswd(n=16):
    passwd_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    passwd = ''.join([random.choice(passwd_chars) for _ in range(16)])
    return passwd

        
def main():
    psr = argparse.ArgumentParser()
    psr.add_argument('-c', '--conf-path', default=os.path.join(BASE_DIR, 'config.json'))
    psr.add_argument('-s', '--secret-file', default=os.path.join(BASE_DIR, 'secret.json'))
    args = psr.parse_args()

    logger.debug('config path: %s', args.conf_path)
    config = json.load(open(args.conf_path, 'rt'))

    if os.path.exists(args.secret_file):
        secrets = json.load(open(args.secret_file, 'rt'))
    else:
        secrets = { 'kea-db-passwd': mkpasswd() }
        json.dump(secrets, open(args.secret_file, 'wt'))

    config['kea-db'] = {'passwd': secrets['kea-db-passwd']}

    
    # Create files.
    create_fluentd_config(config)
    create_kea_config(config)
    create_mysql_env(config)

if __name__ == '__main__':
    main()
