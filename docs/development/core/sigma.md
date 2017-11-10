# Apex Sigma Central Core

## About

The absolute central control core of Apex Sigma. Loads all other mechanics and modules and is ran by the `/run.py` executable. In charge of handling all initialization and data processing for events and commands.

## Components

### [`class ApexSigma()`](#class-apexsigma)

> Arguments: `discord.py` client class.

Class container of Apex Sigma initialized with a [`discord.py`](https://discordpy.readthedocs.io/en/rewrite/) client class, located in `/sigma/core/sigma.py`. If the client is set to be an official bot client the class is set to [`discord.AutoShardedClient()`](https://discordpy.readthedocs.io/en/rewrite/api.html#discord.AutoShardedClient), otherwise, if the bot is set to run on a user account, as a self-bot, it uses the [`discord.Client()`](https://discordpy.readthedocs.io/en/rewrite/api.html#discord.Client) class. Resposible for handling events with re-based asyncronous `on_{event}` event calls.

#### [`create_cache()`](#createcache)

> Arguments: None

A simple method launched on startup. Cleans and creates the `/cache` folder. If the folder doesn't exist, it will make it, if it does, it will first delete it.

#### [`init_logger()`](#initlogger)

> Arguments: None

Launches on startup. Creates the logger for the main core and adds it to the core [`ApexSigma`](#class-apexsigma) class. The logger is handled by the `/sigma/core/mechanics/logger.py` module and the [`Logger()`](./mechanics/logger.md#class-logger) class. The logger is appended to the core as a `log` attribute.

#### [`init_config()`](#initconfig)

> Arguments: None

When the client class is initialized the [`Configuration()`](./mechanics/config.md#class-configuration) class from `/sigma/core/mechanics/config.py` is loaded up. It will load all of the data from the required files located in the `/config/core` folder. For details on how to configure and use the configuration folder and it's files you can go to the guide [here](../../configuration/core.md). The config is appended to the core as a `cfg` attribute.

#### [`init_database()`](#initdatabase)

> Arguments: None

During startup the client tries to establish a connection to the MongoDB server running on the address specified in your [configuration](../../configuration/core.md) along the credentials you have specified. The [`Database()`](./mechanics/database.md#class-database) is loaded from `/sigma/core/mechanics/database.py` module. If the client fails to connect to the database the bot will shut down with the error code `10060` ([`errno.ETIMEDOUT`](https://docs.python.org/3/library/errno.html#errno.ETIMEDOUT)). If the specified credentials are invalid and the connection is rejected by the database the bot will shut down with the error code `13` ([`errno.EACCES`](https://docs.python.org/3/library/errno.html#errno.EACCES)). The databse is appended to the core as a `db` attribute.

#### [`init_cool_down()`](#initcooldown)

> Arguments: None

Initializes the [`Cooldown()`](./mechanics/cooldown.md#class-cooldowncontrol) class from the `/sigma/core/mechanics/cooldown.py` module and adds it to the control core. The cooldown control core is appended to the main core as a `cd` attribute.

#### [`init_music()`](#initmusic)

> Arguments: None

Loads and adds the [`MusicCore()`](./mechanics/music.md#class-musiccore) class from the `/sigma/core/mechanics/music.py` module. The music control core is added to the core as a `music` attribute.

#### [`init_modules()`](#initmodules)

> Arguments: `init=bool`

Lods up the [`PluginManager()`](./mechanics/plugman.md#class-pluginmanager) class from `/sigma/core/mechanics/plugman.py` which in turns makes it load all of Sigma's event and command modules. The `init` argument determines if the Plugin Manager should log all modules that are imported. This is `True` on startup but `False` by default for use with the `>>reload` command. The Plugin Manager is appended to the core as a `modules` attribute.

#### [`get_prefix()`](#getprefix)

> Arguments: `message=`[`discord.Message`](https://discordpy.readthedocs.io/en/rewrite/api.html#discord.Message)

Due to Sigma having dynamic prefixes that each guild is able to set up for themselves this function is used for getting and returning the valid prefix for each message. If the message is a direct message, it uses the default prefix set in the [configuration](../../configuration/core.md), if it's not, it checks if the guild has a custom prefix set, again if they do not, uses the default one, if they do, it uses their personalized one. The end prefix value is returned as a `string`.

#### [`run()`](#run)

> Arguments: None

After full initialization the run method is called starting the connection establishing process to Discord's gateway servers. If the `token` in your core [configuration](../../configuration/core.md) is invalid it will shut down with the error code `1` ([`errno.EPERM`](https://docs.python.org/3/library/errno.html#errno.EPERM)).
