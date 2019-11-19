#!/bin/sh

unset IFS
for var in $(compgen -e); do
    echo "${!var}"
done
