# Module Construction Guide

## About

Sigma has her own internal framework that is used for handling commands and the functions that they can access. This will explain how the Apex Sigma module framework works and how to control it as well as some examples for basic functions.

## Modules

Sigma's modules are composed of two main things, a module information `.yml` and the module `.py` file and function. In the following examples we'll make a simple `>>ping` command that will respond with a simple text message and the bot's latency and a message event that will unflip tables.

### Preparation

The modules are stored in `sigma/modules` and grouped into folders. For organization and clarity during the guide we'll make a new folder in the `modules` folder and name it `custom`. Within that folder create two new files, `module.yml`, `ping.py` and `unflipper.py`. Since we said that the command we're making is named ping, the `.py` file for it must be named `ping.py`.

### YAML Information Container

The YAML information container is the `module.yml` file we previously created, and it looks like this.

#### Layout

```yml
name:            Custom Commands # The name of the module.
category:        custom          # The category of the module.
enabled:         true            # Is the module enabled or not.

commands:                        # List of commands in the module.
  - name:        ping            # Name of the command function.
    alts:                        # List of aliases for that command.
      - "pang"
    enabled:     true            # Is the command enabled or not.
    permissions:                 # Permission settings for the command.
      nsfw:      false           # Is the command a NSFW command.
      owner:     false           # Is the command only for owners.
      dmable:    true            # Can the command be used in DMs.
    usage:       "{pfx}{cmd}"    # Usage example for the command.
    description:                 # The description of the command.
      "Returns a message with the bot's current latency."

events:                          # List of events in the module.
  - name:        unflipper       # Name of the event function.
    type:        message         # Type of the event it listens for.
    enabled:     true            # Is the event enabled or not.
```

#### Module Keys

- `name`: The name of the module used for organization and vanity.
- `category`: The category of the module, when the `>>modules` command is used, it lists all the module categories. The category of modules that this one falls into.
- `enabled`: If set to `true` the module and it's nested commands are loaded, if `false` no command in that module will be loaded.
- `commands`: A list of dicts that contain information about each command that is a part of that module.

#### Command Keys

- `name`: The name of the file and function of the command as well as the main command that function responds to.
- `alts`: Alternative commands that will call the same function.
- `enabled`: If set to `true` the command will be loaded, if `false` it will not be loaded.
- `permissions`: Contains details of where the command can be used and by who.
- `usage`: The usage example of the command. It usually has `{pfx}` and `{cmd}` in it, being the `Prefix` and `Command Name` respectively.
- `description`: The verbose description of the command with details about it.

#### Permission Keys

- `nsfw`: Detemines if the command is usable anywhere or just in NSFW channels.
- `owner`: Determines if the command is usable by anyone or just the bot's owners.
- `partner`: Determines if the command is usable anywhere or just on partner servers.
- `dmable`: Determines if the command is usable in Direct Messages or only on guilds.

#### Event Keys

- `name` The name of the file and function of the event that is called.
- `type`: The type of event the function listens for. This is any event from the `discord.py` library with the `on_` removed from it's name. Such as `on_message`, `on_member_join` and the like, resulting in `message` and `member_join`.
- `enabled`: If set to `true` the event will be loaded, if `false` it will not be loaded.

### Ping Command

The code of the actual `>>ping` command and function. The following code goes into `ping.py` that we created.

```py
async def ping(cmd, message, args):
    bot_latency = round(cmd.bot.latency * 1000, 2)
    response = f'Pong! Latency: {bot_latency}ms'
    await message.channel.send(response)
```

So what does all this mean. We defined a new asyncronous function using `async def` and named it `ping` after our command and file name. Every command takes `3` arguments which are `cmd`, `message` and `args`.

- `cmd`: Main command class, the gateway to accessing the command's internal function as well as the `bot` class which is the main discord client connection class.
- `message`: The `discord.Message()` class that was passed when the message was sent, containing it's contents, who the author is, where it was sent and similar information.
- `args`: Short for `arguments` it is a list of what else the message had in it besides the command. For example if the command entered was `>>ping me daddy` args would contain `['me', 'daddy']` in it, otherwise it's an empty list.

We grabbed the bot's latency accessible through the client's attribute of `.latency`. Since it is stored as a `float` in seconds (for example `0.0694123`) we multiplied it by `1000` to get the latency in miliseconds and rounded the number to `2` decimals. We made a new string response from that using a `fString` which was introduced in Python 3.6 that will be sent as a reply. Then we call and await the method to send the response to the channel where the command, that is the message that called the command, originated from.

### Unflipper Event

The code of the `on_message`, that is the `message` event in Sigma that will result in automatically unflipped tables. This code resides in `unflipper.py` as created earlier and specified in the `module.yml`.

```py
async def unflipped(ev, message):
    flipped_table = '(╯°□°）╯︵ ┻━┻'
    if flipped_table in message.content:
        unflipped_table = '┬─┬﻿ ノ( ゜-゜ノ)'
        await message.channel.send(unflipped_table)
```

Events are composed of an `ev` argument as it's core argument contained in every event, however depending on the event type, other arguments might be present, they might be members, guilds, messages, etc. In this example that is a `message` argument due to the event being triggered by a `message` event.

- `ev`: Main event class, the same as the `cmd` argument for commands, giving access to the bot core and functions from the event.
- `*args`: Whatever arguments the event has in it other than `ev` depending on it's type.

The command checks if the content of the message sent has a flipped table in it. If it does it responds to that channel with an unflipped table, simple enough.