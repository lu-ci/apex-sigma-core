# Ubuntu Setup Guide

> A note before you start. Linux installations differ with each distribution.
This also stands for different versions of Ubuntu. This guide targets **Ubuntu
Server 16.04 Xenial**.

## Requirements

* GIT Client
* Python 3.6
* MongoDB 3.4
* Super User Permissions

## Installing Basic Packages

Before installing Python and MongoDB, we need some basic building packages.
For clarity of the list I've separated the package installations into three lines
instead of making them clutter in only one.
If you feel like it, you can just aggregate all of them.

```sh
sudo apt-get install git ffmpeg build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev
sudo apt-get install libsqlite3-dev tk-devlibgdbm-dev libc6-dev libbz2-dev
```

## Installing Python 3.6

To make sure everything is proper and installed as it's supposed to,
we will be compiling Python from source code. Reason being Ubuntu Xenial not
having Python 3.6 in it's general archive.

```sh
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tgz
sudo tar xzf Python-3.6.2.tgz
cd Python-3.6.2
sudo ./configure
sudo make altinstall
```
The configuration and compiling might take some time.
I suggest having some tea.

Once it's done, I suggest testing it by running `python3.6 --version`.

## Installing MongoDB 3.4

This is a minified and compressed version of Mongo's official guide that can
be found [here](https://docs.mongodb.com/tutorials/install-mongodb-on-ubuntu/#install-mongodb-community-edition) if you would like to read it.

```sh
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

## Setting Sigma Up

> This part explains how to pull Sigma's main repository using GIT,
how to update her when you need to, and how to install her PIP modules.

To start off you need to navigate to your home directory and pull the repository.

```sh
cd ~
git clone https://github.com/aurora-pro/apex-sigma-core.git
cd apex-sigma-core
```

Now you need to update Sigma's Python PIP modules.
If the following returns permission errors, please use the commands with `sudo`.

```sh
python3.6 -m pip install -Ur requirements.txt
```

Once this is completed, the technical parts are done.
All that is left for you to do is the Discord application creation and configuration.
You can find the Discord setup guide
[here](https://sigma.readthedocs.io/en/latest/setup/discord/)
and the Sigma core configuration guide
[here](https://sigma.readthedocs.io/en/latest/configuration/core/).

When you finish the configuration finally. Run the following.
Again, if permission issues arise, use `sudo`.

```sh
cd ~/apex-sigma-core
python3.6 run.py
```
**And enjoy your fresh self-hosted Sigma~**
