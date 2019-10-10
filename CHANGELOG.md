# Apex Sigma Changelog

## [Unreleased]

### Changed

- Fixed a `RuntimeError` in `enchantment.py`.

## 4.66.1323 Yuria

### Added

- The `heal` command has been added for the event. You can heal all your missing vigor, or a specified amount. You can also heal others.
- Event leaderboard commands, which are `>>topsweets` and `>>toppumpkin` have been added.
- The `grow` command was added that lets you grow your pumpkin. The more sweets you spend at once, the more it grows. The formula determining the gained weight is a positive exponential curve.
- Added the `steal` command that has consequences if you fail. It's used for stealing sweets. Failure means getting cursed, losing lots of vigor, and losing some Kud.
- A passive sweets adding mechanism has been added to messages. If the message and the guild meet criteria, a piece of candy will be given to the user. There's also a low chance for 6 to be added instead.
- The `enchant` command has been added with the ability to enchant a user. Enchanted users get higher amounts of candy during the event. Up to two users can enchant a user at a time and enchantments last for **2 hours**. Getting cursed wipes any active enchantments, so be careful.
- The curse mechanic was added. Atempting to do something bad during the event, such as stealing sweets, has a chance to get you cursed which has various negative effects such as reducing Vigor, which in turn has it's own negative effects.
- The `pumpkin` command and Weight resource for the spooktober event. The resource is in milligrams, the displayed value is in kilograms. This one also has fancy visuals!
- Added the FetchHelper class. It has it's own memory cacher to not spam the REST endpoint. Adds the ability to safely retrieve data about objects that are not in the general cache or obtainable from `get_<object>()` functions.
- Added detailed command statistics tracking for use in the upcoming profile rework. Such as your most used commands, arguments, most active guilds and channels, etc.
- The `trickortreat` command that gives you sweets if successfull. Includes chances for bonus candy.
- The `sweets` command and Sweets resource for the spooktober event (with fancy image generating!).
- The `vigor` command and Vigor resource for the spooktober event. Vigor affects your event cooldowns and chances.

### Changed

- The `daily` command now gives **+1 {Currency}** for each consecutive day.
- Replaced the `.replace()` directives in FFXIV Timers with `.shift()` due to deprecation of the former method causing errors.
- Overridden getter functions will use the FetchHelper to try to get invisible data.
- Added a catch-all exception for the dominant color processing handler.
- Fixed the interaction origin showing "Unknown User/Server" even when there is data where the interaction came from.
- Finding items of a **Spectral** or **Ethereal** rarity awards you sweets.

## 4.60.1201 Maka

### Changed

- You can now set a custom raffle icon with `>>raffleicon`. This needs to be an emote from the server you're starting the raffle from.
- Mentioning a channel in a `raffle` command will now start the raffle in that channel instead of the one where the command is executed in. Sigma will check if the user starting the raffle has the permission to Send Messages in that channel before starting said raffle.
- Fix global emote caching issues when using a redis or mixed cache. The cache will now be MemoryCached, forcibly, for this.
- The `spouses` command now sorts the users properly. This was only an issue when someone with database access started fucking with the data (me).
- The `spouses` command now displays a more accurate time since you got married to a user.
- The `divorce` command got a facelift. You are now presented with a dialogue and options on how to proceed with the divorce. You can ask for a mutual one which will have no cost or force the divorce costing you based on the time you spent married (and display the value). The final option is withdrawing the divorce proposal. Using the divorce command with an ID instead of a mention will not give you an option for a mutual divorce but will still display the dialogue and the cost of forcing the divorce.
- Slap now has a `smack` alias.
- Punch now has a `hit` alias.

## 4.57.1146 Taiga

### Added

- The `>>tackle` interaction is now a thing. Holding a dev hostage to make it is not ok...

### Changed

- Sleep now has a `nap` alias.
- Drink now has a `cheers` alias.

## 4.57.1145 Taiga

### Changed

- The formula used for scaling quiz-type minigames has been altered.
Because I got asked this earlier, taking trivia for reference, there is no maximum amount of Kud you can get from the minigame.
However, there is an effective one due to the nature of a reverse exponential formula.
The effective limits for trivia's **Easy/Medium/Hard/Average** would be **760/1520/3795/2025 Kud**, in that order.

## 4.57.1144 Taiga

### Changed

