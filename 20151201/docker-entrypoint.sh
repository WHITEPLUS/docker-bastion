#!/usr/bin/env bash

LOGIN_PASSWD=${LOGIN_PASSWD}

[[ -n $LOGIN_PASSWD ]] \
|| ( echo ENV LOGIN_PASSWD is necessary. ;exit 1 )

( echo "root:${LOGIN_PASSWD}" | chpasswd ) \
|| ( echo Failed to init root password. ;exit 1 )

# Start supervisord and services
/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
