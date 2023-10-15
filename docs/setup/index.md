# Setup and Running

I recommend making a VENV, a virtual python environment.
This prevents package conflicts and localizes all dependencies.
It keeps you from messing up your main Python installation and pip packages.

If you don't care,
or use a system in which they're isolated in a different way,
feel free to skip this.

## Initialization

Open Sigma's directory in your terminal and init the venv with this.

```
python -m venv .venv
```

It'll create a new folder in the directory named `.venv`.

## Activation

For now, your environment is still using your main Python installation.
To tell your terminal to use the VENV, run the following based on your OS.
You can tell what you're using by what it says in your terminal.
For example, if it says just `alex@LUCI ~/apex-sigma (master)>`,
it means you are **not** using the VENV.
But if you see a `(.venv)` at the front,
making it `(.venv) alex@LUCI ~/apex-sigma (master)>`,
then the VENV is active and ready for use.
This only persists for the current terminal instance,
so just closing the terminal is enough to deactivate it.

### Linux

```sh
source .venv/bin/activate
```

### Windows

```bat
.venv\Scripts\activate.bat
```

Or if you need the one for PowerShell, it's:

```bat
.venv\Scripts\activate.psl
```

## Installation

This part just explains how to get PyPi package requirements.
Which sort of translates to installing Sigma.

Open Sigma's directory in a terminal, activate your VENV (if you use one),
and run the following.

```
pip install -Ur requirements.txt
```

This is the part where you grab a drink while it finishes.
The speed depends on both your network speed and processing power.

## Running

Again, if you have a VENV, make sure it's activated,
and just run the following from Sigma's directory.

```
python run.py
```

If everything's set up correctly you'll see a successful Discord connetion.
If not, you'll be told what went wrong.
