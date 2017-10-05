# About Plugin Configuration Files

All plugin configuration files are `.yml` files that need to be made manually.
They need to be made in the `config/plugins/` folder.
Plugin configuration files need to be named after the main command name of
their respective commands.
For example, if you are making a configuration file for the `>>slots` command,
the configuration file needs to be named `slots.yml`. They can not use command
alternate names/aliases.

# Reaction Addition Logging

The configuration file of the `>>addreact` command is used to specify the logging channel for the command.
Whenever a new reaction is added, information about it is sent to that channel.

**Example of log message**:

> ![AddReact Log Example](https://i.imgur.com/ik4GkJ9.png)

**Configuration file contents**:
```yml
log_ch: 01234567890123456789
```

The `log_ch` key value needs to be an **Integer**.

> The file for storing this configuration is `addreact.yml`.
You can obtain a channel's ID by using the `>>cid` command in that channel,
or by targeting a channel with the same command.
Or by activating Developer Mode in Discord's Appearance settings,
right clicking the channel of your choice, and clicking Copy ID,
they ID will be copied to your clipboard.

# Cat Command

The `>>cat` command pulls images of cats from an external API.
This API has a usage limit when used without an API key.
The configuration for this command, as well as the API key is **NOT REQUIRED** for the command to work.
But is highly recommended to have.

**Configuration file contents**:
```yml
api_key: 'cat_api_key'
```

The `api_key` key value needs to be a **String**.

> The file for storing this configuration is `cat.yml`.
You can obtain an API key for the Cat API at their documentation page [here](http://thecatapi.com/docs.html).

# Dictionary

This is the configuration file for the `>>dictionary` command.
The function for the dictionary command uses the Oxford dictionary API,
and requires a key to use their features.

**Configuration file contents**:
```yml
app_id: 'your_app_id'
app_key: 'your_app_api_key'
```

Both the `app_id` and `app_key` keys need to be **Strings**.

> The file for storing this configuration is `dictionary.yml`.
You can obtain the application credentials from Oxford's developer page
[here](https://developer.oxforddictionaries.com/).

# Rare Fish Logging Channel

Item collection commands such as `>>fish` and `>>forage` have the feature to log
finding an item of Rarity 5 (Prime) or higher to a specific channel. Meant to be
used as a type of a hall of fame of people who got luck and found a rare item.

**Example of log message**:

![Rare Fish Found Example](https://i.imgur.com/pr9GnPR.png)

**Configuration file contents**:
```yml
item_channel: 01234567890123456789
```

The `item_channel` key value is an **Integer**.

> The file that stores this configuration is `fish.yml`.
You can obtain a channel's ID by using the `>>cid` command in that channel,
or by targeting a channel with the same command.
Or by activating Developer Mode in Discord's Appearance settings,
right clicking the channel of your choice, and clicking Copy ID,
they ID will be copied to your clipboard.

# Rare Plant Logging Channel

Item collection commands such as `>>fish` and `>>forage` have the feature to log
finding an item of Rarity 5 (Prime) or higher to a specific channel. Meant to be
used as a type of a hall of fame of people who got luck and found a rare item.

**Example of log message**:

![Rare Fish Found Example](https://i.imgur.com/rywvZ6p.png)

**Configuration file contents**:
```yml
item_channel: 01234567890123456789
```

The `item_channel` key value is an **Integer**.

> The file that stores this configuration is `forage.yml`.
You can obtain a channel's ID by using the `>>cid` command in that channel,
or by targeting a channel with the same command.
Or by activating Developer Mode in Discord's Appearance settings,
right clicking the channel of your choice, and clicking Copy ID,
they ID will be copied to your clipboard.

# Recipe

Unfortunately a tool for finding recipes was actually really hard to find.
Or rather, a good and reliable, but free and open one, to be precise.
Sigma uses the Food2Fork API to search for recipes, and requires their API key.

**Configuration file contents**:
```yml
api_key: 'my_f2f_api_key_here'
```

The `api_key` key value is a **String**.

> The file for storing this configuration is `recipe.yml`.
You can obtain an API key from their API page
[here](http://food2fork.com/about/api).

# Reddit

Sigma uses PRAW for Reddit access, being the official Reddit wrapper for python.
To use any Reddit features, an official application is required, and it's credentials.

**Configuration file contents**:
```yml
client_id: "app_client_id"
client_secret: "app_client_secret"
```

Both the `client_id` and `client_secret` keys need to be **Strings**.

> The file for storing this configuration is `reddit.yml`.
You can create an application and obtain it's credentials on the application
preferences page [here](https://www.reddit.com/prefs/apps/).

# URL Shortening

For the `>>shortenurl` command, the Bit.ly API is used. By default and hardcoded,
all links generated are ad-less simple redirect URLs. To use this function a API
key is required.

**Configuration file contents**:
```yml
access_token: 'my_access_token'
```

The `access_token` key value is a **String**.

> The file for storing this configuration is `shortenurl.yml`.
The access token can be obtained from their official dev page
[here](http://dev.bitly.com/).
You can generate a *Generic Access Token* once there.

# Slots Victory Logging

Similar to the logging of rare items, you can set Sigma up to log when someone
gets a combination of 3 symbols to a channel of your choice.

**Example of log message**:

![Slot Win Example Image](https://i.imgur.com/JPOUlUu.png)

**Configuration file contents**:
```yml
win_channel: 01234567890123456798
```

The `win_channel` key value is an **Integer**.

> The file that stores this configuration is `slots.yml`.
You can obtain a channel's ID by using the `>>cid` command in that channel,
or by targeting a channel with the same command.
Or by activating Developer Mode in Discord's Appearance settings,
right clicking the channel of your choice, and clicking Copy ID,
they ID will be copied to your clipboard.

# Urban Dictionary

This command uses the Urban Dictionary API that needs to be consumed on Mashape.
Mashape is basically a market of various APIs, and the UD API is one of them.
It's required for UD command to function.

**Configuration file contents**:
```yml
api_key: 'your_mashape_key'
```

The `api_key` key value is a **String**.

> The file for storing this configuration is `urbandictionary.yml`.
The urban dictionary API can be seen and consumed
[here](https://market.mashape.com/community/urban-dictionary).

# Weather

To use the `>>weather` command you need a Dark Sky API secret key.

**Configuration file contents**:
```yml
secret_key: 'your_ds_secret_key'
```

The `secret_key` key value is a **String**.

> The file for storing this configuration is `weather.yml`.
You can get the secret key at the developer page
[here](https://darksky.net/dev/account).

# Wolfram Alpha

Wolfram Alpha is one of the most amazing mathematics and statistics engines.
Capable of processing extreme operations and finding various data.
Way beyond any of our capabilities, so we mooch off of them a bit, and use their API.
To use the `>>wa` command, you need their API key.

**Configuration file contents**:
```yml
app_id: 'your_app_id'
```

The `app_id` key value is a **String**.

> The file for storing this configuration is `wolframalpha.yml`.
You can get the application ID at their API product page
[here](https://products.wolframalpha.com/api/).

# World of Warships

To use `>>wows` and get World of Warships statistics about a player's profile,
we use the Wargaming official API.

**Configuration file contents**:
```yml
app_id: 'your_app_id'
```

The `app_id` key value is a **String**.

> The file for storing this configuration is `worldofwarships.yml`.
You can get the application ID at their developer page
[here](https://developers.wargaming.net/).
