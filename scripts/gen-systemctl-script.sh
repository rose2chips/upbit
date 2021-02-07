#!/bin/bash

USAGE="${0} [margin rate] [currency]"

if [[ "$#" < 2 ]]; then
  echo ${USAGE}
  exit
fi

cat > $UPBIT_MONITOR_HOME/bin/monitor${2^}.sh << EOF
#!/bin/bash
$UPBIT_MONITOR_HOME/bin/monitor.py ${1} ${2^^} 
EOF

chmod a+x $UPBIT_MONITOR_HOME/bin/monitor${2^}.sh

cat > $UPBIT_MONITOR_HOME/monitor-${2}.service << EOF
# file: /etc/systemd/system/upbit-monitor.service
[Unit]
Description     = Upbit monitoring service
Wants           = network-online.target
After           = network-online.target
[Service]
User            = ${USER}
Type            = simple
WorkingDirectory= ${UPBIT_MONITOR_HOME}/
ExecStart       = /bin/bash -c '${UPBIT_MONITOR_HOME}/bin/monitor${2^}.sh'
KillSignal=SIGINT
RestartKillSignal=SIGINT
TimeoutStopSec=2
LimitNOFILE=32768
Restart=always
RestartSec=5
[Install]
WantedBy	= multi-user.target
EOF

sudo mv $UPBIT_MONITOR_HOME/monitor-${2}.service /etc/systemd/system/monitor-${2}.service
sudo chmod 644 /etc/systemd/system/monitor-${2}.service

sudo systemctl daemon-reload
sudo systemctl enable monitor-${2}
