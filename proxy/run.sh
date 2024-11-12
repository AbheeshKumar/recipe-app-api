#!/bin/sh

set -e

echo "Running run.sh"

#environment substitute
#/etc/nginx/conf.d/default.conf contains default config evs that will substituted in our default proxy
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

nginx -g 'daemon off;'

echo "Completing run.sh"