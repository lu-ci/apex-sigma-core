# Plugin Configuration Files

All plugin configuration files are `.yml` files that need to be made manually.
They need to be made in the `config/plugins/` folder.
Plugin configuration files need to be named after the main command name of
their respective commands.
For example, if you are making a configuration file for the `>>slots` command,
the configuration file needs to be named `slots.yml`. They can not use command
alternate names/aliases.

## Interaction Adding

The interaction addition configuration tells the bot where to send a message notifying the authors that a new interaction has been submitted.
This can be used as a safety protocol against malicious submissions and a quick way to remove bad submissions.
If a bot owner reacts to one of these interaction log messages with an **❌** emote the bot will remove it and react with **🔥** if it deletes it, that is, if the submission is found in the database and deleted.
**Note: This requires the `imgur` command to be set up.**

**Example of log message**:

> ![Interaction Log Example](https://i.imgur.com/GGc9F4s.png)

**Configuration file contents**:

```yml
log_ch: 01234567890123456789
```

The `log_ch` key value needs to be an **Integer**.

> The file for storing this configuration is `addinteraction.yml`.
You can obtain a channel's ID by using the `>>cid` command in that channel,
or by targeting a channel with the same command.
Or by activating Developer Mode in Discord's Appearance settings,
right clicking the channel of your choice, and clicking Copy ID,
the ID will be copied to your clipboard.

## Bot Development Suggestions

This function serves to have a global centralized suggestion channel
where users can submit suggest changes they want made to the bot.
Usually development and feature wise.
When someone uses the `>>botsuggest` command their suggestion is sent
to the bot suggestion channel, given a suggestion ID and stored in the
database, as well as automatically given an Arrow Up and Arrow Down
emote reaction so users can vote on the suggestion.
This ID, shown in the bottom left of the suggestion message, can be
used with the `>>declinesuggestion` and `>>approvesuggestion` commands
which allow fast responses to suggestions.

**Example of suggestion message**:

> ![Suggestion Message Example](https://i.imgur.com/5UdGnZw.png)

**Configuration file contents**:

```yml
channel: 01234567890123456789
```

The `channel` key value needs to be an **Integer**.

> The file for storing this configuration is `botsuggest.yml`.
You can obtain a channel's ID by using the `>>cid` command in that channel,
or by targeting a channel with the same command.
Or by activating Developer Mode in Discord's Appearance settings,
right clicking the channel of your choice, and clicking Copy ID,
the ID will be copied to your clipboard.

## Suggestion Approval

This command automates a lot of stuff for developers when it comes
to approving suggestions and adding them to a TODO list.
Well, GitLab honestly since that's what Lucia's Cipher uses.
When the `>>approvesuggestion` command is used with a suggestion ID
the suggestion message in the suggestion channel is marked with a
check mark and if GitLab repository information is in the config
it is also added as a new issue with a **Suggestion** tag.

**Example of suggestion issue**:

![Suggestion Issie Example](https://i.imgur.com/8gVeBOf.png)

**Configuration file contents**:

```yml
token: 'gitlab_personal_access_token'
project: 123456789
```

The `token` key value needs to be a **String**,
the `project` key value needs to be a **String** or an **Integer**.

> The file for storing this configuration is `approvesuggestion.yml`.
The `token` which is a Personal Access Token can be obtained from
your settings [here](https://gitlab.com/profile/personal_access_tokens).
I'm not sure which scopes are required so I enable all of them.
Just remember to never give that token to anyone no matter what.
The `project` is the ID of the GitLab project. It can be found on your project page under the project's description, where it says:
`Project ID: XXXXXXX`. The `XXXXXXX` is what you want here.

## Cat Command

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

## Dictionary

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

## Food Recipe

Unfortunately a tool for finding recipes was actually really hard to find.
Or rather, a good and reliable, but free and open one, to be precise.
Sigma uses the Food2Fork API to search for recipes, and requires their API key.

**Configuration file contents**:

```yml
api_key: 'my_f2f_api_key_here'
```

The `api_key` key value is a **String**.

> The file for storing this configuration is `foodrecipe.yml`.
You can obtain an API key from their API page
[here](http://food2fork.com/about/api).

## URL Shortening

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

## Urban Dictionary

This command uses the Urban Dictionary API that needs to be consumed on RapidAPI.
RapidAPI is basically a market of various APIs, and the UD API is one of them.
It's required for UD command to function.

**Configuration file contents**:

```yml
api_key: 'your_rapidapi_key'
```

The `api_key` key value is a **String**.

> The file for storing this configuration is `urbandictionary.yml`.
The urban dictionary API can be seen and consumed
[here](https://rapidapi.com/community/api/urban-dictionary).

## Weather

To use the `>>weather` command you need a Dark Sky API secret key.

**Configuration file contents**:

```yml
secret_key: 'your_ds_secret_key'
```

The `secret_key` key value is a **String**.

> The file for storing this configuration is `weather.yml`.
You can get the secret key at the developer page
[here](https://darksky.net/dev/account).

## Wolfram Alpha

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