- Added a small `>>dictionary` safeguard for GRAMB type attribute errors.
- Added a small `>>jisho` safeguard for the field title value.
- The `concurrent.futures._base.CancelledError` exception will now be ignored since it happens when Sigma's forcefully stopped and has no valuable information.
- Fixed the `--global` argument for the `>>randomemote` command.
- Paginated the `>>queue` command. View past the first page with `>>queue <page>`.
- Simplified some functions in the `>>play` command file.
- Changed the audio codec in `music.py` to opus instead of mp3.
- Fixed a hardcoded word in the `>>dictionary` command.
- The chatter core responder has been given a hard capped response time of two minutes.
- The chatter core responder also got its message content cleaner fixed.
- Fixed an invalid keyword argument in `chatter_core_init.py`. See the arrow changelog.
- Added proper spacing between copyright text and imports that have also been formatted.
- Changed a few copyrights from being commented to multi line strings.

### Removed

- Not really removed... The Girls Frontline module has been disabled for now while a rework is pending.

## 4.56.1134 Taiga

### Changed

- The `>>dictionary` command has been repaired and reworked.
- The chatter core responder has been given a hard capped response time of two minutes.
- The chatter core responder also got its message content cleaner fixed.   

## 4.55.1112 Taiga

### Added

- The `>>givevirginity` command was added... I have no excuse other than "I was really bored".

### Changed

- Fixed `user_avatar` checking `user.avatar_url` instead of `user.avatar`.
- Swapped delimiter in `>>ratelimit` from `/` to `:` to match the description. 

## 4.55.1110 Taiga

### Changed

- Fixed some command description typos.
- Fixed an unawaited coroutine in `>>randomemote`.
- Fixed a caching issue in `>>emote`.
- Refactored a check in `>>emote` and `>>randomemote`.
- Int'd a potential float in `>>wfpricecheck`. 
- Added a message content check to `>>whisper` for use in DMs.
- Fixed command descriptions in the Whisper Settings module.

## 4.55.1104 Taiga

### Added

- The `>>hangman` command. It's hangman.
- The `>>whisper` command for sending anonymous messages to a dedicated server channel.
- The `>>whisperchannel` command for setting the aforementioned channel.
- Made the `get_broad_target(pld: CommandPayload)` function to get a target from a payload in a hierarchy order of `mention > id > name or nick`.

### Changed

- Disable pre-caching when using a redis-centric cache system.
- Recipe values are now calculated based on the items they're made from and a bit of math.
  If you need to know, the formula is
  ```py
  int(sum(ingredient_values) * (3 * (0.075 * sum(ingredient_rarities))) / 100) * 100
  ```
- Items now have hardcoded values per rarity (this was always the case, but they were in the item YAMLs).
- Tweaked some comments in `>>purge` to be more accurate.
- Cleaned up the changelog a bit. Slightly less spelling and grammatical mistakes.
- Changed the trigger checker function for auto reactors/responders to remove punctuation.
- Added a unique user safeguard to prevent one user from spamming the reaction.
- Added broad targeting to `ban`, `hardmute`, `hardunmute`, `kick`, `softban`, `voicekick` and `issuewarning`. Be careful with broad targeting when using names.
- Changed `>>starboardlimit` to show the current limit if one isn't specified.
- Changed `>>starboardchannel` to use the current channel if one isn't mentioned.
- Fixed an error in `starboard_watcher` resulting in disabling the starboard having no effect.
- Updated `>>randomcomicgenerator` to accommodate joining the three images returned by the web page. 
- Changed `>>wfnightwave` to not have hardcoded XP amounts, which caused errors.  

## Removed

- Removed unnecessary `usage` and `dmable`, fields in various `module.yml` files.
- Removed a duplicate of `clean_word`.

## 4.54.1095 Chito

### Changed

- The new `>>resetongoing` command will reset any "ongoing" locks that are placed on longer minigames to prevent duplicates. If a minigame gets stuck in an "ongoing" state you can clear it with this.
- All ongoing lists have been reworked to be resettable.
- Added a parameter to `>>commandstatistics` for viewing a specific command's use count.

## 4.54.1093 Chito

### Added

- An automatic leaderboard resetting clockwork has been added. It resets the leaderboards at midnight UTC.

### Changed

