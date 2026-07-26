# Raspberry Pi OS Administration

## Introduction

The following documentation could help you with simple system administration for this project.
It's definitely not exhaustive and might not be straightforward depending of the version of  Raspberry Pi OS that you use.

> [!IMPORTANT]
> Always read the man if you're not sure what you're doing!

## Network

### Enable SSH

Install SSH server if not already installed:
```bash
morpheus@raspberrypi:~ $ sudo apt install openssh-server
```

Start and Enable SSH:
```bash
morpheus@raspberrypi:~ $ sudo systemctl enable --now ssh
```

### Set up WiFi using nmcli

Make sure to turn on WiFi:
```bash
morpheus@raspberrypi:~ $ sudo nmcli radio wifi on
```

Scan WiFi networks:
```bash
morpheus@raspberrypi:~ $ sudo nmcli device wifi rescan
```

List WiFi networks:
```bash
morpheus@raspberrypi:~ $ sudo nmcli device wifi list
IN-USE  BSSID              SSID              MODE   CHAN  RATE         SIGNAL  BARS  SECURITY
*       01:23:45:67:89:AB  my access point   Infra  7     270 Mbits/s  91      ****  WPA2
```

Connect to WiFi (here you can either press the "Connect/WPS" button on your access point or type the password when prompted to do so):
```bash
morpheus@raspberrypi:~ $ sudo nmcli device wifi connect "my access point" --ask
```