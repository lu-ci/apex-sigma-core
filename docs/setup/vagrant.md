# Vagrant Installation Method

> Vagrant is a virtual environment creation tool for quickly running software. Sigma has a pre-made script to work with Vagrant and help you out quickly start Sigma.

## Requirements

* UTF-8 Text Editor: [Notepad++](https://notepad-plus-plus.org/download/) or [Atom](https://atom.io/) (*Recommended*)
* Oracle VM VirtualBox: [Download](https://www.virtualbox.org/wiki/Downloads)
* HashiCorp Vagrant: [Download](https://www.vagrantup.com/downloads.html)
* GIT Client: [Download](https://git-scm.com/)

> Please install **all** the above packages before continuing.

## Cloning The Repository

Open a command prompt/terminal and `cd` into the location you want Sigma to be in and clone Sigma's repository and update it's modules using the following commands.

```sh
git clone https://github.com/aurora-pro/apex-sigma-core.git
cd apex-sigma-core
```

## Configuration

Now, before continuing with the Vagrant machine start up, please refer to the **Configuration** part. Once you've created the configuration for Sigma, come back here.
You can find the core configuration documentation [here](https://sigma.readthedocs.io/en/latest/configuration/core/),
and the Discord application creation guide [here](https://sigma.readthedocs.io/en/latest/setup/discord/).

## Starting Vagrant

Ok, `cd` into your `apex-sigma-core` folder, and run the following commands to start the machine up. To work properly, you need to have finished the configuration.

```sh
vagrant up
# Wait for it to finish
# Takes a few minutes depending on your machine
# ... Grabbed a cup of tea?
# Ok it's done!
vagrant ssh
cd /vagrant
python run.py
# This is where Sigma will start up and log in.
```

That's pretty much it, it should be running, you're done.