- Change `>>servericon` fallback type on no icon URL.
- Fix `>>serverinfo` to handle unrecognized/unenumerated regions.
- Added a safeguard for `>>queue` when editing lookup status messages.
- Added a safeguard for `>>bash` for the event where its cache depletes and it's not possible to refill it.
- The Reminder clock no longer uses a DM as a fallback but instead lets another shard take over the task for that reminder.
- Fix missing player creation voice client existence check.
- Add a JSON parsing safeguard for `>>ud` results.
- Fix deck generation for the `>>newdeck` command.
- Minor changelog heading fixes from the previous version.

## 4.54.1088 Chito

### Added

- Add a `>>finalffantasyxivtimers` command that shows Final Fantasy XIV timers cause Heide is a little bitch.
- Add `>>alacquisition` command that shows how you can get an Azur Lane ship.

### Changed

- Jisho URL format safeguard and a safeguard for the reading key for when it doesn't exist.
- Wolfram result display type check fixes and safeguards.
- The `>>lyrics` command got a fallback splitter in case the chunks are too big when split by newline.
- The YouTube command's like/dislike count has default values of 0 now to avoid a NoneType incompatibility.
- Added safeguards to profession commands and their dialogue generators.
- The music playing functions got a safeguard for voice client connections during playback and connection timeout safeguard when joining a channel.
- The donation link is now hardcoded to Patreon.
- Add Azur Lane stats processing safeguards for type mismatches and content checks.
- Add Azur Lane ship color safeguards and safeguards in case of Repair ships.

### Removed

- Remove checking the main License file's integrity to preserve docker container sanity and cross-platform byte reading compatibility. Holy fucking shit, fuck Windows.

## 4.52.1052: Chito

- Fixed some docstrings in the NSFW Core file.
- Refactored `>>wolframalpha` to use a more direct CSS query.

## 4.52.1050: Chito

### Changed

- Added a core GalleryClient class for some of the NSFW module. This acts as a universal handler for API calls to reduce redundant local functions.

## 4.52.1049: Chito

### Changed

- Fixed a possible encoding error in `integrity_check`.
- Fixed typos and inconsistent punctuation in `integrity_check`.
- Refactored the `>>convertcurrency` command to have match Sigma's command structure.

## 4.52.1048: Chito

### Added

- The `>>azurlaneskills` command shows the skill information of the given ship.
- The `>>showlicense` command shows the software's license information.
- The `>>repository` command shows the project's repository URL.
- An integrity check event has been added that checks the integrity of all license comments. Any missmatching of the license text is a violation of the GPLv3 that the project is distributed with and will shut down the software.

### Changed

- Altered command execution to handle ClientOSError instances.
- The redis cacher will now flush all data on boot.

## 4.50.1007: Chito

### Added

- Added the ability to specify the max number of cached messages in the main client. No less than 100 can be stored.
- The `>>azurlaneskins` has been added to list all the skins a ship has.
- The `>>azurlaneskin` has been added to show the given skin.

### Change

- Fix the `>>sniff` command saying "dances" instead of "sniffs".
- Fixed the `>>drawcard` command.
- Fixed `>>convertcurrency` by adapting it to v7 of the API.
- More role binding cache fixes.
- Made the `>>unscramblegame` command use the core cacher.
- Made the antispam checker event use the core cacher.
- Made the role binding mechanics use the core cacher.
- Made the `>>drawcard` command use the core cacher.
- Fix the collector clockwork breaking due to an invalid icon attribute parent.
- Add more detailed logging to most of the dbinit and boot events since they're a part of startup now.
- Changed the way startup events are started, they are now executed before the gateway connection starts.
- Bumped the Python version of the base image to 3.7 from 3.6, that's overdue.
- Moved static detail dicts to the core AzurLaneShip model and add a no-mobile cookie for their wiki.

### Removed

- Removed an unused cache dict from the `>>osu` command.
- The **Path of Exile** module has been completely **removed**. Nobody uses it, don't know why I thought anybody would...

## 4.48.966: Sakurako

### Changed

- Added the `colourme` alias to the `>>colorme` command.
- The `>>colorme` command now takes "surprised" as an argument that will give you a random color.
- Fixed the `>>shootfoot` command breaking due to an invalid dict default setting.
- Change the osu! command's caching.
- Change the Emote command's emote caching.
- The Unscramble Game no longer caches words, instead just runs a quick check of their validity.
- Yande.re command key getting refactor.
- Interaction core fixed for clients that don't use a cacher.
- Changed the XBooru cache to use the core cacher.
- Changed the PoE Passive Skill Gem command to use the core cacher.
- Changed the Rule34 cache to use the core cacher.
- NSFW caches made non-depletable.
- Various typo fixes.

