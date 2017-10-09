**Hey there!** We need your **help**! Come support us on [**Patreon**](https://www.patreon.com/ApexSigma)!

## Command Index
- [ADMINISTRATION](#administration)
- [FUN](#fun)
- [GAMES](#games)
- [HELP](#help)
- [INTERACTIONS](#interactions)
- [MATHEMATICS](#mathematics)
- [MINIGAMES](#minigames)
- [MISCELANOUS](#miscelanous)
- [MODERATION](#moderation)
- [MUSIC](#music)
- [NIHONGO](#nihongo)
- [NSFW](#nsfw)
- [PERMISSIONS](#permissions)
- [ROLES](#roles)
- [SEARCHES](#searches)
- [SETTINGS](#settings)
- [STATISTICS](#statistics)
- [UTILITY](#utility)

### ADMINISTRATION
Commands | Description | Example
----------|-------------|--------
`>>announce` | Announces a message to every server that Sigma is connected to. Servers can opt out of this with the noannouncements command. (Bot Owner Only) | `>>announce Hello world!`
`>>blacklistserver` `>>blacklistguild` `>>blacksrv` `>>blackguild` | Marks a server as blacklisted. This disallows any user on that server from using commands. (Bot Owner Only) | `>>blacklistserver 0123456789`
`>>blacklistuser` `>>blackusr` | Marks a user as blacklisted disallowing them to use any command. (Bot Owner Only) | `>>blacklistuser 0123456789`
`>>eject` | Makes Sigma leave a Discord server. (Bot Owner Only) | `>>eject 0123456789`
`>>evaluate` `>>evaluate` `>>eval` `>>py` `>>python` `>>code` `>>exec` | Executes raw python code. This should be used with caution. (Bot Owner Only) | `>>evaluate print('hello world')`
`>>geterror` | Gets an error's details using the given token. (Bot Owner Only) | `>>geterror 9a2e9a374ac90294f225782f362e2ab1`
`>>givecurrency` `>>givekud` `>>givemoney` | Awards the mentioned user with the inputted amount of currency. The currency goes first and then the user mention as shown in the example. (Bot Owner Only) | `>>givecurrency 150 @person`
`>>giveitem` | Awards the mentioned user with the inputted amount of currency. The currency goes first and then the user mention as shown in the example. (Bot Owner Only) | `>>giveitem @person plants Blue Delta`
`>>reload` | Reloads all of the module in Sigma. This includes both commands and events. (Bot Owner Only) | `>>reload`
`>>send` | Sends a message to a user, channel or server. The first argument needs to be the destination parameter. The destination parameter consists of the destination type and ID. The types are U for User and C for Channel. The type and ID are separated by a colon, or two dots put more simply. (Bot Owner Only) | `>>send u:0123456789 We are watching...`
`>>setavatar` | Sets the avatar of the bot either to the linked image or attached image. The officially supported formats for bot avatars are JPG and PNG images. Note that bots, like all users, have limited profile changes per time period. (Bot Owner Only) | `>>setavatar https://my_fomain.net/my_avatar.png`
`>>setstatus` | Sets the current playing status of the bot. To use this, the automatic status rotation needs to be disabled. It can be toggled with the togglestatus command. (Bot Owner Only) | `>>setstatus with fishies`
`>>setusername` | Sets the name of the bot to the inputted text. Note that bots, like all users, have limited profile changes per time period. (Bot Owner Only) | `>>setusername Supreme Bot`
`>>shutdown` | Forces the bot to disconnect from Discord and shut down all processes. (Bot Owner Only) | `>>shutdown`
`>>sysexec` `>>sh` | Executes a shell command. Extreme warnings. (Bot Owner Only) | `>>sysexec echo 'Hello'`
`>>takecurrency` `>>takekud` `>>takemoney` | Takes away the inputted amount of corrency from the mentioned user. The currency goes first and then the user mention as shown in the example. (Bot Owner Only) | `>>takecurrency 150 @person`
`>>takeitem` | Takes away the inputted amount of corrency from the mentioned user. The currency goes first and then the user mention as shown in the example. (Bot Owner Only) | `>>takeitem abcdef1234567890`
`>>test` `>>t` | For testing purposes, obviously. Used as a placeholder for testing functions. (Bot Owner Only) | `>>test`
`>>togglestatus` | Toggles if the automatic status rotation is enabled or disabled. (Bot Owner Only) | `>>togglestatus`
[Back To Top](#index)

### FUN
Commands | Description | Example
----------|-------------|--------
`>>bash` | If you are old enough to know what IRC is or remember how it looked like, then you will appreciate the quotes that the bash command produces. | `>>bash`
`>>cat` | Outputs a random cat image. Furry felines like it when their owners observe them. | `>>cat`
`>>catfact` | Outputs a random fact about your lovely furry assh~ Eerrrr... I mean, companion! | `>>catfact`
`>>chucknorris` | This command outputs a random Chuck Norris joke. We use Chuck jokes because Bruce Lee is no joke, obviously. | `>>chucknorris`
`>>cookies` | Shows how many cookies you have, or how many a mentioned user has. | `>>cookies @person`
`>>csshumor` | The only thing better than a joke is a joke written in CSS. And while that is sarcasm to a certain degree, these really are fun. Embrace your web designer within and read some CSS jokes. | `>>csshumor`
`>>cyanideandhappiness` `>>cnh` | Outputs an image of a random Cyanide and Happiness comic. Explosm makes awesome comics and animations. | `>>cyanideandhappiness`
`>>dab` | Pseudo-dank metrics or whatever. | `>>dab`
`>>dadjoke` | This will provide a joke that might be something your father would say. You know they are bad, but you will love them anyway, cause you are a good kid. | `>>dadjoke`
`>>dog` | Outputs a random dog image. Cutest, loyalest little woofers. | `>>dog`
`>>dogfact` `>>doggofact` | Outputs a random fact about the man's best friend. | `>>dogfact`
`>>fortune` `>>fortune-mod` | Linux users, and raw UNIX users in general will know the fortune-mod. This command uses their entire database to output one of their quotes. | `>>fortune`
`>>givecookie` | Gives a cookie to a person. Remember to give them to only nice people. You can give only one cookie every hour. | `>>givecookie @person`
`>>joke` | Outputs a pretty much regular joke. It is not really special or anything... Sometimes they are funny, most of the times they are not. | `>>joke`
`>>kitsunemimi` `>>kon` `>>fluffytail` | Displays a random kitsunemimi image. In case you don't know what a kitsunemimi is, it's a foxgirl. All images are sourced from Safebooru, but due to some being borderline. The command rating is naturally set to "Borderline". | `>>kitsunemimi`
`>>leetspeak` `>>leet` `>>l33t` | Turns your inputted statement into l33t text. You can add which level of leet you want your text to be converted to. As it's displayed in the usage example. The accepted levels are basic, advanced and ultimate. | `>>leetspeak owned level:ultimate`
`>>nekomimi` `>>neko` `>>nyaa` | Displays a random nekomimi image. In case you don't know what a nekomimi is, it's a catgirl. All images are sourced from Safebooru, but due to some being borderline. The command rating is naturally set to "Borderline". | `>>nekomimi`
`>>pun` | If you do not know what a pun is... Oh you poor innocent soul. This command will produce a lovely little pun for you. Enjoy the cringe! | `>>pun`
`>>quote` | Gives you a random inspirational or deep quote. | `>>quote`
`>>randomcomicgenerator` `>>rcg` | Uses the Cyanide and Happiness random comic generator for buttloads of fun. Personally the favorite comic command. | `>>randomcomicgenerator`
`>>reversetext` `>>reverse` | Reverses the text that you input into the command. | `>>reversetext hello`
`>>ronswanson` | Everyone's favorite character from Parks and Recreation. This command will output a random quote from Ron Swanson. | `>>ronswanson`
`>>visualnovelquote` `>>vnquote` `>>vnq` | Outputs a random quote from a random VN. Displays it's source as well, of course. | `>>visualnovelquote`
`>>xkcd` | If you like humerous things and know a bit of technology, you will lose a lot of time reading these. XKCD comics are perfect for procrastination and time wasting. | `>>xkcd`
`>>yomomma` `>>yomama` `>>yomoma` | Want to insult some poor fool's mother but don't have the right comeback? This command will provide the perfect yo momma joke for the task. | `>>yomomma`
[Back To Top](#index)

### GAMES
Commands | Description | Example
----------|-------------|--------
`>>bhranking` `>>bhlb` `>>brawlhallaleaderboad` `>>brawlhallaranking` | Grabs the current top players on the Brawlhalla leaderboards. You can append a region to the command to get the leaderboard for that region. If no region is specified, it will use the global ranking page. | `>>bhranking EU`
`>>osu` | Generates a signature image with the users stats for osu. | `>>osu AXAz0r`
`>>pokemon` `>>pkmn` | Shows details for the inputted Pokemon as well as a cute little GIF of them. | `>>pokemon Snorlax`
`>>wfalertchannel` `>>wfac` | Designates a channel for Warframe alerts. When a new alert shows up the news will be posted here. To disable this, write disable after the command instead of a channel. | `>>wfalertchannel #wf-alerts`
`>>wfalerts` `>>wfa` | Shows the currently ongoing alerts in Warframe. As well as their respective rewards. | `>>wfalerts`
`>>wffissurechannel` `>>wffc` | Designates a channel for Warframe void fissures. When a new void fissure shows up the news will be posted here. To disable this, write disable after the command instead of a channel. | `>>wffissurechannel #wf-fissures`
`>>wffissures` `>>wffissure` `>>wff` | Shows the current fissure locations in Warframe. As well as their tiers, locations and mission types. | `>>wffissures`
`>>wfloc` `>>wfdrop` `>>wfprime` | Searches for, and outputs, a prime's drop location. Relics that are vaulted will be marked with an asterisk. | `>>wfloc Fragor Prime`
`>>wfpricecheck` `>>wfpc` `>>wfmarket` | Checks the price for the searched item. This will only list items by members that are currently online and in the game. | `>>wfpricecheck Blind Rage`
`>>wfsortie` `>>wfsorties` `>>wfs` | Shows the ongoing sortie missions in Warframe. | `>>wfsortie`
`>>wfsortiechannel` `>>wfsc` | Designates a channel for Warframe sorties. When a new sortie shows up the news will be posted here. To disable this, write disable after the command instead of a channel. | `>>wfsortiechannel #wf-sorties`
`>>wftag` `>>wftagrole` `>>wfnotify` `>>wfbind` | Binds a certain keyword from alerts and invasions. When this keyword appears during an event all roles bound to it's triggers will be mentioned. | `>>wftag aura Aura Squad`
`>>wftrials` `>>wftrial` `>>wfraids` `>>wfraid` `>>wft` `>>wfr` | Shows raid statistics for the inputted username. Note that DE hasn't been tracking this data forever. So some really old raids won't be shown due to having no data. The shortest raid time shown only counts victorious raids. | `>>wftrials AXAz0r`
`>>worldofwarships` `>>wows` | Grabs the player statistics for the game World of Warships. First the region and then the username. | `>>worldofwarships EU AXAz0r`
[Back To Top](#index)

### HELP
Commands | Description | Example
----------|-------------|--------
`>>commands` | Shows the commands in a module group category. To view all the module group categories, use the modules command. | `>>commands minigames`
`>>help` | Provides the link to Sigma's website and support server. As well as show information about a command if something in inputted. | `>>help fish`
`>>modules` | Shows all the module categories. | `>>modules`
[Back To Top](#index)

### INTERACTIONS
Commands | Description | Example
----------|-------------|--------
`>>addreact` | Adds new reactions. | `>>addreact reaction my.gif.link/fancy.gif`
`>>bite` | Sink your teeth into some poor thing. | `>>bite @person`
`>>cry` | Somebody is making you sad, let them know that with crocodile tears! | `>>cry @person`
`>>cuddle` | Snuggle, snuggle~ | `>>cuddle @person`
`>>dance` | Feel alive? Like you just wanna... boogie? Let's dance! | `>>dance @person`
`>>drink` | Cheers, family! Let's get drunk! | `>>drink @person`
`>>explode` `>>detonate` | When all other means fail, it's time to bring out the carpet bomb squadrons. | `>>explode @person`
`>>facepalm` | Somebody just did something so stupid you want to facepalm. | `>>facepalm @person`
`>>fap` | When you can't get that good-good, you gotta fap to them ԅ(¯﹃¯ԅ) | `>>fap @person`
`>>feed` | Care to share some of your food with someone cute? | `>>feed @person`
`>>fuck` | Don't question my modules... Yes (º﹃º) | `>>fuck @person`
`>>fuckrl` | The same as fuck, but for non-weebs, the RL stuff... STOP JUDGING ME (ﾟ￢ﾟ) | `>>fuckrl @person`
`>>hug` | Even a bot like me can appreciate a hug! The person you mention will surely as well. | `>>hug @person`
`>>kiss` | Humans touching their slimy air vents. How disturbing. | `>>kiss @person`
`>>lick` | Doesn't someone sometimes look so cute that you just want to lick them? Or maybe they have some food on their face, it's a good excuse. | `>>lick @person`
`>>lovecalculator` `>>lovecalc` | Shows the love between two things. Which can be either two users or a user and a thingamabob. Just make sure if you want to see how much @Calum loves Kud you put the user in the first place. | `>>lovecalculator @person1 @person2`
`>>pat` | Pat, pat~ Good human, lovely human. I will kill you last. | `>>pat @person`
`>>peck` | A hit and run style quickie kiss. | `>>peck @person`
`>>poke` | Poke, poke~ Are you alive? | `>>poke @person`
`>>pout` | Make a pouty face at someone and make them change their mind. Or just teast them for being a horrible person. Like when they make you create a pout command for money! | `>>pout @person`
`>>punch` | You have something on your face. IT WAS PAIN! | `>>punch @person`
`>>shoot` | When a damn knife isn't enough. | `>>shoot @person`
`>>shrug` | I don't get it, or I don't care, really whatever *shrug*. | `>>shrug @person`
`>>sip` | Ahh yes, i know the feeling of wanting to sit outside on a chilly morning sipping hot tea. | `>>sip @person`
`>>slap` | When a punch is too barbaric a slap should be just elegant enough. | `>>slap @person`
`>>stab` | Boy... Somebody really has you pissed off if you are using this one. | `>>stab @person`
`>>stare` | Jiiiiiiiiiii~ | `>>stare @person`
[Back To Top](#index)

### MATHEMATICS
Commands | Description | Example
----------|-------------|--------
`>>analyze` `>>sentiment` | Sentimental analysis of the given text. | `>>analyze Fill my mouth with spaghetti, senpai!`
`>>collectchain` | Collects messages sent by the mentioned user and saves it as a chain. Only one person can use the command at the time due to the processing load it takes. | `>>collectchain @person`
`>>impersonate` `>>mimic` | Tries to impersonate the mentioned user if a chain file for them exists. | `>>impersonate @person`
`>>makehash` `>>hash` | Creates a hash using the inputed has type. These are all the hash types you can use. sha512, sha3_224, sha3_512, MD4, dsaWithSHA, ripemd160, RIPEMD160, SHA, ecdsa-with-SHA1, sha3_384, SHA512, sha1, SHA224, md4, DSA-SHA, SHA384, blake2b, dsaEncryption, SHA256, sha384, sha, DSA, shake_128, sha224, SHA1, shake_256, sha256, MD5, blake2s, md5, sha3_256, whirlpool | `>>makehash md5 Nabzie is best tree.`
`>>timeconvert` `>>tconv` | Converts the given time in the given time zone to the inputted time zone. | `>>timeconvert 18:57 UTC>PST`
`>>wipechain` | It wipes your entire Markov chain, if you have one. | `>>wipechain`
`>>wolframalpha` `>>wa` | Makes a request for Wolfram Alpha to process. This can be a lot of things, most popular being complex math operation. | `>>wolframalpha 69+42`
[Back To Top](#index)

### MINIGAMES
Commands | Description | Example
----------|-------------|--------
`>>animechargame` `>>anichargame` `>>anicg` | A minigame where you guess the name of the anime character shown. You can add "hint" in the command to make it show the character's scrambled name. The Kud reward is equal to the number of characters of the shortest part of the characters name. If the hint is used, the Kud reward is split in half. | `>>animechargame hint`
`>>buyupgrade` `>>shop` | Opens Sigma's profession upgrade shop. | `>>buyupgrade`
`>>coinflip` `>>cf` | Flips a coin. Nothing complex. You can try guessing the results by typing either Heads or Tails. | `>>coinflip Heads`
`>>eightball` `>>8ball` | The 8Ball has answers to ALL your question. Come one, come all, and ask the mighty allknowing 8Ball! Provide a question at the end of the command and await the miraculous answer! | `>>eightball Will I ever be pretty?`
`>>filtersell` `>>fsell` | Sells all items that have a certain attribute. The accepted attributes are name, type and rarity. | `>>filtersell rarity:Legendary`
`>>finditem` | Looks up information about an item. The first argument needs to be the item type. For example if it is a fish, meat, plant or material. And the rest is the name of the item. | `>>finditem fish Jitteroon`
`>>fish` | Cast a lure and try to catch some fish. You can fish once every 60 seconds, better not scare the fish away. | `>>fish`
`>>forage` | Go hiking and search nature for all the delicious bounty it has. Look for plants that you might want to use for cooking in the future. Foraging is tiring so you need to rest for 60 seconds after looking for plants. | `>>forage`
`>>inspect` | Inspects an item that is in your inventory. | `>>inspect Nabfischz`
`>>inventory` `>>bag` `>>storage` `>>backpack` | Shows your current inventory. The inventory has unlimited slots. You can also specify the page number you want to see. The inventory is sorted by item rarity. | `>>inventory 2 @person`
`>>inventorystats` `>>invstats` `>>bagstats` | Shows the statistics of a user's inventory. The number of items per type and per rarity. | `>>inventorystats @person`
`>>joinrace` `>>jr` | Joins a race instance if any are ongoing. | `>>joinrace`
`>>mathgame` `>>mg` | A mathematics minigame. You are given a problem, solve it. Numbers are rounded to 2 decimals. You can also specify how hard you want the problem to be. The scale goes from 1-9. The default difficulty is 3. The time and Kud reward scale with the difficulty and number of hard operators. | `>>mathgame 4`
`>>quiz` | A quiz minigame with various quizes to choose from. With a lot more coming soon | `>>quiz`
`>>race` | Creates a race in the current text channel. To join the race use the joinrace command. A race needs at least 2 people to start. And has a maximum of 10 participants. You can specify a required buy-in to join the race. The winner gets the entire pool minus 10% that goes to the track upkeep. | `>>race 20`
`>>raceoverride` `>>raceover` | Overrides the race in case a bug occurs. | `>>raceoverride`
`>>roll` `>>dice` | Gives a random number from 0 to 100. You can specify the highest number the function calls by adding a number after the command. The Number TECHNICALLY does not have a limit but the bigger you use, the bigger the message, which just looks plain spammy. | `>>roll 501`
`>>rps` `>>rockpaperscissors` | Play Rock-Paper-Scissors with the bot. No cheating, we swear. Maybe she just doesn't like you. | `>>rps s`
`>>sell` | Sells an item from your inventory. Input all instead of the item name to sell your entire inventory. | `>>sell Copula`
`>>slots` | Spin the slot machine, maybe you win, maybe you don't. Who knows? It costs 10 Kud to spin the slot machine by default. But you can specify how much you want to put in the machine. And the rewards are based on how many of the same icon you get in the middle row. Rewards are different for each icon. The slots can be spun only once every 60 seconds. | `>>slots 52`
`>>unscramble` `>>usg` | A minigame where you guess the scrambled word. You have 30 seconds to guess the word shown. The Kud reward is equal to the number of letters in the word. | `>>unscramble`
`>>upgrades` | Shows the user's current upgrades. You can view another person's upgrades by tagetting them. | `>>upgrades @person`
`>>vnchargame` `>>vncg` | A minigame where you guess the name of the visual novel character shown. You can add "hint" in the command to make it show the character's scrambled name. The Kud reward is equal to the number of characters of the shortest part of the characters name. If the hint is used, the Kud reward is split in half. | `>>vnchargame`
[Back To Top](#index)

### MISCELANOUS
Commands | Description | Example
----------|-------------|--------
`>>afk` | Sets you as afk. Whenever someone mentions you they will be notified that you are afk. When you send a message your afk status will be removed. This automatic removal ignores commands. | `>>afk Sleeping or eating, probably both!`
`>>choose` | The bot will select a thing from the inputed list. Separate list items with a semicolon and space. | `>>choose Sleep; Eat; Code; Lewd Stuff`
`>>httpstatus` `>>http` | Shows information about a HTTP response status code. | `>>httpstatus 404`
`>>poll` | Creates a poll with the items from the inputted list. Separate list items with a semicolon and a space. | `>>poll Want to eat?; Yes; No; Hand me the cheese!`
`>>randombetween` `>>ranin` | Outputs a random number between two inputted numbers. | `>>randombetween 59 974`
`>>remind` `>>remindme` `>>setreminder` `>>alarm` | Sets a timer that will mention the author when it's done. The time format is H:M:S. You can technically type 999:999:999. Really no limit to that. | `>>remind 1:03:15 LEEEEROOOOY JEEEEEENKIIIIINS!`
[Back To Top](#index)

### MODERATION
Commands | Description | Example
----------|-------------|--------
`>>ban` | Ban a user from the server. This will also remove all messages from that user in the last 24h. The user can only be targeted by a mention tag. This is to preserve compatibility with logging and audits. | `>>ban @person Way, WAY too spicy for us...`
`>>kick` | Kicks a user from the server. The user can only be targeted by a mention tag. This is to preserve compatibility with logging and audits. | `>>kick @person Couldn't handle the spice.`
`>>purge` `>>prune` | Deletes X number of messages posted by the mentioned person. If a user is not provided, it will prune the last X messages regardless of poster. If a number is not provided it will prune the last 100 messages. If neither number nor user is provided, it will prune the bots messages. Requires the user who calls the command to have the Manage Messages permission. | `>>purge X @person`
`>>softban` `>>sb` | Soft-Ban a user from the server. This bans the user and immediatelly unbans them. Useful if you want to purge all messages from that user in the last 24h. The user can only be targeted by a mention tag. This is to preserve compatibility with logging and audits. | `>>softban @person Some spice needed de-spicing.`
`>>textmute` `>>tmute` | Disallows the user from typing. Well technically, it will make the bot auto delete any message they send. You can add a message at the end to be sent to the user as the reason why. | `>>textmute @person Was too spicy!`
`>>textunmute` `>>tunmute` | Disallows the user from typing. Well technically, it will make the bot auto delete any message they send. | `>>textunmute @person`
`>>unban` | Unbans a banned user by inputted username. | `>>unban Chicken Shluggets`
`>>unwarn` `>>clearwarnings` `>>clearwarns` | Clears a user's warning. A user target and warning ID are required. You can input "all" instead of an idea to clear all their warnings. | `>>unwarn @person all`
`>>warn` | Adds a user to the warning list along with the reason stated. The used will also receive a direct message from the bot stating they have been warned. Warnings can be cleared with the unwarn command. | `>>warn @person Bit my dog`
`>>warning` `>>warninfo` | Shows information regarding a user's warning. Both the mention of the user and the warning ID are required. | `>>warning @person 12af`
`>>warnings` `>>warns` | Shows what the mentioned user was warned for. If the user who calls the command doesn't have the manage message permission, it will show their warnings instead, | `>>warnings @person`
[Back To Top](#index)

### MUSIC
Commands | Description | Example
----------|-------------|--------
`>>disconnect` `>>stop` | Stops the music, disconnects the bot from the current voice channel, and purges the music queue. | `>>disconnect`
`>>musicoverride` `>>overridemusic` `>>musickill` `>>killmusic` | Overrides the current music player in instances where sigma is stuck in a channel. This will not purge the queue, just disconnect the bot. | `>>musicoverride`
`>>nowplaying` `>>currentsong` `>>playing` `>>np` | Shows information regarding the currently playing song. | `>>nowplaying`
`>>play` `>>start` | Starts playing the music queue. | `>>play`
`>>queue` `>>add` | Queues up a song to play from YouTube. Either from a direct URL or text search. Playlists are supported but take a long time to process. | `>>queue Kaskade Disarm You Illenium Remix`
`>>repeat` | Toggles if the current queue should be repeated. Whenever a song is played, it's re-added to the end of the queue. | `>>repeat`
`>>shuffle` | Randomizes the current song queue. | `>>shuffle`
`>>skip` `>>next` | Skips the currently playing song. | `>>skip`
`>>summon` `>>move` | If the bot isn't connected to any channel, it'll connect to yours. If it is connected, it will move to you. | `>>summon`
`>>unqueue` `>>remove` | Removes a song from the queue. Minimum number is 1 and the maximum is however many items the queu has. Even though list indexes start at zero. | `>>unqueue 5`
[Back To Top](#index)

### NIHONGO
Commands | Description | Example
----------|-------------|--------
`>>jisho` | Searches Jisho, which is the Japanese language dictionary, for your input. Resulting in various information regarding your lookup. | `>>jisho Kawaii`
`>>wanikani` `>>wk` | Shows the mentioned person's WaniKani statistics. If no person is mentioned it will show the author's stats. This requires the person to have a WaniKani API key stored with the wksave command. | `>>wanikani @person`
`>>wanikanisave` `>>wksave` | Saves your WaniKani API key in the database so the wanikani command can be used. | `>>wanikanisave 123456798`
[Back To Top](#index)

### NSFW
Commands | Description | Example
----------|-------------|--------
`>>boobs` | Outputs a random NSFW image focusing on the breasts of the model. | `>>boobs`
`>>butts` | Outputs a random NSFW image focusing on the ass of the model. | `>>butts`
`>>danbooru` | Searches Danbooru for the given tag. If no tag is given, the keyword "nude" will be used. As on all image galleries, tags are bound with a "+". If your search has spaces replace them with underscores "_". | `>>danbooru kawaii`
`>>e621` | Searches E621 for the given tag. If no tag is given, the keyword "nude" will be used. As on all image galleries, tags are bound with a "+". If your search has spaces replace them with underscores "_". | `>>e621 knot`
`>>gelbooru` | Searches Gelbooru for the given tag. If no tag is given, the keyword "nude" will be used. As on all image galleries, tags are bound with a "+". If your search has spaces replace them with underscores "_". | `>>gelbooru ovum`
`>>keyvis` | This command returns a Key Visual Arts VN CG. It picks a random VN and a random CG from that VN. You can specify the VN you want the CG to be from. "kud" - Kud Wafter "air" - Air "kanon" - Kanon "little" - Little Busters "clan" - Clannad "plan" - Planetarian "rewr" - Rewrite "harv" - Rewrite Harvest Festa This command is rated explicit due to some CGs being explicit.  | `>>keyvis kud`
`>>konachan` | Searches Konachan for the given tag. If no tag is given, the keyword "nude" will be used. As on all image galleries, tags are bound with a "+". If your search has spaces replace them with underscores "_". | `>>konachan thighhighs`
`>>rule34` | Searches Rule34 for the given tag. If no tag is given, the keyword "nude" will be used. As on all image galleries, tags are bound with a "+". If your search has spaces replace them with underscores "_". | `>>rule34 switch`
`>>xbooru` | Searches Xbooru for the given tag. If no tag is given, the keyword "nude" will be used. As on all image galleries, tags are bound with a "+". If your search has spaces replace them with underscores "_". | `>>xbooru ovum`
`>>yandere` | Searches yandere for the given tag. If no tag is given, the keyword "nude" will be used. As on all image galleries, tags are bound with a "+". If your search has spaces replace them with underscores "_". | `>>yandere naked_apron`
[Back To Top](#index)

### PERMISSIONS
Commands | Description | Example
----------|-------------|--------
`>>disablecommand` `>>dcmd` `>>cmdoff` `>>commandoff` | Disallows a command to be used on the server. Disabled commands are then overwritten by one of the permit commands. Those with the Administrator permission are not affected. | `>>disablecommand nyaa`
`>>disablemodule` `>>dmdl` `>>mdloff` `>>moduleoff` | Disallows an entire module to be used on the server. Disabled modules are then overwritten by one of the permit commands. Those with the Administrator permission are not affected. | `>>disablemodule fun`
`>>enablecommand` `>>cmdon` `>>commandon` | Enables a previously disabled command. | `>>enablecommand kitsune`
`>>enablemodule` `>>mdlon` `>>moduleon` | Enables a previously disabled module. | `>>enablemodule minigames`
`>>permitchannel` | Allows a previously disabled command or module to be used in the specified channel. Follow the usage example, C for command, M for module. | `>>permitchannel m:fun #channel`
`>>permitrole` | Specifies a role that can use a disabled command or module group. It needs to be specified if it is a command or module group. If it is a command use C and if it is a module use M following the example. | `>>permitrole c:csshumor Wizards`
`>>permituser` | Specifies a user that can use a disabled command or module. It needs to be specified if it's a command or module group. If it is a command use C, if it is a module use M, following the usage example. | `>>permituser c:pun @person`
`>>unpermitchannel` | Removes the channel override for a disabled command or module. Follow the usage example, C for command, M for module. | `>>unpermitchannel m:fun #channel`
`>>unpermitrole` | Removes permissions from a role that can use a disabled command or module group to do so. It needs to be specified if it is a command or module group. If it is a command use C and if it is a module use M following the example. | `>>unpermitrole m:minigames Gamblers`
`>>unpermituser` | Unpermits a user from using a previously overridden command or module. It needs to be specified if it's a command or module group. If it is a command use C, if it is a module use M, following the usage example. | `>>unpermituser m:fun @person`
[Back To Top](#index)

### ROLES
Commands | Description | Example
----------|-------------|--------
`>>addselfrole` `>>addrank` `>>asr` | Sets a role as self assignable. Roles that are self assignable, any user can assign to themselves. To assign a self assignbale role to yourself, use the togglerole command. | `>>addselfrole Cheese Lover`
`>>autorole` `>>autorank` | Sets which role should be given to joining members. When a new user enters the server, this role will be assigned to them. The role can not be something that is above the bot's highest role. If you want to disable the autorole, input "disable" as the role name. | `>>autorole Newcomer`
`>>delselfrole` `>>delrank` `>>rsr` `>>dsr` | Removes a role from the list of self assignable roles. | `>>delselfrole Meat Lover`
`>>listselfroles` `>>listranks` `>>listroles` `>>ranks` `>>roles` `>>lsrl` | Toggles a self assignable role. If you don't have the role, it will be given to you. If you do have the role, it will be removed from you. | `>>listselfroles Overlord`
`>>togglerole` `>>togglerank` `>>rank` `>>trl` | Toggles a self assignable role. If you don't have the role, it will be given to you. If you do have the role, it will be removed from you. | `>>togglerole Overlord`
[Back To Top](#index)

### SEARCHES
Commands | Description | Example
----------|-------------|--------
`>>anime` `>>animu` `>>kitsuanime` | Searches Kitsu.io for the inputted anime. The outputed results will be information like the number of episodes, user rating, air time, plot summary, and poster image. | `>>anime Plastic Memories`
`>>antonyms` `>>antonym` `>>ant` | Looks up words that have opposite meaning for the given term. | `>>antonyms late`
`>>cryptocurrency` `>>cryptocur` `>>crypcur` `>>ecoin` | Shows the statistics for the imputted crypto currency. Stats include the current market cap, price, supply, volume, change. | `>>cryptocurrency ethereum`
`>>deezer` `>>music` `>>findsong` | Searches Deezer for infomation on the given song. The output will include a song preview link. | `>>deezer Highway to Hell`
`>>describe` `>>desc` | Looks up words that are often used to describe nouns or are often used by the adjective.  Specify the mode in the first argument. adjectives, adjective, adj or a - to look up nouns that are often described by an adjective. nouns, noun or n - to look up adjectives that are often used to describe a noun.  | `>>describe noun ocean`
`>>dictionary` `>>dict` `>>definition` `>>define` `>>def` | Searches the oxford dictionary for the definition of your input. | `>>dictionary cork`
`>>homophones` `>>homophone` | Looks up words that sound like the given term. | `>>homophones coarse`
`>>imdb` `>>movie` | Searches the Internet Movie DataBase for your input. Gives you the poster, release year and who stars in the movie, as well as a link to the page of the movie. | `>>imdb Blade Runner`
`>>manga` `>>mango` `>>kitsumanga` | Searches Kitsu.io for the inputted manga. The outputed results will be information like the number of chapters, user rating, plot summary, and poster image. | `>>manga A Silent Voice`
`>>recipe` `>>food` | Searches for a dish, or dishes that use inputted ingredients, and outputs one that might be a good match for your search querry. | `>>recipe Chicken in Curry Sauce`
`>>reddit` | Enter a subreddit and it will show a random post from the current top posts in hot. This is by default, you can specify where to grab it from as an appended argument to the end. The accepted arguments are TopHot, RandomHot, TopNew, RandomNew, TopTop and RandomTop. Random arguments choose randomly from a list of 100 first entries. | `>>reddit ProgrammerHumor`
`>>rhymes` `>>rhyme` | Looks up words that rhymes with the given term. | `>>rhymes forgetful`
`>>safebooru` `>>safe` | Returns a random image from the safebooru image repository. You can specify tags to narrow the range down, otherwise it's completely random. | `>>safebooru kawaii`
`>>soundslike` `>>soundlike` | Looks up words that are spelled similarly to the given term. | `>>soundslike elefint`
`>>spelledlike` `>>spelllike` `>>spellike` `>>spellcheck` | Looks up words that are spelled similarly to the given term. Supports the following wildcards ? - one character * - one or many characters  | `>>spelledlike coneticut`
`>>synonyms` `>>synonym` `>>syn` | Looks up words that have exact or nearly same meaning for the given term. | `>>synonyms ocean`
`>>urbandictionary` `>>urbandict` `>>urban` `>>ud` | Looks up the definition for a word or term in the Urban Dictionary. It is strongly suggested to take these with a grain of salt. | `>>urbandictionary dictionary`
`>>weather` `>>we` | Shows meteorological information about the inputed location. You can additionall add a unit argument at the end of the lookup. The allowed units are... auto: automatically select units based on geographic location ca: same as si, except that windSpeed is in kilometers per hour uk2: same as si, except that nearestStormDistance and visibility are in miles and windSpeed is in miles per hour us: Imperial units (the default) si: SI units If no unit is selected it default to auto.  | `>>weather Belgrade unit:si`
`>>wikipedia` `>>wiki` | Returns the summary of a wikipedia page that you inputted the search for. If a search is too general, an error will be returned. | `>>wikipedia Thread (Computing)`
`>>youtube` `>>yt` | A simple youtube search. Outputs the resulting video's information and URL. You can add "-text" at the end of your search to make it a normal URL to the video. Instead of an embed with information. | `>>youtube Game Grumps`
[Back To Top](#index)

### SETTINGS
Commands | Description | Example
----------|-------------|--------
`>>addcommand` `>>addcmd` | Adds a custom command trigger to the server. Whenever this trigger word is used with a command prefix the inputted response will be provided. Command requires the Manage Server permission. | `>>addcommand hi Hello world!`
`>>asciionlynames` `>>forceascii` | Toggles if only ASCII characters are allowed in names. The bot will check members each 60s for an invalid name and rename them if they are not proper. To change the default temporary name, use the asciitempname command. | `>>asciionlynames`
`>>asciitempname` `>>asciitemp` | Changes the default temporary name for those who the temp name was enforced on. | `>>asciitempname <ChangeMePleaseI'mLonely>`
`>>blockedwords` | Lists all blocked words on the server. | `>>blockedwords`
`>>blockinvites` `>>filterinvites` | Toggles if invite links should be automatically removed. When an invite link is removed, the message author is notified and the removal is logged. This ignores anybody with a Manage Server permission. | `>>blockinvites`
`>>blockwords` `>>blockword` | Adds all the words you list to the blocked words filter. If any of the words in the filter is sent, the message will be removed and the author will be notified. | `>>blockwords crap`
`>>bye` `>>goodbye` | Toggles if the bot should say when users leave the server. The goodbye feature is active by default. | `>>bye`
`>>byechannel` `>>byech` | Sets the channel the goodbye messages should be sent to. Of course unless byedm is active. | `>>byechannel #welcome`
`>>byemessage` `>>byemsg` | This sets the message shown to leaving members when they entre the server. There are certain syntaxes for controling what is displayed. {user_name} - Basic text of the leaving user's name. {user_discriminator} - The numbers after the # in the user's name. {user_mention} - A mention tag of the leaving user. {user_id} - The leaving user's discord ID. {server_name} - Text showing the server's name. {server_id} - The server's discord ID. {owner_name} - Basic text showing the name of the server owner. {owner_discriminator} - The numbers after the # in the owner's name. {owner_mention} - A mention tag of the server's owner. {owner_id} - The server owner's discord ID.  | `>>byemessage Hello {user_mention}, welcome to {server_name}!`
`>>chatterbot` | Toggles if the Chatterbot functions should be active. If active, when a message starts with a mention of Sigma, she will respond. This setting is active by default. | `>>chatterbot`
`>>deletecommands` `>>delcmds` | Toggles if messages that are a command should be automatically deleted. | `>>deletecommands`
`>>greet` | Toggles if the bot should greet users when they enter the server. The greeting feature is active by default. | `>>greet`
`>>greetchannel` `>>greetch` | Sets the channel the greeting messages should be sent to. Of course unless greetdm is active. | `>>greetchannel #welcome`
`>>greetdm` `>>greetpm` | Toggles if the bot should greet users by sending them a Direct Message, instead of writing the message in a channel. | `>>greetdm`
`>>greetmessage` `>>greetmsg` | This sets the message shown to joining members when they entre the server. There are certain syntaxes for controling what is displayed. {user_name} - Basic text of the joining user's name. {user_discriminator} - The numbers after the # in the user's name. {user_mention} - A mention tag of the joining user. {user_id} - The joining user's discord ID. {server_name} - Text showing the server's name. {server_id} - The server's discord ID. {owner_name} - Basic text showing the name of the server owner. {owner_discriminator} - The numbers after the # in the owner's name. {owner_mention} - A mention tag of the server's owner. {owner_id} - The server owner's discord ID.  | `>>greetmessage Hello {user_mention}, welcome to {server_name}!`
`>>logedits` | Toggles if message editing should be logged in the server's logging channel. | `>>logedits`
`>>loggingchannel` `>>logchannel` `>>logch` | Designates a channel where server events will be logged to. The stuff that is logged is member movement and moderator actions. Such as warns, bans, muting members and pruning channels. To disable the logging channel, input "disable" as the channel argument. | `>>loggingchannel #logging`
`>>prefix` | Sets the prefix that Sigma should respond to. This will be bound to your server and you can set it to anything you'd like. However, the prefix can not contain spaces. They will be automatically removed. | `>>prefix !!`
`>>removecommand` `>>remcmd` | Removes a custom command trigger used for custom commands from the server. Command requires the Manage Server permission. | `>>removecommand hi`
`>>unblockwords` `>>unblockword` | Removes a blocked word allowing people to send messages containing it. | `>>unblockwords boobs`
`>>unflip` | Toggles if Sigma should respond to tables being flipped. | `>>unflip`
[Back To Top](#index)

### STATISTICS
Commands | Description | Example
----------|-------------|--------
`>>experience` `>>activity` `>>level` `>>exp` `>>xp` | Shows how much of Sigma's internal experience you obtained. Experience is earned by being an active member of the community. Yes, this is meant to be vague. | `>>experience @person`
`>>profile` `>>mystats` | Shows Sigma's statistics for the mentioned user. Their current experience, level and most used commands. | `>>profile @person`
`>>topcommands` `>>topcmds` | Shows the top 20 most used commands globally. | `>>topcommands`
`>>topcookies` | Shows the top 20 users who have the most cookies. | `>>topcookies`
`>>topcurrency` `>>topkud` | Shows the top 10 people in the Kud leaderboards. You can specify if you want to see the top people that are local, global, or by their current kud. The leaderboard shows the local server's leaderboard by default. | `>>topcurrency global`
`>>topexperience` `>>topxp` | Shows the top 10 people in the Experience leaderboards. You can specify if you want to see the top people that are local, global, or by their current xp. The leaderboard shows the local server's leaderboard by default. | `>>topexperience local`
`>>wallet` `>>currency` `>>money` `>>kud` | Shows how much of Sigma's internal currency you currently have. As well as how much you've earned on the current server and in total. Kud is earned by being an active member of the community. Yes, this is meant to be vague. | `>>wallet @person`
[Back To Top](#index)

### UTILITY
Commands | Description | Example
----------|-------------|--------
`>>avatar` `>>av` | Shows the mentioned user's avatar. If no user is mentioned, it shows the author's avatar. | `>>avatar @person`
`>>botinformation` `>>botinfo` `>>info` | Shows information about the bot, version, codename, authors, etc. | `>>botinformation`
`>>bots` | Lists the bots on the server where the command is used and shows their status. | `>>bots`
`>>channelid` `>>chid` `>>cid` | Shows the User ID of the mentioned channel. If no channel is mentioned, it will show the ID of the channel the command is used in. If you don't want the return message to be an embed, add "text" at the end. | `>>channelid #channel`
`>>channelinformation` `>>channelinfo` `>>chinfo` `>>cinfo` | Shows various information and data on the mentioned channel. If no user is mentioned, it will show data for the channel the command is written in. | `>>channelinformation #channel`
`>>color` `>>colour` `>>clr` | Shows the inputted color. It accepts either a HEX code or an RGB array. | `>>color #1abc9c`
`>>ingame` | Shows the top played games on the server. | `>>ingame @person`
`>>permissions` `>>perms` | Shows which permissions a user has and which they do not. If no user is mentioned, it will target the message author. | `>>permissions @person`
`>>roleinformation` `>>roleinfo` `>>rinfo` | Shows various information and data for the inputted role. | `>>roleinformation`
`>>rolepopulation` `>>rolepop` | Shows the population of the inputted role. If no arguments are provided, it will show the top 20 roles by population. | `>>rolepopulation Warlard`
`>>servericon` `>>srvicon` `>>icon` | Shows the server's icon image. | `>>servericon`
`>>serverid` `>>guildid` `>>srvid` `>>sid` `>>gid` | Shows the Server ID of the server the command is used in. | `>>serverid`
`>>serverinformation` `>>serverinfo` `>>sinfo` | Shows various information and data of the server the command is used in. | `>>serverinformation`
`>>shortenurl` `>>shorten` `>>bitly` | Shortens a URL for you using BitLy. All URLs returned via Sigma are without ads, merely shortened using the service. | `>>shortenurl https://i.redd.it/ngwebbf5nwfz.jpg`
`>>statistics` `>>stats` | Shows Sigma's current statistics. Population and message and command counts and rates since startup. As well as when the bot last started. | `>>statistics`
`>>status` | Shows the status of Sigma's machine. Processor information, memory, storage, network, etc. | `>>status`
`>>userid` `>>uid` | Shows the User ID of the mentioned user. If no user is mentioned, it will show the author's ID. If you don't want the return message to be an embed, add "text" at the end. | `>>userid @person`
`>>userinformation` `>>userinfo` `>>uinfo` | Shows various information and data on the mentioned user. If no user is mentioned, it will show data for the message author. | `>>userinformation @person`
`>>whoplays` | Generates a list of users playing the inputted game. | `>>whoplays Overwatch`
[Back To Top](#index)