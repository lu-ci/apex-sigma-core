# Configuring Sigma's Core

## Making The Folders

Inside Sigma's main directory, you should see a folder called `config`.
Inside said folder there are another two, `core` and `plugins`.
If these folders do not exist, feel free to create them.
The `core` folder contains `.yml` files used to configure Sigma's core functions.
Only the core configuration files are mandatory for Sigma to work.

## Making The Core YAMLs

Go to `config/core` and make **three** new files.

* discord.yml
* database.yml
* preferences.yml

### `discord.yml` Contents

```yml
bot:    true
token:  'myfancydiscordtokengoeshere'
owners:
  - 123456789123456789
```

* `bot`: Controls if the account the bot is running is a proper bot account.
  This is implemented as Sigma is able to be a self bot.
  If this is `false` all event handling will be disabled and the bot will only respond to itself.
  The value of the `bot` key is **boolean**.

* `token`: Your **Discord Client Token**. Which you can obtain from your applications.
  You can find your applications [Here](https://discordapp.com/developers/applications/me).
  The value of the `token` key is a **string**.
* `owners`: Contains a list of User IDs that should be marked as bot owners.
  Users with bot owners privileges can control any and all bot functions.
  Be careful who you designated as a bot owner, some functions are dangerous.
  The value of the `owners` key is a **list of integers**.

### `database.yml` Contents

```yml
database: aurora
auth:     false
host:     '127.0.0.1'
port:     27017
username: 'username'
password: 'password'
cache_type: 'memory'
```

* `database`: The name of the database object in MongoDB for storing your data.
  It can be anything you want. Changing it will cause issues as the data stored will be in another location afterwards.
  The value of the `database` key is a **string**.
* `auth`: Tells Sigma if the database requires authorization or not.
  If you have no changed any settings in Mongo, set this to `false`.
  If your MongoDB server does indeed need a username and password, set it to `true`.
  The value of the `auth` key is a **boolean**.
* `host`: Quite simply the IP address of the MongoDB server. If it's running on the same machine, set it to `127.0.0.1` or `localhost`.
  The value of the `host` key is a **string**.
* `port`: This is the connection port of the MongoDB server.
  By default it is `27017`.
  The value of the `port` key is an **integer** but can be a **string**.
* `username`: The authorization username for the MongoDB server if authorization is required.
  If authorization is not required, just input anything as the username, the key is still needed in the configuration file.
  The value of the `username` key is a **string**.
* `password`: Same as the `username` key. Used for authorization when needed. If you don't need to authorize, input anything you want, the key is still required.
  The value of the `password` key is a **string**.
* `cache_type`: This specifies the type of cache that the bot should
  use for storing temporary data during runtime to increase performance.
  In most cases for self-hosts this isn't needed due to serving a very
  tiny amount of servers and users. Consider setting this variable only
  if you ever cross around 9.000 servers or 450.000 users.
  The possible types are `none`, `memory`, `ttl`, `lru`, `redis` and `mixed`. If an unknown value is entered it will default to `none`.
  The value of the `cache_type` key is a **string**.

### `preferences.yml` Contents

```yml
dev_mode:         false
status_rotation:  true
text_only:        false
music_only:       false
prefix:           '>>'
currency:         'Kud'
currency_icon:    '⚜'
website:          'https://lucia.moe/#/sigma'
movelog_channel:  123456789123456789
errorlog_channel: 123456789123456789
key_to_my_heard:  '5up3r_53cr3t_3ncrypt10n'
```

* `dev_mode`: Defines if the bot is in development mode or not.
  When in dev mode, errors that occur are not stored in the database with an error token.
  But their full trace-back is printed in the shell console where it is running.
  The value of the `dev_mode` key is a **boolean**.
* `status_rotation`: If true, Sigma's status will automatically rotate each 3 minutes.
  The list of statuses is hardcoded for now, but they're pretty fun.
  The value of the `status_rotation` key is a **boolean**.
* `text_only`: If `true`, Sigma will not load any commands inside the `Music` module group.
  If `false` nothing changes, and we recommend you keep it to `false`.
  The value of the `text_only` key is a **boolean**.
* `music_only`: If `true`, Sigma will not load any commands outside the `Music` module group.
  If `false` nothing changes, and we recommend you keep it to `false`.
  The value of the `music_only` key is a **boolean**.
* `prefix`: Specifies the default prefix for all of Sigma's commands.
  The default value is `>>`.
  The value of the `prefix` key is a **string**.
* `currency`: Since Sigma has an internal currency, this controls the  name of that currency.
  By default it's `Kud`, but you can set it to anything you want.
  The value of the `currency` key is a **string**.
* `currency_icon`: Controls the icon of the specified currency.
  While it can be an emoticon string like `:fleur_de_lis:`, to preserve compatibility, please use UTF-8 emoticon characters like `⚜`. Which is also the default for the icon.
  The value of the `currency_icon` key is a **string**.
* `website`: The URL leading to Sigma's website that contains all the commands and help for the bot. This is used in the help command.
  The value of the `website` key is a **string**.
* `movelog_channel`: The ID of the channel that should log movement messages.
  Whenever the bot is added to a server a message with basic information about the server is sent to that channel.
  The value of the `movelog_channel` key is an **integer**.
* `errorlog_channel`: The ID of the channel that should log errors.
  When a command breaks and fails to execute, information about what went wrong is, aside from being stored in the database, also sent to this channel (if specified).
  The value of the `errorlog_channel` key is an **integer**.
* `key_to_my_heart`: Sigma has an **encrypt** and **decrypt** command.
  Those commands use this key as the encryption/decryption key for
  the given data. You can make this as short or as long as you'd like.
  The value of the `website` key is a **string**.