### Removed

- Got rid of the "Development" section from the README. It used to have project badges in it, but since GL has a specific section and function for those this section is pointless.

## 4.48.960: Sakurako

### Changed

- The `>>alship` command now accepts `--retrofit` to show the ship's retrofit stats and also shows an average value of the ship's stats. You can also add `--awaken` to see the Lv. 120 stas instead of the base stats.
- A few fixes for Azur Lane statistics processing and wiki scraping.
- Gelbooru hopefully fixed, shit's weird...

## 4.47.943: Sakurako

### Added

- The **Azur Lane** module is born!
- The `>>almimic` command will generate a random markov chain impersonation using all Azur Lane quotes. Or a single ship, though due to being a tiny amount of data, they can be very repetitive.
- The `>>alship` command shows basic Azur Lane ship information and stats. More commands coming soon as I've made a complete scraper for the AL wiki within Sigma.

### Changed

- The `>>stats` command now shows for which shard it is showing stats.
- Error reporter tweaks and safeguards.
- Change all calls of the `discord.Guild.icon_url` to be compatible with the new `discord.Asset` class.
- Tweaked a few `discord.User.avatar_url` calls to make sure assets don't break those.
- The `dbinit` event will now start only on **Shard #0** if the client is sharded.
- Replaced the `discord.py` requirement from a hard repository URL to just the pypi name since rewrite is now the master branch and the repo branch is archived and broken.
- When booting the client will set a booting status message and clear it when it's done.
- Gelbooru uses the core cacher instead of a local dict variable.
- Interactions now use the core cacher instead of a local dict variable.
- Path of Exile Active Skill Gems now use the core cacher... you get the premise, more of these will come soon.
- Made the `get_channel()` and `get_user()` not try to cache their results if the caching method is `redis` or `mixed`.

## 4.45.902: Sakurako

### Added

- Docstrings, docstrings **EVERYWHERE**! Every single docstringable thing has been given a docstring.
- Common mostly static classes have been given `__slots__` attributes by *Valeth*.
- The permission logging lines now have a command blacklisting marker separate from the module one.

### Removed

- Removed parameter type hints.

### Changed

- The `>>konachan` command excepts a JSON parsing error now due to the CloudFlare issue.
- Docker build image fixes by *Valeth*.

## 4.41.827: Mirakurun

### Changed

- Renamed `get_` Discord HTTP functions to `fetch_` to coincide with a recent library update.

## 4.41.824: Mirakurun

### Changed

- `>>marry` now use a bool dialogue rather than a permanent proposal. You're either married or you're not.
- `>>divorce` and `>>spouses` have been refactored to reflect the marriage change.
- `bool_dialogue` now returns a `timeout` bool that says whether the dialogue was declined or timed out.
- `>>filtersell`, `>>sell` and `>>adopt` have been changed to use the previously mentioned `timeout` value.

## 4.41.821: Mirakurun

### Changed

- Switched which API for `>>wfnightwave` back due to the current one having placeholder descriptions.

## 4.41.820: Mirakurun

### Changed

- Fixed `KeyError` exceptions in `invasion_parser.py`.
- Switched which API `wfnews.py` and `news_parser.py` use to one that provides images.

## 4.40.818: Mirakurun

### Added

- Suppressions for "Exception too broad" warnings.
- The `WorldState` class was added for handling Waframe API calls.
- The `wforbvallis` command for checking the temperature on Orb Vallis in Warframe.
- The `wfdroptables` command which provides a link to Warframe's official drop tables.
- The `wfdailydeal` command for checking the current Daily Deal in Warframe.
- The `wffactionprogress` command for viewing faction progress for Invasions in Warframe.
- Appended the completion percentage to Waframe Invasions in `wfinvasions`.

### Changed

- All Warframe API calls have been changed to use the new `WorldState` class.
- Simplified the `remove_revision` function in `image_parser.py`.
- `version_check.py` now uses `yaml.safe_load` instead of the depreciated `yaml.load`.
- Fixed an incorrectly passed parameter in `generic.py`.
- The `wfsortie.py` file was renamed to `wfsorties.py`, along with its associated command.
- Fixed a `KeyError` exception in `wfvoidtrader`.
- Miscellanious refactors in most Warframe commands.

