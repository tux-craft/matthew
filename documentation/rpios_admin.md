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

### Setting up a Headless Raspberry Pi

> [!IMPORTANT]
> The following documentation is a copy of an older, now offline documentation from Raspberry Pi. You can still view the original page thanks to [The Wayback Machine](https://web.archive.org/): https://web.archive.org/web/20211009054952/https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi
>
> As this documentation has been removed, it might not be applicable for newer versions of Rapsberry Pi or Raspberry Pi OS.
> Use at your own risk!

If you do not use a monitor or keyboard to run your Pi (known as headless), but you still need to do some wireless setup, there is a facility to enable wireless networking and SSH when creating a image.

Once an image is created on an SD card, by inserting it into a card reader on a Linux or Windows machines the [boot folder](https://web.archive.org/web/20211009054952/https://www.raspberrypi.com/documentation/computers/configuration.html#the-boot-folder) can be accessed. Adding certain files to this folder will activate certain setup features on the first boot of the Raspberry Pi.

#### Configuring Networking

You will need to define a `wpa_supplicant.conf` file for your particular wireless network. Put this file onto the boot folder of the SD card. When the Raspberry Pi boots for the first time, it will copy that file into the correct location in the Linux root file system and use those settings to start up wireless networking.

The Raspberry Pi’s IP address will not be visible immediately after power on, so this step is crucial to connect to it headlessly. Depending on the OS and editor you are creating this on, the file could have incorrect newlines or the wrong file extension so make sure you use an editor that accounts for this. Linux expects the line feed (LF) newline character.

> [!WARNING]
> After your Raspberry Pi is connected to power, make sure to wait a few (up to 5) minutes for it to boot up and register on the network.

A `wpa_supplicant.conf` file example:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
country=<Insert 2 letter ISO 3166-1 country code here>
update_config=1

network={
 ssid="<Name of your wireless LAN>"
 psk="<Password for your wireless LAN>"
}
```

Where the country code should be set the two letter ISO/IEC alpha2 code for the country in which you are using, e.g.
- GB (United Kingdom)
- FR (France)
- DE (Germany)
- US (United States)
- SE (Sweden)

Here is a more elaborate example that should work for most typical wpa2 personal networks. This template below works for 2.4ghz/5ghz hidden or not networks. The utilization of quotes around the ssid - psk can help avoid any oddities if your network ssid or password has special chars (! @ # $ etc)

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<Insert 2 letter ISO 3166-1 country code here>

network={
        scan_ssid=1
        ssid="<Name of your wireless LAN>"
        psk="<Password for your wireless LAN>"
        proto=RSN
        key_mgmt=WPA-PSK
        pairwise=CCMP
        auth_alg=OPEN
}
```

> [!NOTE]
> Some older Raspberry Pi boards and some USB wireless dongles do not support 5GHz networks.

> [!NOTE]
> With no keyboard or monitor, you will need some way of [remotely accessing](https://web.archive.org/web/20211009054918/https://www.raspberrypi.com/documentation/computers/remote-access.html#remote-access) your headless Raspberry Pi. For headless setup, SSH can be enabled by placing a file named `ssh`, without any extension, onto the boot folder of the SD Card. For more information see the section on [setting up an SSH server](https://web.archive.org/web/20211009054918/https://www.raspberrypi.com/documentation/computers/remote-access.html#ssh).

### Setting up a Routed Wireless Access Point

> [!IMPORTANT]
> The following documentation is a copy of an older, now offline documentation from Raspberry Pi. You can still view the original page thanks to [The Wayback Machine](https://web.archive.org/): https://web.archive.org/web/20211009054952/https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-routed-wireless-access-point
>
> As this documentation has been removed, it might not be applicable for newer versions of Rapsberry Pi or Raspberry Pi OS.
> Use at your own risk!

A Raspberry Pi within an Ethernet network can be used as a wireless access point, creating a secondary network. The resulting new wireless network is entirely managed by the Raspberry Pi.

If you wish to extend an existing Ethernet network to wireless clients, consider instead setting up a bridged access point.

```
                                         +- RPi -------+
                                     +---+ 10.10.0.2   |          +- Laptop ----+
                                     |   |     WLAN AP +-)))  (((-+ WLAN Client |
                                     |   | 192.168.4.1 |          | 192.168.4.2 |
                                     |   +-------------+          +-------------+
                 +- Router ----+     |
                 | Firewall    |     |   +- PC#2 ------+
(Internet)---WAN-+ DHCP server +-LAN-+---+ 10.10.0.3   |
                 |   10.10.0.1 |     |   +-------------+
                 +-------------+     |
                                     |   +- PC#1 ------+
                                     +---+ 10.10.0.4   |
                                         +-------------+
```

A routed wireless access point can be created using the inbuilt wireless features of the Raspberry Pi 4, Raspberry Pi 3 or Raspberry Pi Zero W, or by using a suitable USB wireless dongle that supports access point mode. It is possible that some USB dongles may need slight changes to their settings.

This documentation was tested on a Raspberry Pi 3B running a fresh installation of Raspberry Pi OS Buster.

#### Before you Begin

- Ensure you have administrative access to your Raspberry Pi. The network setup will be modified as part of the installation: local access, with screen and keyboard connected to your Raspberry Pi, is recommended.

- Connect your Raspberry Pi to the Ethernet network and boot the Raspberry Pi OS.

- Ensure the Raspberry Pi OS on your Raspberry Pi is up-to-date and reboot if packages were installed in the process.

- Take note of the IP configuration of the Ethernet network the Raspberry Pi is connected to:

  - In this document, we assume IP network `10.10.0.0/24` is configured on the Ethernet LAN, and the Raspberry Pi is going to manage IP network `192.168.4.0/24` for wireless clients.

  - Please select another IP network for wireless, e.g. `192.168.10.0/24`, if IP network `192.168.4.0/24` is already in use by your Ethernet LAN.

- Have a wireless client (laptop, smartphone, …​) ready to test your new access point.

#### Install AP and Management Software

In order to work as an access point, the Raspberry Pi needs to have the `hostapd` access point software package installed:

```bash
sudo apt install hostapd
```

Enable the wireless access point service and set it to start when your Raspberry Pi boots:

```bash
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
```

In order to provide network management services (DNS, DHCP) to wireless clients, the Raspberry Pi needs to have the `dnsmasq` software package installed:

```bash
sudo apt install dnsmasq
```

Finally, install `netfilter-persistent` and its plugin `iptables-persistent`. This utilty helps by saving firewall rules and restoring them when the Raspberry Pi boots:

```bash
sudo DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent
```

Software installation is complete. We will configure the software packages later on.

#### Set up the Network Router

The Raspberry Pi will run and manage a standalone wireless network. It will also route between the wireless and Ethernet networks, providing internet access to wireless clients. If you prefer, you can choose to skip the routing by skipping the section "Enable routing and IP masquerading" below, and run the wireless network in complete isolation.

##### Define the Wireless Interface IP Configuration

The Raspberry Pi runs a DHCP server for the wireless network; this requires static IP configuration for the wireless interface (`wlan0`) in the Raspberry Pi. The Raspberry Pi also acts as the router on the wireless network, and as is customary, we will give it the first IP address in the network: `192.168.4.1`.

To configure the static IP address, edit the configuration file for `dhcpcd` with:

```bash
sudo nano /etc/dhcpcd.conf
```

Go to the end of the file and add the following:

```
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
```

##### Enable Routing and IP Masquerading

This section configures the Raspberry Pi to let wireless clients access computers on the main (Ethernet) network, and from there the internet.

> [!NOTE]
> If you wish to block wireless clients from accessing the Ethernet network and the internet, skip this section.

To enable routing, i.e. to allow traffic to flow from one network to the other in the Raspberry Pi, create a file using the following command, with the contents below:

```bash
sudo nano /etc/sysctl.d/routed-ap.conf
```

File contents:

```
# Enable IPv4 routing
net.ipv4.ip_forward=1
```

Enabling routing will allow hosts from network `192.168.4.0/24` to reach the LAN and the main router towards the internet. In order to allow traffic between clients on this foreign wireless network and the internet without changing the configuration of the main router, the Raspberry Pi can substitute the IP address of wireless clients with its own IP address on the LAN using a "masquerade" firewall rule.

- The main router will see all outgoing traffic from wireless clients as coming from the Raspberry Pi, allowing communication with the internet.

- The Raspberry Pi will receive all incoming traffic, substitute the IP addresses back, and forward traffic to the original wireless client.

This process is configured by adding a single firewall rule in the Raspberry Pi:

```bash
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

Now save the current firewall rules for IPv4 (including the rule above) and IPv6 to be loaded at boot by the `netfilter-persistent` service:

```bash
sudo netfilter-persistent save
```

Filtering rules are saved to the directory `/etc/iptables/`. If in the future you change the configuration of your firewall, make sure to save the configuration before rebooting.

##### Configure the DHCP and DNS services for the wireless network

The DHCP and DNS services are provided by `dnsmasq`. The default configuration file serves as a template for all possible configuration options, whereas we only need a few. It is easier to start from an empty file.

Rename the default configuration file and edit a new one:

```bash
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo nano /etc/dnsmasq.conf
```

Add the following to the file and save it:

```
interface=wlan0 # Listening interface
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
                # Pool of IP addresses served via DHCP
domain=wlan     # Local wireless DNS domain
address=/gw.wlan/192.168.4.1
                # Alias for this router
```

The Raspberry Pi will deliver IP addresses between `192.168.4.2` and `192.168.4.20`, with a lease time of 24 hours, to wireless DHCP clients. You should be able to reach the Raspberry Pi under the name `gw.wlan` from wireless clients.

There are many more options for `dnsmasq`; see the default configuration file (`/etc/dnsmasq.conf`) or the [online documentation](https://thekelleys.org.uk/dnsmasq/doc.html) for details.

#### Ensure Wireless Operation

Countries around the world regulate the use of telecommunication radio frequency bands to ensure interference-free operation. The Linux OS helps users [comply](https://wireless.docs.kernel.org/en/latest/en/developers/regulatory/statement.html) with these rules by allowing applications to be configured with a two-letter "WiFi country code", e.g. `US` for a computer used in the United States.

In the Raspberry Pi OS, 5 GHz wireless networking is disabled until a WiFi country code has been configured by the user, usually as part of the initial installation process (see wireless configuration pages in this [section](https://web.archive.org/web/20211009054952/https://www.raspberrypi.com/documentation/computers/configuration.html#configuring-networking) for details.)

To ensure WiFi radio is not blocked on your Raspberry Pi, execute the following command:

```bash
sudo rfkill unblock wlan
```

This setting will be automatically restored at boot time. We will define an appropriate country code in the access point software configuration, next.

#### Configure the AP Software

Create the `hostapd` configuration file, located at `/etc/hostapd/hostapd.conf`, to add the various parameters for your new wireless network.

```bash
sudo nano /etc/hostapd/hostapd.conf
```

Add the information below to the configuration file. This configuration assumes we are using channel 7, with a network name of `NameOfNetwork`, and a password `AardvarkBadgerHedgehog`. Note that the name and password should **not** have quotes around them. The passphrase should be between 8 and 64 characters in length.

```
country_code=GB
interface=wlan0
ssid=NameOfNetwork
hw_mode=g
channel=7
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=AardvarkBadgerHedgehog
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

Note the line `country_code=GB`: it configures the computer to use the correct wireless frequencies in the United Kingdom. **Adapt this line** and specify the two-letter ISO code of your country. See [Wikipedia](https://en.wikipedia.org/wiki/ISO_3166-1) for a list of two-letter ISO 3166-1 country codes.

To use the 5 GHz band, you can change the operations mode from `hw_mode=g` to `hw_mode=a`. Possible values for hw_mode are:

- a = IEEE 802.11a (5 GHz) (Raspberry Pi 3B+ onwards)
- b = IEEE 802.11b (2.4 GHz)
- g = IEEE 802.11g (2.4 GHz)

Note that when changing the `hw_mode`, you may need to also change the `channel` - see [Wikipedia](https://en.wikipedia.org/wiki/List_of_WLAN_channels) for a list of allowed combinations.

#### Running the new Wireless AP

Now restart your Raspberry Pi and verify that the wireless access point becomes automatically available.

```bash
sudo systemctl reboot
```

Once your Raspberry Pi has restarted, search for wireless networks with your wireless client. The network SSID you specified in file `/etc/hostapd/hostapd.conf` should now be present, and it should be accessible with the specified password.

If SSH is enabled on the Raspberry Pi, it should be possible to connect to it from your wireless client as follows, assuming the `pi` account is present: `ssh pi@192.168.4.1` or `ssh pi@gw.wlan`

If your wireless client has access to your Raspberry Pi (and the internet, if you set up routing), congratulations on setting up your new access point!

If you encounter difficulties, contact the [forums](https://forums.raspberrypi.com/) for assistance. Please refer to this page in your message.

### Setting up a Bridged Wireless Access Point

> [!IMPORTANT]
> The following documentation is a copy of an older, now offline documentation from Raspberry Pi. You can still view the original page thanks to [The Wayback Machine](https://web.archive.org/): https://web.archive.org/web/20211009054952/https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-bridged-wireless-access-point
>
> As this documentation has been removed, it might not be applicable for newer versions of Rapsberry Pi or Raspberry Pi OS.
> Use at your own risk!

The Raspberry Pi can be used as a bridged wireless access point within an existing Ethernet network. This will extend the network to wireless computers and devices.

If you wish to create a standalone wireless network, consider instead setting up a [routed access point](https://web.archive.org/web/20211009054952/https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-routed-wireless-access-point).

```
                                         +- RPi -------+
                                     +---+ 10.10.0.2   |          +- Laptop ----+
                                     |   |     WLAN AP +-)))  (((-+ WLAN Client |
                                     |   |  Bridge     |          | 10.10.0.5   |
                                     |   +-------------+          +-------------+
                 +- Router ----+     |
                 | Firewall    |     |   +- PC#2 ------+
(Internet)---WAN-+ DHCP server +-LAN-+---+ 10.10.0.3   |
                 |   10.10.0.1 |     |   +-------------+
                 +-------------+     |
                                     |   +- PC#1 ------+
                                     +---+ 10.10.0.4   |
                                         +-------------+
```

A bridged wireless access point can be created using the inbuilt wireless features of the Raspberry Pi 4, Raspberry Pi 3 or Raspberry Pi Zero W, or by using a suitable USB wireless dongle that supports access point mode. It is possible that some USB dongles may need slight changes to their settings. If you are having trouble with a USB wireless dongle, please check the [forums](https://forums.raspberrypi.com/).

This documentation was tested on a Raspberry Pi 3B running a fresh installation of Raspberry Pi OS Buster.

#### Before you Begin

- Ensure you have administrative access to your Raspberry Pi. The network setup will be entirely reset as part of the installation: local access, with screen and keyboard connected to your Raspberry Pi, is recommended.

> [!NOTE]
> If installing remotely via SSH, connect to your Raspberry Pi **by name** rather than by IP address, e.g. `ssh pi@raspberrypi.local`, as the address of your Raspberry Pi on the network will probably change after installation. You should also be ready to add screen and keyboard if needed in case you lose contact with your Raspberry Pi after installation.

- Connect your Raspberry Pi to the Ethernet network and boot the Raspberry Pi OS.

- Ensure the Raspberry Pi OS on your Raspberry Pi is up-to-date and reboot if packages were installed in the process.

- Have a wireless client (laptop, smartphone, …​) ready to test your new access point.

#### Install AP and Management Software


In order to work as a bridged access point, the Raspberry Pi needs to have the `hostapd` access point software package installed:

```bash
sudo apt install hostapd
```

Enable the wireless access point service and set it to start when your Raspberry Pi boots:

```bash
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
```

Software installation is complete. We will configure the access point software later on.

#### Setup the Network Bridge

A bridge network device running on the Raspberry Pi will connect the Ethernet and wireless networks using its built-in interfaces.

##### Create a bridge device and populate the bridge

Add a bridge network device named `br0` by creating a file using the following command, with the contents below:

```bash
sudo nano /etc/systemd/network/bridge-br0.netdev
```

File contents:

```
[NetDev]
Name=br0
Kind=bridge
```

In order to bridge the Ethernet network with the wireless network, first add the built-in Ethernet interface (`eth0`) as a bridge member by creating the following file:

```bash
sudo nano /etc/systemd/network/br0-member-eth0.network
```

File contents:

```
[Match]
Name=eth0

[Network]
Bridge=br0
```

> [!NOTE]
> The access point software will add the wireless interface `wlan0` to the bridge when the service starts. There is no need to create a file for that interface. This situation is particular to wireless LAN interfaces.

Now enable the `systemd-networkd` service to create and populate the bridge when your Raspberry Pi boots:

```bash
sudo systemctl enable systemd-networkd
```

##### Define the bridge device IP configuration

Network interfaces that are members of a bridge device are never assigned an IP address, since they communicate via the bridge. The bridge device itself needs an IP address, so that you can reach your Raspberry Pi on the network.

`dhcpcd`, the DHCP client on the Raspberry Pi, automatically requests an IP address for every active interface. So we need to block the `eth0` and `wlan0` interfaces from being processed, and let `dhcpcd` configure only `br0` via DHCP.

```bash
sudo nano /etc/dhcpcd.conf
```

Add the following line near the beginning of the file (above the first `interface xxx` line, if any):

```
denyinterfaces wlan0 eth0
```

Go to the end of the file and add the following:

```
interface br0
```

With this line, interface `br0` will be configured in accordance with the defaults via DHCP. Save the file to complete the IP configuration of the machine.

#### Ensure Wireless Operation

Countries around the world regulate the use of telecommunication radio frequency bands to ensure interference-free operation. The Linux OS helps users [comply](https://wireless.docs.kernel.org/en/latest/en/developers/regulatory/statement.html) with these rules by allowing applications to be configured with a two-letter "WiFi country code", e.g. `US` for a computer used in the United States.

In the Raspberry Pi OS, 5 GHz wireless networking is disabled until a WiFi country code has been configured by the user, usually as part of the initial installation process (see wireless configuration pages in this [section](https://web.archive.org/web/20211009054952/https://www.raspberrypi.com/documentation/computers/configuration.html#configuring-networking) for details.)

To ensure WiFi radio is not blocked on your Raspberry Pi, execute the following command:

```bash
sudo rfkill unblock wlan
```

This setting will be automatically restored at boot time. We will define an appropriate country code in the access point software configuration, next.

#### Configure the AP Software

Create the hostapd configuration file, located at `/etc/hostapd/hostapd.conf`, to add the various parameters for your new wireless network.

```bash
sudo nano /etc/hostapd/hostapd.conf
```

Add the information below to the configuration file. This configuration assumes we are using channel 7, with a network name of `NameOfNetwork`, and a password `AardvarkBadgerHedgehog`. Note that the name and password should **not** have quotes around them. The passphrase should be between 8 and 64 characters in length.

```
country_code=GB
interface=wlan0
bridge=br0
ssid=NameOfNetwork
hw_mode=g
channel=7
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=AardvarkBadgerHedgehog
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

Note the lines `interface=wlan0` and `bridge=br0`: these direct `hostapd` to add the `wlan0` interface as a bridge member to `br0` when the access point starts, completing the bridge between Ethernet and wireless.

Note the line `country_code=GB`: it configures the computer to use the correct wireless frequencies in the United Kingdom. **Adapt this line** and specify the two-letter ISO code of your country. See [Wikipedia](https://en.wikipedia.org/wiki/ISO_3166-1) for a list of two-letter ISO 3166-1 country codes.

To use the 5 GHz band, you can change the operations mode from `hw_mode=g` to `hw_mode=a`. Possible values for hw_mode are:

- a = IEEE 802.11a (5 GHz) (Raspberry Pi 3B+ onwards)
- b = IEEE 802.11b (2.4 GHz)
- g = IEEE 802.11g (2.4 GHz)

Note that when changing the `hw_mode`, you may need to also change the `channel` - see [Wikipedia](https://en.wikipedia.org/wiki/List_of_WLAN_channels) for a list of allowed combinations.

#### Run the new Wireless AP

Now restart your Raspberry Pi and verify that the wireless access point becomes automatically available.

```bash
sudo systemctl reboot
```

Once your Raspberry Pi has restarted, search for wireless networks with your wireless client. The network SSID you specified in file `/etc/hostapd/hostapd.conf` should now be present, and it should be accessible with the specified password.

If your wireless client has access to the local network and the internet, congratulations on setting up your new access point!

If you encounter difficulties, contact the [forums](https://forums.raspberrypi.com/) for assistance. Please refer to this page in your message.
