## Quick Setup
### With Vagrant

Install [Vagrant](https://www.vagrantup.com) and [VirtualBox](https://www.virtualbox.org).

Open a terminal window and change to the cloned project directory.

Run `vagrant up`, and wait until Vagrant is finished bootstrapping the VM (depending on your system this can take a while).

You should now have a running bot instance inside a virtual machine.

You can open a terminal session to the machine with the `vagrant ssh` command.


### Without Vagrant, Linux Systems

Prerequisites
1. Python 3.6 or higher
  `
  sudo apt-get install build-essential checkinstall
  sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
  cd /usr/src
  wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
  sudo tar xzf Python-3.6.0.tgz
  cd Python-3.6.0
  sudo ./configure
  sudo make altinstall
  `
2. [MongoDB](https://docs.mongodb.com/tutorials/install-mongodb-on-ubuntu/])

Creating a discord application
1. Ensure that you are logged in to your Discord account and go to the [developers page](https://discordapp.com/developers/applications/me)
2. Create a new app with any name and any profile picture (these can be changed later with `setusername` and `setavatar`)
3. On the second "Create App" page, click "Create a Bot User" and confirm.
4. Click to reveal your token (not client secret). You will need it later.

Setup
1. Run `git clone https://github.com/aurora-pro/apex-sigma-core.git` to clone the repository.
2. Run `cd apex-sigma-core && python3.6 -m pip install -Ur requirements.txt` to install the pip modules.
3. Run `git submodule update --init --recursive` to get the submodules.
3. If you want music, run `sudo apt-get install ffmpeg`.
4. Run `cd ~/apex-sigma-core/config && mkdir core && mkdir plugins && cd core` to create some directories and navigate to the core directory.
5. Use `nano` command to create and edit the core files as shown [here](https://sigma.readthedocs.io/en/latest/configuration/core/#making-the-core-yamls)
6. Run `cd ~/apex-sigma-core && python3.6 run.py` to start up the bot.