### Removed

- Warframe Alert commands and events.

## 4.40.810: Mirakurun

### Added

- More AIML properties for the Chatterbot.
- The `>>wfnightwave` command was added. Shows the current Nightwave challenges in Warframe.

### Removed

- The `wfsyndicates` command. API shutdown by host.

## 4.40.809: Mirakurun

### Changed

- Interactions will not try to fill missing user and guild data for usage in the footer text.
- The order of the `get_scaled()` arguments has been changed for more logic, it also takes the maximum multiplier cap as an argument.
- The profession emote reactions are back. Here's what happened with this. People were pissed about it being made, and when we reverted it, more people were pissed about it being gone. So "fuck you" to the little bitches that can't click an icon.
- Fix markov chain commands sometimes failing due to upstream `KeyError` instances that make no goddamn sense.
- Fix the `>>listinactivewarnings` command not working. Was using a non-existent method.

## 4.37.759: Ange

### Changed

- Chatterbot has been improved with better details, and missing details filled.
- Fixed reporter inconsistencies and errors.
- Sigma can now be told to interact with a user like `>>lick @Sigma @NotALoli`.

## 4.37.744: Ange

### Added

- The `get_scaled()` method was added to the Cooldown Controller to get a scaled up cooldown from a base value. The scaled time is slightly randomized and exponential with a passive cleaning method and cap.
- The `>>massban` command was added by *Shifty*. Bans all mentioned users.
- The `>>masskick` command was added by *Shifty*. Kicks all mentioned users.
- The `>>choosemany` command was added by *Shifty*. Chooses `n` items from a given, semicolon-separated, list.

### Changed

- Commands' antispam cooldown now uses the the scaling cooldown to additionally prevent abuse. 
- Professions now have special, partially randomized, scaling cooldowns.
- Misc and Utility modules have been moved and re-organized by *Shifty*.
- Profession rarity check exceptions have been replaced with proper ones by *Shifty*.
- Import lines cleaned and re-ordered by *Shifty*.
- The `>>disown` command's response when trying to disown someone who's not in your immediate family has been changed by *Shifty* to be clearer that you can only disown immediate family members.
- The `errors.py` core file was renamed to `error.py` by *Shifty*. Reason being that the file name should be consistently singular.

### Removed

- Profession emote interaction validation.

## 4.35.730: Ange

### Added

- The `>>roleswithpermission` (the `>>rlwperm` for short) command has been made. It lists all roles that have a given permission or list of permissions separated by a `; ` (semicolon). You can reverse the search so it shows that don't have the permission by adding `--negative` to the end of the command.

## 4.35.726: Ange

### Added

- Created the `CacherConfiguration` class that handles all `Cacher` classes. This adds a new core config file at `config/core/cache.yml` that should contain the cacher parameters. Those are: `type` for the type of `Cacher` to use, `size` for the max number of items in LRU and TTL caches, `time` for the time-to-live time limit in the TTL cache, and `host` and `port` for the Redis and Mixed cachers.

### Changed

- The `>>adopt` command now requires emote reaction confirmation that they agree to being adopted.
- The `>>familytree` command now uploads a yaml file instead of posting the contents to hastebin due to hastebin's low storage allowance.
- `Cacher` classes now take a `CacheConfiguration` value, instead of specific required values.
- The default value for the bot token has been removed and replaced with a safeguard check. Sigma now terminates without trying to contact discord if the token is `None`.

## 4.35.712: Ange

### Added

- Created the `ModuleConfig` class that wraps command config data for future configuration expansions.
- The initial `run.py` file now checks for any import errors. If detected, it'll try to install the requirements file.
- The ChatterBot Core returns! Brought back AI without ChatterBot, now with AIML... it's good enough.

### Changed

- Codename changed to **Ange** for **4.35**.
- The `SigmaEvent` class now has a `path` attribute and `resource()` method like the one for commands.
- Updated all copyright comments from 2018 to 2019.
- All instances of `plugin` have been renamed to `module`. Meaning that you need to rename `config/plugins` to `config/modules`.
- Family tree consistency fixes by *Shifty*.

## 2019-02-12

### Changed

- Major family module fixes. Added sibling checks and make recursion issues less likely.
- Fixed the `>>colorme` hex color safeguard check.
- Fixed the `>>adopt` response not being assigned to the response variable when targeting bots.

## 2019-02-10

### Changed

