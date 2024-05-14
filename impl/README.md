# Installation

## OS installation
Install RaspianOS Bullseye Legacy 32 bit (released 2024-03-12) full desktop on the Raspberry Pi, tested on Raspberry Pi 4 model B.

Keep username `pi` as it is necessary to complete installation of touch screen drivers successfully.

## Preparing the OS for the touchscreen

Used was Waveshare LCD 35B-v2 touchscreen. For more details in case of utilization of different hardware parts or operating systems follow tutorial: https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(A)

Following commands prepare the operating system for the touchscreen by downloading installing necessary packages and screen driver.

```bash
sudo apt update
sudo apt upgrade
sudo apt install cmake
sudo apt-get install libraspberrypi-dev raspberrypi-kernel-headers
rm -rf Bookshelf Documents/ Downloads/ Music/ Pictures/ Public/ Templates/ Videos/
git clone https://github.com/waveshare/LCD-show.git
cd LCD-show/
chmod +x LCD35B-show-V2
./LCD35B-show-V2
cd ~
```

### Removing cursor
To remove the cursor in the OS, simply add a `nocursor` option as follows in the file (`/etc/lightdm/lightdm.conf`)
```
xserver-command = X -nocursor
```

No cursor is displayed whatsoever. You can still put your finger on the touch screen and do what you normally do with your mouse pointer, clicking or dragging.

## Installing Proxmark software

Following command installs necessary dependencies for the Proxmark3 software.
```
sudo apt install libreadline-dev gcc-arm-none-eabi libssl-dev cmake liblz4-dev libbz2-dev
```

Following command clones the Proxmark3 repository.
```bash
git clone https://github.com/RfidResearchGroup/proxmark3.git
```
Next it is important to copy `Makefile.platform.sample` to `Makefile.platform`, uncomment `PLATFORM=PM3GENERIC` and comment out `PLATFORM=PM3RDV4`. This will set up the program for Proxmark 3 Easy device.

Following script compiles and install the Proxmark3 software
```bash
make all && make install
```

## Flashing the Proxmark 3 Easy

> Before proceeding, ensure to disable ModemManager on the utilized system! More information avaiable here: https://github.com/RfidResearchGroup/proxmark3/blob/master/doc/md/Installation_Instructions/ModemManager-Must-Be-Discarded.md

After successful installation of Proxmark3, flash the Proxmark 3 Easy device by connecting the device to the computer and by running following script.

```
sudo ./pm3-flash-all
```

## Installing this software

```shell
git clone git@gitlab.fit.cvut.cz:benesm41/final-project.git cloner
```
To install necessary files, run following commands

```
chmod +x install.sh
./install.sh
```

And then edit the config file in `~/.cloner` for your preferences. Default values are set.

After rebooting, the program starts on immediatelly and the device is ready to use.
