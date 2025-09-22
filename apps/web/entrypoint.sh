#!/bin/sh
set -eu
: "${WEB_API_BASE:=/api}"
: "${ENVIRONMENT:=local}"
: "${SENTRY_DSN:=}"
sed -e "s|%%WEB_API_BASE%%|$WEB_API_BASE|g"     -e "s|%%ENVIRONMENT%%|$ENVIRONMENT|g"     -e "s|%%SENTRY_DSN%%|$SENTRY_DSN|g"     /usr/share/nginx/html/config.template.js > /usr/share/nginx/html/config.js
exec nginx -g 'daemon off;'
