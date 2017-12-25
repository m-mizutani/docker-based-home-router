#!/bin/bash

cat <<EOF > $HOME/.my.cnf
[client]
password="$MYSQL_ROOT_PASSWORD"
EOF

sleep 3
if [ -z "`mysqlshow -u root -h 127.0.0.1 | grep dhcpdb`" ] ; then
		mysql -u root -h 127.0.0.1 -e "CREATE DATABASE dhcpdb;"
		mysql -u root -h 127.0.0.1 -e "SOURCE /usr/share/kea-admin/scripts/mysql/dhcpdb_create.mysql;" dhcpdb
fi

sed -i -e "s@__MYSQL_ROOT_PASSWORD__@$MYSQL_ROOT_PASSWORD@g" /etc/kea/kea-config.json
exec kea-dhcp4 -c /etc/kea/kea-config.json
