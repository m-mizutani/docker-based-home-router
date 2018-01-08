Docker based Home Router
===================

Setup
----------------

### Configure AWS S3 for log storage

### Install Mackerel

Mackerel (https://mackerel.io) is a metrics monitoring service. Mackerel provides [Free plan](https://mackerel.io/orgs/mizutani-home/plans) including 5 hosts monitoring and 10 monitoring rules. 

After creating Mackerel account, the Mackerel agent can be installed to latest ubuntu Linux by like following command.

```shell
$ wget -q -O - https://mackerel.io/file/script/setup-all-apt-v2.sh | MACKEREL_APIKEY='2R8VBzXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' sh
```

You can find a guide with more details to install agent to each OS from [their document](https://mackerel.io/orgs/mizutani-home/instruction-agent)

### Create config.json

```shell
$ cp config.template.json config.json
$ vim config.json
```

The template file of config.json assumes following:

- Home network
    - Network: `10.0.0.0/24`
    - IP address range for DHCP hosts: from `10.0.0.129` to `10.0.0.254`
    - Network interface connecting to home network: `enp0s3`
    - IP address of above network interface: `10.0.0.1`

Change each parameter in `config.json` according to your network envrionment.

### Run setup script to generate config files

After configure of `config.json`, run `setup.py`. It may require Python3.

```shell
$ ./setup.py
2018-01-06 03:57:57,279 [DEBUG] config path: /home/ubuntu/modern-home-router-2018/config.json
2018-01-06 03:57:57,282 [INFO] creating fluentd config: /home/ubuntu/modern-home-router-2018/fluentd/fluent.conf
2018-01-06 03:57:57,286 [DEBUG] Found Mackerel API KEY in config
2018-01-06 03:57:57,286 [DEBUG] Found Mackerel ID file: /var/lib/mackerel-agent/id
2018-01-06 03:57:57,286 [INFO] creating kea config file: /home/ubuntu/modern-home-router-2018/kea/kea-config.json
2018-01-06 03:57:57,289 [INFO] creating env file for mysql: /home/ubuntu/modern-home-router-2018/mysql.env
2018-01-06 03:57:57,289 [INFO] creating env file for dns-gazer: /home/ubuntu/modern-home-router-2018/dns-gazer.env
```
