# Apex Sigma Changelog

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
- The proffession emote reactions are back. Here's what happened with this. People were pissed about it being made, and when we reverted it, more people were pissed about it being gone. So "fuck you" to the little bitches that can't click an icon.
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

- The `>>roleswithpermission` (the `>>rlwperm` for short) command has been made. It lists all roles that have a given permission or list of permissions  separated by a `;` (semicolon). You can reverse the search so it shows that don't have the permission by adding `--negative` to the end of the command.

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

- Renamed `>>packages` to `>>pythonpackage`, packages is too broad and has no corelation with what the command does.

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

- Hardmute ongoing message deletion safeguard. By *Shifty*.
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
- Fixed extention blocked incompatibility with the Payload system by *Shifty*.

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
