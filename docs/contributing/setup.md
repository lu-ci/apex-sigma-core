## Quick Setup

Install [Vagrant](https://www.vagrantup.com) and [VirtualBox](https://www.virtualbox.org).

Open a terminal window and change to the cloned project directory.

Run `vagrant up`, and wait until Vagrant is finished bootstrapping the VM (depending on your system this can take a while).

You should now have a running bot instance inside a virtual machine.

You can open a terminal session to the machine with the `vagrant ssh` command.


### without Vagrant

Please make sure you have [Python](https://www.python.org/) version 3.6 or higher installed on your system.

Also, make sure you have a [MongoDB](https://www.mongodb.com/) server running.

Consult the respective documentation for instructions how to set them up.

Open a terminal window and change to the cloned project directory.

Edit the file named `config/discord.yml` and replace `token: "TOKEN"` with your actual discord bot token.
