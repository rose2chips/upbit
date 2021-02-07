#!/bin/bash

if [ "$1" == "" ]; then
  echo "$0 [start|stop|restart] {currency}"
  exit
fi

if [ "$2" == "" ]; then
  sudo systemctl $1 monitor-eth
  sudo systemctl $1 monitor-atom
  sudo systemctl $1 monitor-ada
  sudo systemctl $1 monitor-xlm
  sudo systemctl $1 monitor-snt
  sudo systemctl $1 monitor-zil
  sudo systemctl $1 monitor-xrp
  sudo systemctl $1 monitor-hbar
  sudo systemctl $1 monitor-kmd
  exit
fi

sudo systemctl $1 monitor-${2}
