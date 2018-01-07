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

    s3_configs = [
        {
            'tag': 'system.**',
            'path': 'system',
            'time_slice_wait': '30m',
            'buffer_path': '/var/log/fluentd/buffer_system'
        },
        {
            'tag': 'docker.**',
            'path': 'docker',
            'time_slice_wait': '30m',
            'buffer_path': '/var/log/fluentd/buffer_docker'
        },
        {
            'tag': 'dns-gazer.**',
            'path': 'dns',
            'time_slice_wait': '10m',
            'buffer_path': '/var/log/fluentd/buffer_dns'
        },
        {
            'tag': 'netflow.event',
            'path': 'netflow',
            'time_slice_wait': '10m',
            'buffer_path': '/var/log/fluentd/buffer_netflow'
        },
    ]
    
    s3_template = '''
<match {4}>
  @type s3
  aws_key_id {0}
  aws_sec_key {1}
  s3_region {2}
  s3_bucket {3}
  s3_object_key_format %{{path}}/%Y/%m/%d/%{{time_slice}}_%{{index}}.%{{file_extension}}
  time_slice_format %Y%m%d%H

  path {5}
  buffer_path {6}
  time_slice_wait {7}
  buffer_chunk_limit 256m
</match>
'''

    for c in s3_configs:
        ofd.write(s3_template.format(
            config['s3']['key'],
            config['s3']['secret'],
            config['s3']['region'],
            config['s3']['bucket_name'],
            c['tag'],
            c['path'],
            c['buffer_path'],
            c['time_slice_wait'],
        ))

    # ---------------------------
    # Mackerel
        
    mackerel_template = '''
<match metrics.**>
  @type mackerel
  api_key {0}
  hostid {1}
  metrics_name my_metrics.${{out_key}}
  out_keys val1,va2
</match>
'''
    MACKEREL_ID = '/var/lib/mackerel-agent/id'

    mackerel_api_key = config.get('mackerel', {}).get('api_key')
    if mackerel_api_key:
        logger.debug('Found Mackerel API KEY in config')
    if os.path.exists(MACKEREL_ID):
        logger.debug('Found Mackerel ID file: {}'.format(MACKEREL_ID))

    if mackerel_api_key and os.path.exists(MACKEREL_ID):
        ofd.write(mackerel_template.format(
            mackerel_api_key, open(MACKEREL_ID, 'rt').read()
        ))

        
def create_mysql_env(config):
    OUT_FILE = os.path.join(BASE_DIR, 'mysql.env')
    logger.info('creating env file for mysql: %s', OUT_FILE)

    with open(OUT_FILE, 'wt') as ofd:
        ofd.write('MYSQL_DATABASE=dhcpdb\n')
        ofd.write('MYSQL_ROOT_PASSWORD={}\n'.format(config['kea-db']['passwd']))

def create_dns_gazer_env(config):
    OUT_FILE = os.path.join(BASE_DIR, 'dns-gazer.env')
    logger.info('creating env file for dns-gazer: %s', OUT_FILE)

    with open(OUT_FILE, 'wt') as ofd:
        ofd.write('DEVICE={}\n'.format(config['monitor']['interface']))
        ofd.write('FLUENTD_ADDRESS=127.0.0.1:24224\n')
        
def create_softflowd_env(config):
    OUT_FILE = os.path.join(BASE_DIR, 'softflowd.env')
    logger.info('creating env file for softflowd: %s', OUT_FILE)

    with open(OUT_FILE, 'wt') as ofd:
        ofd.write('DEVICE={}\n'.format(config['monitor']['interface']))
        ofd.write('NETFLOW_COLLECTOR=127.0.0.1:2055\n')

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

    create_softflowd_env(config)
    create_dns_gazer_env(config)


if __name__ == '__main__':
    main()