- Renamed `>>packages` to `>>pythonpackage`, packages is too broad and has no correlation with what the command does.

## 2019-02-09

### Changed

- No longer able to `>>adopt` bots.
- Clean the `.name` attribute of `AdoptableHuman` because fuck special characters.
- Have the `.name` attribute of `AdoptableHuman` update when they're interacted with.

## 2019-02-08

### Added

- The family tree functions have been added. You can `>>adopt` people, if you don't like them you can `>>disown` them. If you want to see your entire family tree from start to end use `>>familytree` and it will generate a nice little link with your entire tree in it. A thing to note that is that this mimics an actual biological family tree, meaning that you can't have more than 2 parents, cause biology.

### Changed

- Renamed all instances of the method `dictify()` to `to_dict()`. It's more uniform and logical.

## 2019-02-07

### Added

- The `>>sniff` interaction has been added. I have no official reason behind this besides liking the idea of lewd sniffs. Just being honest...

## 2019-02-05

### Added

- The `>>visualnoveldatabase` (I know it's long, use `>>vndb` or `>>vn` instead) command was revived. Now with 100% less locks and 100% more async. It looks up visual novels, obviously.

## 2019-02-04

### Changed

- Fixed the `>>spelledlike` command. That issue was there for a long time but nobody really uses this command...
- The `>>shadowpollvote` command will now try to delete the vote command message.

## 2019-02-02

### Changed

- Hard mute ongoing message deletion safeguard. By *Shifty*.
- Music playing notification edit safeguard. By *Shifty*.
- Replace aiohttp exceptions to reduce imports. By *Shifty*.

### Removed

- Disabled `>>yomomma` while a replacement endpoint is found. By *Shifty*.

## 2019-01-25

## 2019-01-24

### Added

- Selling your entire inventory or selling items with a filter will trigger a confirmation dialogue for the user to confirm their sale.
- The bool dialogue generator now takes a `tracked: bool` argument that records how long the user took to respond.

### Changed

- The interaction addition is now a whitelist mechanic. Instead of being able to remove submitted interactions with an `❌` emote reaction to the log message, you now approve it instead with a `✅`. Unless approved, the interaction will not be used. Sigma will then add a `🆗` reaction of her own if successfully approved.

## 2019-01-22

### Changed

- Server renamed to Support in the `>>help` command and make the command link lead to the website once again.
- Fix the invite URL in the `CONTRIBUTING.md` document and remove the nonexistent setup link.
- Suggestion approval and declining commands return an `ok` response if the user was not found or if the notification was undelivered, specifying the lookup or delivery failure.
- Shortened the `status_clockwork(ev: SigmaEvent)` lines for caching the status files.
- Placed `.get()` methods in `afk_mention_check.py` to combat possible (but unlikely) `KeyError` instances.
- Refactored `module.yml` files automatically for visual alignment and clarity.
- The `>>youtube` command was repaired by *Shifty*.

## 2019-01-19

### Changed

- Remove logger creation from the `ExecutionClockwork` class as it was unused.
- The logger files contain shard numbers in them in the format of `sigma.{shard}.{date}.log`.
- The way the `>>play` command executes the `>>summon`, `>>queue` and `>>donate` commands are executed now use their raw methods instead of the `.execute(pld: CommandPayload)` method of the `SigmaCommand` class.
- Generic responses implementation by *Shifty*, second pass.

## 2019-01-18

### Changed

- Generic responses implementation by *Shifty*, first pass.
- Fixed extension blocked incompatibility with the Payload system by *Shifty*.

## 2019-01-10

### Added

- The `>>crates` command for searching crates.io Cargo/Rust packages.

### Changed

- Fix CHANGELOG.md dates and alter styling. Poor me was still stuck in 2018.

## 2019-01-09

### Added

- Generic core utility for making async HTTP requests created with the `aioget(url: str, as_json: bool)` coroutine.
- Add the `error(content: str)` generic response method.

### Changed

- Blockers/filters now check for the `administrator` permission in `guild_permissions` instead of `permissions_in(channel)`.
- Change invite blocking functions default value for the `invite_found` variable from a `bool` to a `None`.
- Remove the `>>prefix` command minimum length limit of 2 characters.
- Fix the `>>donate` command's missing (incorrect) argument.

## 2019-01-08

### Changed

- Disable caching of blacklist items. Those are user, server, module and command blacklist entries.
