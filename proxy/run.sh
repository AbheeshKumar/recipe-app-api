#!/bin/sh

set -e

#environment substitute
#/etc/nginx/conf.d/default.conf contains default config evs that will substituted in our default proxy
envsubst < "/etc/nginx/default.conf.tpl" > "/etc/nginx/conf.d/default.conf"
nginx -g 'daemon off;'


