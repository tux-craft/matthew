# matthew
Nature watch camera.

## Introduction

This project is greatly inspired from [My Naturewatch](https://mynaturewatch.net/).
The original [My Naturewatch](https://mynaturewatch.net/) uses older hardware and has not been updated since Feb 23, 2022 so I decided to run my own version.
You can also have a look at the [Community edition of My Naturewatch](https://github.com/interactionresearchstudio/NaturewatchCameraServer-CommunityDevelopmentEdition) which is more up to date.

## File tree

```
matthew/
├── content/         # content to run the nature watch camera
├── documentation/   # some usefull but not strictly necessary documentation
├── LICENSE          # license file
└── README.md        # this file
```

## Hardware

This nature watch camera has been developped and tested with the following hardware:
- [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
- [Raspberry Pi Camera Module 3 **NoIR**](https://www.raspberrypi.com/products/camera-module-3/)
- [Raspberry Pi Camera Cable](https://www.raspberrypi.com/products/camera-cable/)
- 20000 mAh Powerbank (e.g. [Intenso 7313550 Powerbank XS 20000](https://www.intenso.de/en/products/powerbanks/xs5000-xs10000-xs20000/))
- Infrared LED Module

To assemble the hardware I used the instructions from [My Naturewatch](https://mynaturewatch.net/infrared).

## Installation

> [!NOTE]  
> In the following documentation the system has been installed with one user `morpheus`.
> You can obviously name it the way you want.
> In step 4. we create another user `tux-craft` which will be used to run the nature watch camera service.
> If you do not want to create this user or want another name, make sure to edit lines 6 and 7 of `matthew.service` and line 13 of `matthew.py`.

1. Install the latest version of Raspberry Pi OS following the [official documentation](https://www.raspberrypi.com/software/).

2. Update the system:
```bash
morpheus@raspberrypi:~ $ sudo apt update
morpheus@raspberrypi:~ $ sudo apt upgrade
```

3. Install necessary packages for Python:
```bash
morpheus@raspberrypi:~ $ sudo apt install python3-opencv python3-picamera2
```

4. Create user tux-craft:
```bash
morpheus@raspberrypi:~ $ sudo useradd -c "matthew service user" -d /home/tux-craft -m -s /usr/sbin/nologin tux-craft
```

5. Change the permissions of its home directory:
```bash
morpheus@raspberrypi:~ $ sudo chmod 2770 /home/tux-craft
```

6. Add your userer in the tux-craft group:
```bash
morpheus@raspberrypi:~ $ sudo usermod -a -G tux-craft morpheus
```

> [!NOTE]
> At this point you need to reload the session of your current user (log out and log back in or re-SSH in a fresh terminal)

7. Create a directory for Matthew:
```bash
morpheus@raspberrypi:~ $ mkdir /home/tux-craft/Matthew
```