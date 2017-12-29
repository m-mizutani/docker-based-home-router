#!/bin/bash

cat << EOF > $HOME/.my.cnf
[client]
password="$MYSQL_ROOT_PASSWORD"
EOF

NEXT_WAIT_TIME=0
until mysqladmin ping -u root -h 127.0.0.1 || [ $NEXT_WAIT_TIME -eq 10 ]; do
		echo "waiting..."
		sleep $(( NEXT_WAIT_TIME++ ))
done

exec kea-dhcp4 -c /etc/kea/kea-config.json
