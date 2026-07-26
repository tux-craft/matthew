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
- [Raspberry Pi Camera Module 3 _NoIR_](https://www.raspberrypi.com/products/camera-module-3/)
- [Raspberry Pi Camera Cable](https://www.raspberrypi.com/products/camera-cable/)
- 20000 mAh Powerbank (e.g. [Intenso 7313550 Powerbank XS 20000](https://www.intenso.de/en/products/powerbanks/xs5000-xs10000-xs20000/))
- Infrared LED Module

To assemble the hardware I used the instructions from [My Naturewatch](https://mynaturewatch.net/infrared).

## Prerequisites

Install the latest version of Raspberry Pi OS following the [official documentation](https://www.raspberrypi.com/software/).