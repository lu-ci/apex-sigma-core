**Hey there!** We need your **help**! Come support us on [**Patreon**](https://www.patreon.com/ApexSigma)!

## Module Index
- [DEVELOPMENT](#development)
- [FUN](#fun)
- [HELP](#help)
- [INTERACTIONS](#interactions)
- [LOGGING](#logging)
- [MATHEMATICS](#mathematics)
- [MINIGAMES](#minigames)
- [MISCELLANEOUS](#miscellaneous)
- [MODERATION](#moderation)
- [MUSIC](#music)
- [NIHONGO](#nihongo)
- [NSFW](#nsfw)
- [OSU](#osu)
- [OVERWATCH](#overwatch)
- [PATH OF EXILE](#path of exile)
- [PERMISSIONS](#permissions)
- [ROLES](#roles)
- [SEARCHES](#searches)
- [SETTINGS](#settings)
- [STATISTICS](#statistics)
- [UTILITY](#utility)
- [WARFRAME](#warframe)

### DEVELOPMENT
Commands | Description | Example
----------|-------------|--------
`>>addstatus` | Adds a status message to Sigma's database for automatic status rotation. (Bot Owner Only) | `>>addstatus with tentacles`
`>>awardleaderboards` `>>awardlbs` | Awards all the global leaderboards. Basically gives a large amount of Kud to the top 20 users in each leaderboard category. Currency earned, experience, and cookies. (Bot Owner Only) | `>>awardleaderboards`
`>>blacklistmodule` `>>blackmodule` `>>blackmdl` | Disallows a person from using a specific module category. (Bot Owner Only) | `>>blacklistmodule 0123456789 minigames`
`>>blacklistserver` `>>blacklistguild` `>>blacksrv` `>>blackguild` | Marks a server as blacklisted. This disallows any user on that server from using commands. (Bot Owner Only) | `>>blacklistserver 0123456789`
`>>blacklistuser` `>>blackusr` | Marks a user as blacklisted, disallowing them to use any command. (Bot Owner Only) | `>>blacklistuser 0123456789`
`>>destroycurrency` `>>destroykud` `>>descurr` `>>deskud` | Takes away the inputted amount of corrency from the mentioned user. The currency goes first and then the user mention as shown in the example. (Bot Owner Only) | `>>destroycurrency 150 @person`
`>>destroyitem` `>>desitem` | Destroys the item with the given ID. (Bot Owner Only) | `>>destroyitem abcdef1234567890`
`>>eject` | Makes Sigma leave a Discord server. (Bot Owner Only) | `>>eject 0123456789`
`>>evaluate` `>>evaluate` `>>eval` `>>py` `>>python` `>>code` `>>exec` | Executes raw python code. This should be used with caution. You should never use this unless you are certain of what you are doing. (Bot Owner Only) | `>>evaluate print('hello world')`
`>>generatecurrency` `>>generatekud` `>>gencurr` `>>genkud` | Awards the mentioned user with the inputted amount of currency. The currency goes first and then the user mention as shown in the example. (Bot Owner Only) | `>>generatecurrency 150 @person`
`>>generateitem` `>>genitem` | Creates and gives an item to the tagged user from the inputted category. (Bot Owner Only) | `>>generateitem @person plants Blue Delta`
`>>geterror` | Gets an error's details using the given token. (Bot Owner Only) | `>>geterror 9a2e9a374ac90294f225782f362e2ab1`
`>>getreaction` `>>getreact` | No description provided. (Bot Owner Only) | `>>getreaction 4242ea69`
`>>reload` | Reloads all of the modules in Sigma. This includes both commands and events. (Bot Owner Only) | `>>reload`
`>>removereaction` `>>removereact` `>>delreact` | Remove a reaction with the inputed ID. (Bot Owner Only) | `>>removereaction 1ba2e263f287522f`
`>>removestatus` | Removes a status with the inputed ID from Sigma's status database. (Bot Owner Only) | `>>removestatus 1d9cae144f`
`>>resetleaderboards` `>>resetlbs` | Resets the global leaderboard data. Global experience, currency and cookies. (Bot Owner Only) | `>>resetleaderboards`
`>>sabotageuser` `>>sabusr` | Sabotages a user making them have extreme bad luck in various modules. (Bot Owner Only) | `>>sabotageuser 0123456789`
`>>send` | Sends a message to a user, channel or server. The first argument needs to be the destination parameter. The destination parameter consists of the destination type and ID. The types are U for User and C for Channel. The type and ID are separated by a colon, or two dots put more simply. (Bot Owner Only) | `>>send u:0123456789 We are watching...`
`>>setavatar` | Sets the avatar of the bot either to the linked or attached image. The officially supported formats for bot avatars are JPG and PNG images. Note that bots, like all users, have limited profile changes per time period. (Bot Owner Only) | `>>setavatar https://my_fomain.net/my_avatar.png`
`>>setstatus` | Sets the current playing status of the bot. To use this, the automatic status rotation needs to be disabled. It can be toggled with the togglestatus command. (Bot Owner Only) | `>>setstatus with fishies`
`>>setusername` | Sets the name of the bot to the inputted text. Note that bots, like all users, have limited profile changes per time period. (Bot Owner Only) | `>>setusername Supreme Bot`
`>>shutdown` | Forces the bot to disconnect from Discord and shut down all processes. (Bot Owner Only) | `>>shutdown`
`>>sysexec` `>>sh` | Executes a shell command. Extreme warning! This executes commands in the Operating System's Shell. Command Prompt on Windows and Bash on Linux. It will execute things on the same level of authority as the program is ran by. Meaning, don't do something stupid and wipe your damn root. (Bot Owner Only) | `>>sysexec echo 'Hello'`
`>>test` | For testing purposes, obviously. Used as a placeholder for testing functions. | `>>test`
`>>togglestatus` | Toggles if the automatic status rotation is enabled or disabled. (Bot Owner Only) | `>>togglestatus`
`>>wipeawards` | Removes a user's currency, experience and cookie data. Used when wanting to remove a blacklisted user's ill gotten gains. (Bot Owner Only) | `>>wipeawards 0123456789`
[Back To Top](#module-index)

### FUN
Commands | Description | Example
----------|-------------|--------
`>>award` `>>pay` | Awards a chosen amount of Kud from the vault to a targeted person. The amount of Kud needs to go first, followed by the target. Only server managers can award Kud from the vault. Anybody can contribute to the vault with the givetovault command. | `>>award 500 @person`
`>>bash` | If you are old enough to know what IRC is or remember how it looked like, then you will appreciate the quotes that the bash command produces. | `>>bash`
`>>cat` | Outputs a random cat image. Furry felines like it when their owners observe them. | `>>cat`
`>>catfact` | Outputs a random fact about your lovely furry assh~ eerrrr... I mean, companion! | `>>catfact`
`>>chucknorris` | This command outputs a random Chuck Norris joke. We use Chuck jokes because Bruce Lee is no joke, obviously. | `>>chucknorris`
`>>cookies` | Shows how many cookies you have, or how many a mentioned user has. Cookies are given with the givecookie command. | `>>cookies @person`
`>>csshumor` | The only thing better than a joke is a joke written in CSS. And while that is sarcasm to a certain degree, these really are fun. Embrace your web designer within and read some CSS jokes. | `>>csshumor`
`>>cyanideandhappiness` `>>cnh` | Outputs an image of a random Cyanide and Happiness comic. Explosm makes awesome comics and animations. | `>>cyanideandhappiness`
`>>dab` | All words escape me on what this command does, just use it. | `>>dab`
`>>dadjoke` | This will provide a joke that might be something your father would say. You know they are bad, but you will love them anyway, cause you are a good kid. | `>>dadjoke`
`>>dog` | Outputs a random dog image. Cutest, loyalest little woofers. | `>>dog`
`>>dogfact` `>>doggofact` | Outputs a random fact about man's best friend. | `>>dogfact`
`>>famousquote` `>>fquote` | Gives you a random inspirational or deep quote. | `>>famousquote`
`>>fortune` `>>fortune-mod` | Linux users, and raw UNIX users in general will know the fortune-mod. This command uses their entire database to output one of their quotes. | `>>fortune`
`>>givecookie` `>>gibcookie` | Gives a cookie to a person. Remember to give them only to nice people. You can give only one cookie every hour and can't give them to yourself. If you target @someone with the command, the cookie will be given to a random member of the server. | `>>givecookie @person`
`>>givecurrency` `>>givecurr` `>>givekud` | Transfers Kud between you and a targetted person. The Kud amount goes first and the target tag afterwards like it is given in the example above. | `>>givecurrency 100 @person`
`>>givetovault` `>>givetobank` `>>gtv` `>>gtb` | The vault is a server specific Kud storage system. Members can contribute to the vault with this command. The kud can then be awarded to users using the award command. | `>>givetovault 500`
`>>joke` | Outputs a joke. It is not really special or anything... Sometimes they are funny, most of the times they are not. | `>>joke`
`>>kitsunemimi` `>>kon` `>>fluffytail` | Displays a random kitsunemimi image. In case you don't know what a kitsunemimi is, it's a foxgirl. All images are sourced from Safebooru, but be warned that some can be very borderline. | `>>kitsunemimi`
`>>leetspeak` `>>leet` `>>l33t` | Turns your inputted statement into l33t text. You can add which level of leet you want your text to be converted to. As it's displayed in the usage example. The accepted levels are basic, advanced and ultimate. | `>>leetspeak owned level:ultimate`
`>>nekomimi` `>>neko` `>>nyaa` | Displays a random nekomimi image. In case you don't know what a nekomimi is, it's a catgirl. All images are sourced from Safebooru, but be warned that some can be very borderline. | `>>nekomimi`
`>>numberfact` `>>numfact` `>>numf` | Searches for interesting things about a given number. You can also insert a date in the DAY/MON format. You can specify a type of number you want retrived in the format TYPE:NUMBER. The allowed types are trivia, math, date, year. You can also specify "random" instead of a number to make it a random number. | `>>numberfact 42`
`>>pun` | If you do not know what a pun is... Oh you poor innocent soul. This command will produce a lovely little pun for you. Enjoy the cringe! | `>>pun`
`>>randomcomicgenerator` `>>rcg` | Uses the Cyanide and Happiness random comic generator for buttloads of fun. Personally the favorite comic command. | `>>randomcomicgenerator`
`>>realprogrammers` `>>realdevelopers` `>>rp` `>>rd` | Tells you what real programmers do. | `>>realprogrammers`
`>>reversetext` `>>reverse` | Reverses the text that you input into the command. | `>>reversetext hello`
`>>ronswanson` | Everyone's favorite character from Parks and Recreation. This command will output a random quote from Ron Swanson. | `>>ronswanson`
`>>shootfoot` `>>sf` | Tells you how to shoot yourself in the foot with the given programming language. If no language is provided, it will pick a random one. | `>>shootfoot Python`
`>>vault` `>>bank` | Shows the current amount of Kud in the guild's vault. | `>>vault`
`>>visualnovelquote` `>>vnquote` `>>vnq` | Outputs a random quote from a random VN. Displays it's source as well, of course. If the source visual novel of the quote is NSFW, the image will be hidden and the footer will state that. | `>>visualnovelquote`
`>>xkcd` | If you like humorous things and know a bit of technology, you will lose a lot of time reading these. XKCD comics are perfect for procrastination and time wasting. | `>>xkcd`
`>>yomomma` `>>yomama` `>>yomoma` `>>ym` | Want to insult some poor fool's mother but don't have the right comeback? This command will provide the perfect yo momma joke for the task. | `>>yomomma`
[Back To Top](#module-index)

### HELP
Commands | Description | Example
----------|-------------|--------
`>>commands` `>>modules` `>>cmds` `>>mdls` | If not module name is inputed, it will show the list of available modules. To see the commands in a module category, input that modules name. | `>>commands minigames`
`>>donate` | Shows donation information for Sigma. | `>>donate`
`>>help` `>>h` | Provides the link to Sigma's website and support server. As well as show information about a command if something in inputted. | `>>help fish`
`>>invite` `>>inv` | Provides Sigma's invitation link to add her to your server. | `>>invite`
[Back To Top](#module-index)

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
`>>lovecalculator` `>>lovecalc` | Shows the love between two tagged users. | `>>lovecalculator @person1 @person2`
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
[Back To Top](#module-index)

### LOGGING
Commands | Description | Example
----------|-------------|--------
`>>logbans` | Toggles logging of when users get banned. | `>>logbans`
`>>logdeletions` `>>logdeletes` `>>logdels` | Toggles logging of messages being deleted. | `>>logdeletions`
`>>logedits` | Toggles logging of messages being edited. | `>>logedits`
`>>logfilters` | Toggles logging of when a user's message is deleted due to containing a blacklisted word or when posting links when they are not allowed. | `>>logfilters`
`>>loggingchannel` `>>logchannel` `>>logch` | Designates a channel where server events will be logged to. The stuff that is logged is member movement and moderator actions. Such as warns, bans, muting members and pruning channels. To disable the logging channel, input "disable" as the channel argument. | `>>loggingchannel #logging`
`>>logkicks` | Toggles logging of when users get kicked. | `>>logkicks`
`>>logmodule` | Toggles logging of commands in the specified module being used. | `>>logmodule moderation`
`>>logmovement` | Toggles logging of when users join and/or leave the server. | `>>logmovement`
`>>logmutes` | Toggles logging of when users get text muted/unmuted and hard muted/unmuted. | `>>logmutes`
`>>logpurges` | Toggles logging of when a channel gets purged. | `>>logpurges`
`>>logwarnings` | Toggles logging of when users get warned or unwarned. | `>>logwarnings`
[Back To Top](#module-index)

### MATHEMATICS
Commands | Description | Example
----------|-------------|--------
`>>blockcollector` `>>nochain` `>>nocollector` `>>disablechain` `>>disablecollector` | Toggles the ability for other users to collect a chain for you. If active, only you will be able to collect a markov chain for yourself. If not, the collector works as always, where anybody can start a chain collection for you. | `>>blockcollector`
`>>collectchain` `>>collch` | Collects messages sent by the mentioned user and saves it as a chain. Only one chain can be collected at a time so a queue is implemented. If a user isn't tagged, it will collect a chain for you. And if a channel isn't tagged, it will collect items from the one that the command is used in. | `>>collectchain @person #channel`
`>>combinechains` `>>combine` `>>cmbch` `>>mix` | Like the impersonate command. This one however targets two uers and uses their chains to generated a mixed response. | `>>combinechains @target_one @target_two`
`>>currenttime` `>>time` | Shows the current time in UTC. You can specify a time zone as well. If you wish to convert time, use the timeconvert command. | `>>currenttime PDT`
`>>decrypt` | Decrypts any message that was encrypted using the Sigma Heart Key. You can add ":t" at the end to force it to be raw text instead of an embed. | `>>decrypt H7U2JfWkr0zCApDPDkO`
`>>dokidoki` `>>doki` `>>dd` | Makes a random markov chain based sentence from a random Doki Doki Literature Club character quote. You can force which character to quote by adding their name as an argument to the command. And you can force a glitch by adding ":glitch" as the ending argument. | `>>dokidoki`
`>>encrypt` | Encrypts the message of your choice using the Sigma Heart Key. The message can be decrypted using the decrypt command. You can add ":t" at the end to force it to be raw text instead of an embed. | `>>encrypt I will always be here to talk to you for as long as you want.`
`>>impersonate` `>>mimic` | Tries to impersonate the mentioned user if a chain file for them exists. This command is on a 20 second cooldown due to it's weight. The more items in your chain you have, the better the output. Having a low number of items, or having items that aren't good enough, might result in Sigma not being able to generate anything. The optimal amount is 5000 items. You can check how many items you have with the chain command. | `>>impersonate @person`
`>>makehash` `>>hash` | Creates a hash using the inputed has type. These are all the hash types you can use. sha512, sha3_224, sha3_512, MD4, dsaWithSHA, ripemd160, RIPEMD160, SHA, ecdsa-with-SHA1, sha3_384, SHA512, sha1, SHA224, md4, DSA-SHA, SHA384, blake2b, dsaEncryption, SHA256, sha384, sha, DSA, shake_128, sha224, SHA1, shake_256, sha256, MD5, blake2s, md5, sha3_256, whirlpool | `>>makehash md5 Nabzie is best tree.`
`>>markovchain` `>>chain` | Shows how many items you have in your chain, or the targetted users'. | `>>markovchain @person`
`>>timeconvert` `>>tconv` | Converts the given time in the given time zone to the inputted time zone. | `>>timeconvert 18:57 UTC>PST`
`>>wipechain` `>>clearchain` | It wipes your entire Markov chain, if you have one. | `>>wipechain`
`>>wolframalpha` `>>wa` | Makes a request for Wolfram Alpha to process. This can be a lot of things, most popular being complex math operations. | `>>wolframalpha 69+42`
[Back To Top](#module-index)

### MINIGAMES
Commands | Description | Example
----------|-------------|--------
`>>animechargame` `>>anichargame` `>>anicg` | A minigame where you guess the name of the anime character shown. You can add "hint" in the command to make it show the character's scrambled name. The Kud reward is equal to the number of characters of the shortest part of the characters name. If the hint is used, the Kud reward is split in half. | `>>animechargame hint`
`>>buyupgrade` `>>shop` | Opens Sigma's profession upgrade shop. | `>>buyupgrade`
`>>chances` | Shows a table with your item chance statistics. | `>>chances @person`
`>>coinflip` `>>cf` | Flips a coin. Nothing complex. You can try guessing the results by typing either Heads or Tails. | `>>coinflip Heads`
`>>cook` `>>make` | Uses a recipe to create an item from raw resources that you've gathered. You can see all available recipes with the recipes command. | `>>cook Shade Tea`
`>>eightball` `>>8ball` | The 8Ball has answers to ALL your questions. Come one, come all, and ask the mighty allknowing 8Ball! Provide a question at the end of the command and await the miraculous answer! | `>>eightball Will I ever be pretty?`
`>>filtersell` `>>fsell` | Sells all items that have a certain attribute. The accepted attributes are name, type and rarity. | `>>filtersell rarity:Legendary`
`>>finditem` | Looks up information about an item. Like inspect, but you don't need to have the item. | `>>finditem fish Jitteroon`
`>>fish` | Cast a lure and try to catch some fish. You can fish once every 60 seconds, better not scare the fish away. | `>>fish`
`>>forage` | Go hiking and search nature for all the delicious bounties it has. Look for plants that you might want to use for cooking in the future. Foraging is tiring so you need to rest for 60 seconds after looking for plants. | `>>forage`
`>>hunt` | Go into the wilderness and hunt for game. You can hunt once every 60 seconds, everyone needs rest. | `>>hunt`
`>>inspect` | Inspects an item that is in your inventory. | `>>inspect Nabfischz`
`>>inventory` `>>bag` `>>storage` `>>backpack` | Shows your current inventory. The inventory has 64 slots at the start but can be upgraded in the shop. You can also specify the page number you want to see. The inventory is sorted by item rarity. Items used in recipes are marked with an asterisk. | `>>inventory 2 @person`
`>>inventorystats` `>>invstats` `>>bagstats` | Shows the statistics of a user's inventory. The number of items per type and per rarity. | `>>inventorystats @person`
`>>joinrace` `>>jr` | Joins a race instance if any are ongoing in the current channel. | `>>joinrace`
`>>mangachargame` `>>mangochargame` `>>mancg` | A minigame where you guess the name of the manga character shown. You can add "hint" in the command to make it show the character's scrambled name. The Kud reward is equal to the number of characters of the shortest part of the characters name. If the hint is used, the Kud reward is split in half. | `>>mangachargame hint`
`>>mathgame` `>>mg` | A mathematics minigame. You are given a problem, solve it. Numbers are rounded to 2 decimals. You can also specify how hard you want the problem to be. The scale goes from 1-9. The default difficulty is 3. The time and Kud reward scale with the difficulty and number of hard operators. | `>>mathgame 4`
`>>race` | Creates a race in the current text channel. To join the race use the joinrace command. A race needs at least 2 people to start, and has a maximum of 10 participants. You can specify a required buy-in to join the race. The winner gets the entire pool minus 10% that goes to the track upkeep. | `>>race 20`
`>>raceoverride` `>>raceover` `>>killrace` | Overrides the race in case a bug occurs. | `>>raceoverride`
`>>recipes` | Lists all recipes available for making. The recipe list is limited to 10 items per page. You can specify the number of the page that you want to view. | `>>recipes`
`>>roll` `>>dice` | Rolls a number from 0 to the one you provided. You can also roll dice as in the example above. Following the format [Number of Dice]d[MaxNumber] +[Bonus]. | `>>roll 5d10 +2`
`>>rps` `>>rockpaperscissors` | Play Rock-Paper-Scissors with the bot. No cheating, we swear. She just doesn't like you. | `>>rps s`
`>>sell` | Sells an item from your inventory. Input all instead of the item name to sell your entire inventory. | `>>sell Copula`
`>>sequencegame` `>>sequence` `>>sqcg` | Starts a sequence guessing game. 4 symbols will randomly be chosen and you have to guess them in 6 tries or fewer. When a symbol is in the corret position the diamond will be blue. If it is in the sequence but incorrect position, it will be yellow. If the symbol is not in the sequence, a red triangle will be shown. The symbols can repeat, the Kud award is 50. | `>>sequencegame`
`>>slots` | Spin the slot machine, maybe you win, maybe you don't. Who knows? It costs 10 Kud to spin the slot machine by default. But you can specify how much you want to put in the machine. And the rewards are based on how many of the same icon you get in the middle row. Rewards are different for each icon. The slots can be spun only once every 60 seconds. | `>>slots 52`
`>>trivia` `>>triv` `>>t` | A trivia minigame. You are given a question and have to input the number of your answer. Guess correctly and you win 5-15 Kud, depending on the difficulty. You have 20 seconds to answer the question. | `>>trivia`
`>>unscramble` `>>usg` | A minigame where you guess the scrambled word. You have 30 seconds to guess the word shown. The Kud reward is equal to the number of letters in the word. | `>>unscramble`
`>>upgrades` | Shows the user's current upgrades. You can view another person's upgrades by tagetting them. | `>>upgrades @person`
`>>viewrecipe` `>>recipe` `>>vrec` | Shows information about a recipe. Such as the ingredients required, value of the item, and it's description. | `>>viewrecipe Shade Tea`
`>>vnchargame` `>>vncg` | A minigame where you guess the name of the visual novel character shown. You can add "hint" in the command to make it show the character's scrambled name. The Kud reward is equal to the number of characters of the shortest part of the characters name. If the hint is used, the Kud reward is split in half. | `>>vnchargame`
[Back To Top](#module-index)

### MISCELLANEOUS
Commands | Description | Example
----------|-------------|--------
`>>afk` | Sets you as afk. Whenever someone mentions you they will be notified that you are afk. When you send a message your afk status will be removed. This automatic removal ignores messages that start with the command prefix. | `>>afk Sleeping or eating, probably both!`
`>>choose` | The bot will select a thing from the inputed list. Separate list items with a semicolon and space. | `>>choose Sleep; Eat; Code; Lewd Stuff`
`>>edgecalculator` `>>edgecalc` | Calculates how edgy the targeted person is. If no user is tagged, the target will be the one who uses the command. | `>>edgecalculator @person`
`>>endraffle` `>>endraf` | Prematurely ends a raffle. Usable only by the raffle's creator. The responses are the same as the redraw command. If an active raffle with the given id is not found, it will be a magnifying glass. If you are not the creator of the raffle, a no entry sign. If no ID is given, an exclamation. | `>>endraffle 1abc9c`
`>>httpstatus` `>>http` | Shows information about a HTTP response status code. | `>>httpstatus 404`
`>>listraffles` `>>listraf` `>>lraf` | Lists all your ongoing raffles and their information. Such as in how long they end and where they are ongoing. | `>>listraffles`
`>>myreminders` `>>reminders` `>>rms` | Shows a list of the reminders that you have created. The location where they are set to execute in. And in what time they execute in. If you add "here" to the end of the command, it will only show reminders made in the current channel. | `>>myreminders here`
`>>poll` | Creates a poll with the items from the inputted list. Separate list items with a semicolon and a space. | `>>poll Want to eat?; Yes; No; Hand me the cheese!`
`>>quote` | Quotes a message from it's given ID. | `>>quote 381449702589202432`
`>>raffle` `>>giveaway` | Starts a raffle with a given timer and title. Entering the raffle works by reacting to Sigma's embed message with an automatically given reaction. When the timer runs out a message will appear in the channel the raffle was made in and the creator of the raffle and the winner will be tagged. | `>>raffle 48:30:59 50,000 Kud`
`>>randombetween` `>>ranin` | Outputs a random number between two inputted numbers. | `>>randombetween 59 974`
`>>redrawraffle` `>>redraw` | Redraws a raffle in case that's ever needed. This command is only usable by the author of the raffle. To redraw a raffle use the raffle's ID that can be found in it's footer. This command has no response aside from a reaction to your message. If all is well, a green check will appear, if the user is not the author, it will be a no entry sign, if a raffle with that ID is not found, a magnifying glass will be the reaction, if no arguments are provided, it will be an exclamation mark. A raffle needs to be marked as ended before it can be redrawn. | `>>redrawraffle 1abc9c`
`>>reminderinfo` `>>reminder` `>>rminfo` `>>rmi` | Shows information about your reminder with the given ID. Such as when it executes and where. | `>>reminderinfo f93f`
`>>remindme` `>>remind` `>>setreminder` `>>alarm` `>>rmme` | Sets a timer that will mention the author when it's done. The time format is H:M:S, but is not limited to the constraints of their types. Meaning you can type "200:5000:999999" if you wish. Reminders are limited to 90 days, and you are limited to 15 reminders. | `>>remindme 1:03:15 LEEEEROOOOY JEEEEEENKIIIIINS!`
`>>removereminder` `>>delreminder` `>>unremind` `>>delrm` | Deletes a reminder of yours with the inputted ID. | `>>removereminder 1a9e`
`>>shadowpoll` | Makes a private shadow poll. The user that voted on the shadow poll can only be seen by it's creator. Additional commands can set an expiration timer for the shadow poll and the visibility of the poll's current vote count and percentages. | `>>shadowpoll Ban Nuggetlord?; Yes; Yes; Yes; No; Soft`
`>>shadowpollclose` `>>spclose` | Closes/deactivated a shadow poll. Closed polls can not be voted on and can not be viewed unless they are set to be visible. | `>>shadowpollclose 1bca22`
`>>shadowpolldelete` `>>spdelete` `>>spdel` | Permanently deletes a shadow poll. | `>>shadowpolldelete 1bca22`
`>>shadowpollexpires` `>>spexpiration` `>>spexpires` `>>spexpire` | Sets a poll to automatically close after the given time elapses. The time to close is counted from the command execution, not the initial opening of the poll. When the poll expires the author will be notified of the expiration. Only the poll's creator can edit it's expiration time. | `>>shadowpollexpires 1bca22 48:30:59`
`>>shadowpollinvisible` `>>spinvisible` `>>spinvis` | Reverts a shadow poll back to invisible. Making it's statistics only accessible to the author. All shadow polls are invisible by default. | `>>shadowpollinvisible 1bca22`
`>>shadowpolllist` `>>splist` | Lists all shadow polls that you have created. You can also list the polls that are active and created in the current server or channel by adding a "server" or "channel" argument to the command. Polls that have expired or that are closed are marked with an exclamation mark. | `>>shadowpolllist channel`
`>>shadowpollopen` `>>spopen` | Opens a previously closed poll. If the poll has an expiration timer, it will be wiped. | `>>shadowpollopen 1bca22`
`>>shadowpollpermit` `>>sppermit` `>>spperm` | Permits a role, channel or user to vote in the poll. If no permission settings are set, anybody can vote on the poll. If any permissions are set, only items permitted can vote in the poll. Tag a user to permit a user, tag a channel to permit a channel, or type the name of the role you want to permit. | `>>shadowpollpermit 1bca22 #council`
`>>shadowpollstats` `>>spstats` | Shows statistics for the given poll. Total count of votes and votes for each option as well as percentages. | `>>shadowpollstats 1bca22`
`>>shadowpollunpermit` `>>spunpermit` `>>spunperm` | Unpermits a previously permitted object from voting on the poll. For more information check the description of the sppermit command. | `>>shadowpollunpermit 1bca22 Disowned`
`>>shadowpollview` `>>spview` | Displays a shadow poll's question and possible options. If the poll is not active and not finished, information will not be displayed. Unless of course the one who uses the view command is the poll's creator. | `>>shadowpollview 1bca22`
`>>shadowpollvisible` `>>spvisible` `>>spvis` | Marks a poll as visible. If a poll is visible anybody can see it's statistics. Such as total vote count and how many votes go to each choice. | `>>shadowpollvisible 1bca22`
`>>shadowpollvote` `>>spvote` | Votes on a shadow poll. Choosing multiple options is not allowed. Re-using the command will result in your vote being changed. | `>>shadowpollvote 1bca22`
`>>shadowpollvoters` `>>spvoters` | Shows all the users that voted on a shadow poll and what they voted on. This command can only be used by the author of the poll. | `>>shadowpollvoters 1bca22`
`>>shadowpollwipe` `>>spwipe` | Completely resets a poll's statistics. Deleting all the data about who voted for what option. | `>>shadowpollwipe 1bca22`
[Back To Top](#module-index)

### MODERATION
Commands | Description | Example
----------|-------------|--------
`>>ban` | Bans a user from the server. This will also remove all messages from that user in the last 24h. The user can only be targeted by a mention tag. This is to preserve compatibility with logging and audits. | `>>ban @person Way, WAY too spicy for us...`
`>>hardmute` `>>hmute` | Hard-mutes the target user. Users who are hard-muted are disallowed from typing to any channel. There is no message deletion, this is a permission based mute. | `>>hardmute @person For talking about the fight club.`
`>>hardunmute` `>>hunmute` | Unmutes a hard-muted person. Allowing them to send messages again. | `>>hardunmute @person`
`>>issuewarning` `>>warn` | Issues a warning to a user with the reason stated. The warning reason is not mandatory. When the user is warned they will be sent a direct message about it. Each warning has a unique ID that you can call and view with the warninginfo command. | `>>issuewarning @person Took too long in the bathroom.`
`>>kick` | Kicks a user from the server. The user can only be targeted by a mention tag. This is to preserve compatibility with logging and audits. | `>>kick @person Couldn't handle the spice.`
`>>listwarnings` `>>warns` `>>warnings` | Lists all active warnings issued to the target user. The list is compact and shows only the warning IDs, the issuer of the warning, and when the warning was issued. A moderator with manage messages permissions can view any user's warnings while users without said permission can only view the list of theirs. The warning list is paginated, 5 warnings per page. Just add the page number to the end of the command to see that page. | `>>listwarnings @person`
`>>purge` `>>prune` | Deletes X number of messages posted by the mentioned person. If a user is not provided, it will prune the last X messages regardless of poster. If a number is not provided it will prune the last 100 messages. If neither number nor user is provided, it will prune the bots messages. Requires the user who calls the command to have the Manage Messages permission. If you add "attachments" to the command arguments it will only purge messages that have attachments. If you add "content:something you want gone" to the command arguments it will only delete messages that have the inputted content after "content:" in them, which can be a word or a sentence. Due to content catching everything after the ":" in it, it's suggested to be the last argument in the command. | `>>purge X @person`
`>>removewarning` `>>unwarn` | Shows detailed information for the given user's warning. Both the user mention and the warning ID are needed for the command. | `>>removewarning @person 1abc`
`>>softban` `>>sb` | Soft-Ban a user from the server. This bans the user and immediatelly unbans them. Useful if you want to purge all messages from that user in the last 24h. The user can only be targeted by a mention tag. This is to preserve compatibility with logging and audits. | `>>softban @person Some spice needed de-spicing.`
`>>textmute` `>>tmute` | Disallows the user from typing. Well technically, it will make the bot auto delete any message they send. You can add a message at the end to be sent to the user as the reason why. Users with the Administrator permission are ignored, their messages will not be deleted. Requires the user who calls the command to have the Manage Messages permission. | `>>textmute @person Was too spicy!`
`>>textunmute` `>>tunmute` | Removes the tagged person from the list of muted users. Making the bot no longer delete their messages. Requires the user who calls the command to have the Manage Messages permission. | `>>textunmute @person`
`>>unban` | Unbans a banned user by inputted username. | `>>unban Chicken Shluggets`
`>>viewwarning` `>>warning` `>>warninginfo` | Shows detailed information for the given user's warning. Both the user mention and the warning ID are needed for the command. | `>>viewwarning @person 1abc`
[Back To Top](#module-index)

### MUSIC
Commands | Description | Example
----------|-------------|--------
`>>disconnect` `>>stop` | Stops the music, disconnects the bot from the current voice channel, and purges the music queue. | `>>disconnect`
`>>nowplaying` `>>currentsong` `>>playing` `>>np` | Shows information regarding the currently playing song. | `>>nowplaying`
`>>pause` | Pauses the music player. | `>>pause`
`>>play` `>>start` | Starts playing the music queue. | `>>play`
`>>queue` `>>add` | Queues up a song to play from YouTube. Either from a direct URL or text search. Playlists are supported but take a long time to process. | `>>queue Kaskade Disarm You Illenium Remix`
`>>repeat` | Toggles if the current queue should be repeated. Whenever a song is played, it's re-added to the end of the queue. | `>>repeat`
`>>resume` | Resumes the music player. | `>>resume`
`>>shuffle` | Randomizes the current song queue. | `>>shuffle`
`>>skip` `>>next` | Skips the currently playing song. | `>>skip`
`>>summon` `>>move` | If the bot isn't connected to any channel, it'll connect to yours. If it is connected, it will move to you. | `>>summon`
`>>unqueue` `>>remove` | Removes a song from the queue. Minimum number is 1 and the maximum is however many items the queue has. Even though list indexes start at zero. | `>>unqueue 5`
[Back To Top](#module-index)

### NIHONGO
Commands | Description | Example
----------|-------------|--------
`>>jisho` | Searches Jisho, which is the Japanese language dictionary, for your input. Resulting in a display of various types of information regarding your lookup. | `>>jisho Kawaii`
`>>kanji` | Searches Jisho, which is the Japanese language dictionary, for specified kanji. Returns stroke count, stroke order, parts, variants, meanings and readings. | `>>kanji 夢`
`>>wanikani` `>>wk` | Shows the mentioned person's WaniKani statistics. If no person is mentioned it will show the author's stats. This requires the person to have a WaniKani API key stored with the wksave command. | `>>wanikani @person`
`>>wanikanisave` `>>wksave` | Saves your WaniKani API key in the database so the wanikani command can be used. | `>>wanikanisave 123456798`
[Back To Top](#module-index)

### NSFW
Commands | Description | Example
----------|-------------|--------
`>>boobs` `>>tits` | Outputs a random NSFW image focusing on the breasts of the model. | `>>boobs`
`>>butts` `>>ass` | Outputs a random NSFW image focusing on the ass of the model. | `>>butts`
`>>e621` | Searches E621 for the given tag. If no tag is given, the keyword "nude" will be used. As on all image galleries, tags are bound with a "+". If your search has spaces replace them with underscores "_". | `>>e621 knot`
`>>gelbooru` `>>gelb` | Searches Gelbooru for the given tag. If no tag is given, the keyword "nude" will be used. As on all image galleries, tags are bound with a "+". If your search has spaces replace them with underscores "_". | `>>gelbooru ovum`
`>>keyvis` | This command returns a Key Visual Arts VN CG. It picks a random VN and a random CG from that VN. You can specify the VN you want the CG to be from. "kud" - Kud Wafter "air" - Air "kanon" - Kanon "little" - Little Busters "clan" - Clannad "plan" - Planetarian "rewr" - Rewrite "harv" - Rewrite Harvest Festa This command is rated explicit due to some CGs being explicit.  | `>>keyvis kud`
`>>konachan` `>>kchan` | Searches Konachan for the given tag. If no tag is given, the keyword "nude" will be used. As on all image galleries, tags are bound with a "+". If your search has spaces replace them with underscores "_". | `>>konachan thighhighs`
`>>rule34` `>>r34` | Searches Rule34 for the given tag. If no tag is given, the keyword "nude" will be used. As on all image galleries, tags are bound with a "+". If your search has spaces replace them with underscores "_". | `>>rule34 switch`
`>>xbooru` `>>xb` | Searches Xbooru for the given tag. If no tag is given, the keyword "nude" will be used. As on all image galleries, tags are bound with a "+". If your search has spaces replace them with underscores "_". | `>>xbooru ovum`
`>>yandere` `>>yre` | Searches yandere for the given tag. If no tag is given, the keyword "nude" will be used. As on all image galleries, tags are bound with a "+". If your search has spaces replace them with underscores "_". | `>>yandere naked_apron`
[Back To Top](#module-index)

### OSU
Commands | Description | Example
----------|-------------|--------
`>>osu` | Generates a signature image with the user's stats for osu!. | `>>osu AXAz0r`
[Back To Top](#module-index)

### OVERWATCH
Commands | Description | Example
----------|-------------|--------
`>>overwatch` `>>owstats` `>>ow` | Outputs the Overwatch statistics for the given player from the given region. Do note that the battletag is case sensitive, Aurora#22978 is not the same as aurora#22978 | `>>overwatch EU Aurora#22978`
[Back To Top](#module-index)

### PATH OF EXILE
Commands | Description | Example
----------|-------------|--------
`>>poeactive` `>>poeasg` | Shows information about a Path of Exile Active Skill Gem. | `>>poeactive Cold Snap`
`>>poebody` | Shows information about a Path of Exile Body Armor piece of equipment. | `>>poebody Arena Plate`
`>>poeboots` | Shows information about Path of Exile boots. | `>>poeboots Arena Plate`
`>>poegloves` | Shows information about Path of Exile boots. | `>>poegloves Arena Plate`
`>>poehelmet` | Shows information about Path of Exile helmets. | `>>poehelmet Arena Plate`
`>>poeshield` | Shows information about Path of Exile shields. | `>>poeshield Arena Plate`
`>>poesupport` `>>poessg` | Shows information about a Path of Exile Support Skill Gem. | `>>poesupport Iron Will`
[Back To Top](#module-index)

### PERMISSIONS
Commands | Description | Example
----------|-------------|--------
`>>disablecommand` `>>dcmd` `>>cmdoff` `>>commandoff` | Disallows a command to be used on the server. Disabled commands are then overwritten by one of the permit commands. Those with the Administrator permission are not affected. | `>>disablecommand nyaa`
`>>disablemodule` `>>dmdl` `>>mdloff` `>>moduleoff` | Disallows an entire module to be used on the server. Disabled modules are then overwritten by one of the permit commands. Those with the Administrator permission are not affected. | `>>disablemodule fun`
`>>enablecommand` `>>cmdon` `>>commandon` | Enables a previously disabled command. | `>>enablecommand kitsune`
`>>enablemodule` `>>mdlon` `>>moduleon` | Enables a previously disabled module. | `>>enablemodule minigames`
`>>permitchannel` `>>pch` `>>pchs` `>>permch` `>>permchs` `>>permitc` `>>permitcs` `>>permitchannels` | Allows a previously disabled command or module to be used in the specified channel. Follow the usage example, C for command, M for module. Multiple channels can be tagged. | `>>permitchannel m:fun #channel`
`>>permitrole` `>>prl` `>>permrl` `>>permitr` | Specifies a role that can use a disabled command or module group. It needs to be specified if it is a command or module group. If it is a command use C and if it is a module use M following the example. | `>>permitrole c:csshumor Wizards`
`>>permituser` `>>pusr` `>>pusrs` `>>permusr` `>>permusrs` `>>permitu` `>>permitus` `>>permitusers` | Specifies a user that can use a disabled command or module. It needs to be specified if it's a command or module group. If it is a command use C, if it is a module use M, following the usage example. Multiple users can be tagged. | `>>permituser c:pun @person`
`>>unpermitchannel` `>>upch` `>>upchs` `>>unpermch` `>>unpermchs` `>>unpermitc` `>>unpermitcs` `>>unpermitchannels` | Removes the channel override for a disabled command or module. Follow the usage example, C for command, M for module. Multiple channels can be tagged. | `>>unpermitchannel m:fun #channel`
`>>unpermitrole` `>>uprl` `>>unpermrl` `>>unpermitrl` | Removes permissions from a role that can use a disabled command or module group to do so. It needs to be specified if it is a command or module group. If it is a command use C and if it is a module use M following the example. | `>>unpermitrole m:minigames Gamblers`
`>>unpermituser` `>>upusr` `>>upusrs` `>>unpermusr` `>>unpermusrs` `>>unpermitu` `>>unpermitus` `>>unpermitusers` | Unpermits a user from using a previously overridden command or module. It needs to be specified if it's a command or module group. If it is a command use C, if it is a module use M, following the usage example. Multiple users can be tagged. | `>>unpermituser m:fun @person`
[Back To Top](#module-index)

### ROLES
Commands | Description | Example
----------|-------------|--------
`>>addselfrole` `>>addrank` `>>asr` | Sets a role as self assignable. Roles that are self assignable, any user can assign to themselves. To assign a self assignbale role to yourself, use the togglerole command. | `>>addselfrole Cheese Lover`
`>>autorole` `>>autorank` | Sets which role should be given to joining members. When a new user enters the server, this role will be assigned to them. The role can not be something that is above the bot's highest role. If you want to disable the autorole, input "disable" as the role name. | `>>autorole Newcomer`
`>>autoroletimeout` `>>arltimeout` `>>arlt` | Sets the number of seconds the bot should wait before assigning the set auto-role. To disable the timeout, simply input 0 as the timeout, nothing special. | `>>autoroletimeout 600`
`>>bindemoterole` `>>berl` | Binds a role to an emote role group. Emote role groups are limited to have 10 roles per group. | `>>bindemoterole 5a8e3 King Killers`
`>>bindinvite` `>>bindinvs` `>>binvite` `>>binv` | Binds an invite to a role. When a member joins using that invite the stated role will be given to them. | `>>bindinvite aEUCHwX Cheese Lovers`
`>>bindrole` `>>brl` | Binds a role to a role group. Role groups are limited to have 32 roles per group. | `>>bindrole 5a8e3 King Killers`
`>>boundinvites` `>>boundinvs` `>>binvites` `>>binvs` | Lists all the invites that are bound and what they are bound to. | `>>boundinvites`
`>>colorme` `>>clrme` `>>cme` | If the current guild has color roles enabled, you can color yourself with this command. For more information about how this works, use the help command on the colorroles command. Any other (prefixed) color roles on you will be removed prior to adding the new one. | `>>colorme #1abc9c`
`>>deleteemoterolegroup` `>>derg` `>>rerg` | Deletes an emote role group. This cannot be undone. Emote role groups are created with the makeemoterolegroup command. | `>>deleteemoterolegroup 5a8e3`
`>>deleterolegroup` `>>drg` `>>rrg` | Deletes a role group. This cannot be undone. Role groups are created with the makerolegroup command. | `>>deleterolegroup 5a8e3`
`>>delselfrole` `>>delrank` `>>rsr` `>>dsr` | Removes a role from the list of self assignable roles. | `>>delselfrole Meat Lover`
`>>giverole` `>>giverank` `>>grole` `>>grank` | Gives the inputed role to the tagged user. The role must be below Sigma in Discord hierarchy. | `>>giverole @person Grandma`
`>>listemoterolegroups` `>>lerg` | Lists emote role groups on the server. The list is paginated, you can enter the page you want to see after the command name as an argument. To view a role groups details, such as the populace and roles that are bound to that group, use the viewemoterolegroup command. | `>>listemoterolegroups 2`
`>>listrolegroups` `>>lrg` | Lists role groups on the server. The list is paginated, you can enter the page you want to see after the command name as an argument. To view a role groups details, such as the populace and roles that are bound to that group, use the viewrolegroup command. | `>>listrolegroups 2`
`>>listselfroles` `>>listranks` `>>listroles` `>>ranks` `>>roles` `>>lsrl` | Lists all self assignable roles present on the server. | `>>listselfroles`
`>>makeemoterolegroup` `>>merg` `>>cerg` | Creates a role group for binding emote role to. Emote roles need to be limited to groups due to generating emote toggle messages for said roles which have limited emote numbers. As a good side effect, this also allows placing multiple emote toggle messages in different places with slight alterations. | `>>makeemoterolegroup`
`>>makeemotetoggles` `>>metg` | Makes the core message that cotains the emotes for the emote role toggles. You enter the ID of the emote role group you want to make a toggler for and can also specify the channel you want it to go. If no channel is specified the toggler is created in the current channel. The toggler message contains instruction on how to use the toggles. You can add "nodesc" to the end of the command if you don't want the toggle instructions to be displayed in the toggler message. | `>>makeemotetoggles 5a8e3 #channel`
`>>makerolegroup` `>>mrg` `>>crg` | Creates a role group for binding a role to. Role groups are limited to 32 roles per group. | `>>makerolegroup`
`>>pruneroles` `>>proles` | Removes all empty roles from the server. | `>>pruneroles`
`>>removerole` `>>removerank` `>>rrole` `>>rrank` | Removes the inputed role from the tagged user. The role must be below Sigma in Discord hierarchy. | `>>removerole @person Wangly`
`>>syncinvites` `>>syncinvs` `>>sinvs` | Forces an update of the invite cache for your server. For use if you have suspicions that the bound role counters are out of sync. | `>>syncinvites`
`>>togglerole` `>>togglerank` `>>rank` `>>trl` | Toggles a self assignable role. If you don't have the role, it will be given to you. If you do have the role, it will be removed from you. | `>>togglerole Overlord`
`>>unbindemoterole` `>>uberl` | Unbind a role from an emote role group. | `>>unbindemoterole 5a8e3 Serpent Squires`
`>>unbindinvite` `>>unbinvite` `>>unbindinv` `>>unbinv` | Unbinds a previously bound invite from it's bound role. If the invite with that ID no longer exists on your server add ":f" to the end to force remove it. Please not that if you are force removing an invite that it is case sensitive. | `>>unbindinvite aEUCHwX`
`>>unbindrole` `>>ubrl` | Unbind a role from a role group. | `>>unbindrole 5a8e3 Serpent Squires`
`>>viewemoterolegroup` `>>verg` | Shows emote role group details such as roles that are in the group, and the total population of the group roles. | `>>viewemoterolegroup 5a8e3`
`>>viewrolegroup` `>>vrg` | Shows role group details such as roles that are in the group, and the total population of the group roles. | `>>viewrolegroup 5a8e3`
[Back To Top](#module-index)

### SEARCHES
Commands | Description | Example
----------|-------------|--------
`>>anime` `>>animu` `>>kitsuanime` | Searches Kitsu.io for the inputted anime. The outputed results will be information like the number of episodes, user rating, air time, plot summary, and poster image. | `>>anime Plastic Memories`
`>>antonyms` `>>antonym` `>>ant` | Looks up words that have opposite meanings for the given term. | `>>antonyms late`
`>>busplus` | Returns the bus departure times from both terminus locations for the given line number. This is only for the Belgrade BusPlus transit tracking system. It will display the departure times for the current, previous and next hour. | `>>busplus 18`
`>>cryptocurrency` `>>cryptocur` `>>crypcur` `>>ecoin` | Shows the statistics for the imputted crypto currency. Stats include the current market cap, price, supply, volume, change. | `>>cryptocurrency ethereum`
`>>deezer` `>>music` `>>findsong` | Searches Deezer for infomation on the given song. The output will include a song preview link. | `>>deezer Highway to Hell`
`>>describe` `>>desc` | Looks up words that are often used to describe nouns or are often used by the adjective. Specify the mode in the first argument. adjectives, adjective, adj, a: To look up nouns that are often described by an adjective. nouns, noun, n: To look up adjectives that are often used to describe a noun.  | `>>describe noun ocean`
`>>dictionary` `>>dict` `>>definition` `>>define` `>>def` | Searches the Oxford dictionary for the definition of your input. | `>>dictionary cork`
`>>foodrecipe` `>>frec` `>>food` | Searches for a dish, or dishes that use inputted ingredients, and outputs one that might be a good match for your search query. | `>>foodrecipe Chicken in Curry Sauce`
`>>homophones` `>>homophone` | Looks up words that sound like the given one. | `>>homophones coarse`
`>>imdb` `>>movie` | Searches the Internet Movie DataBase for your input. Gives you the poster, release year and who stars in the movie, as well as a link to the page of the movie. | `>>imdb Blade Runner`
`>>manga` `>>mango` `>>kitsumanga` | Searches Kitsu.io for the inputted manga. The outputed results will be information like the number of chapters, user rating, plot summary, and poster image. | `>>manga A Silent Voice`
`>>mapsearch` `>>maps` `>>map` | Searches Google Maps for the inputted location. If specific details aren't found about the location, it will result in a broad search.  | `>>mapsearch Belgrade`
`>>reddit` | Enter a subreddit and it will show a random post from the current top posts in hot. This is by default, you can specify where to grab it from as an appended argument to the end. The accepted arguments are TopHot, RandomHot, TopNew, RandomNew, TopTop and RandomTop. Random arguments choose randomly from a list of 100 first entries. | `>>reddit ProgrammerHumor`
`>>rhymes` `>>rhyme` | Looks up words that rhymes with the given term. | `>>rhymes forgetful`
`>>safebooru` `>>safe` | Returns a random image from the safebooru image repository. You can specify tags to narrow the range down, otherwise it's completely random. | `>>safebooru kawaii`
`>>soundslike` `>>soundlike` | Looks up words that are spelled similarly to the given term. | `>>soundslike elefint`
`>>spelledlike` `>>spelllike` `>>spellike` `>>spellcheck` | Looks up words that are spelled similarly to the given term. Supports the following wildcards ? - one character * - one or many characters  | `>>spelledlike coneticut`
`>>synonyms` `>>synonym` `>>syn` | Looks up words that have exact or nearly the same meaning for the given term. | `>>synonyms ocean`
`>>urbandictionary` `>>urbandict` `>>urban` `>>ud` | Looks up the definition for a word or term in the Urban Dictionary. It is strongly suggested to take these with a grain of salt. | `>>urbandictionary dictionary`
`>>weather` `>>we` | Shows meteorological information about the inputed location. You can additionall add a unit argument at the end of the lookup. The allowed units are... auto: automatically select units based on geographic location ca: same as si, except that windSpeed is in kilometers per hour uk2: same as si, except that nearestStormDistance and visibility are in miles and windSpeed is in miles per hour us: Imperial units (the default) si: SI units If no unit is selected it default to auto.  | `>>weather Belgrade unit:si`
`>>wikipedia` `>>wiki` | Returns the summary of a wikipedia page that you inputted the search for. If a search is too general, an error will be returned. | `>>wikipedia Thread (Computing)`
`>>youtube` `>>yt` | A simple YouTube search. Outputs the resulting video's information and URL. You can add "-text" at the end of your search to make it a normal URL to the video. Instead of an embed with information. | `>>youtube Game Grumps`
[Back To Top](#module-index)

### SETTINGS
Commands | Description | Example
----------|-------------|--------
`>>addcommand` `>>addcmd` | Adds a custom command trigger to the server. Whenever this trigger word is used with a command prefix the inputted response will be provided. Command requires the Manage Server permission. Custom commands can have special dynamic arguments in them. {author_name}: Message author name. {author_nick}: Message author nickname. {author_mention}: Tag the message author. {author_id}: Message author's ID. {channel_name}: Channel name. {channel_mention}: Channel tag. {channel_id}: Channel ID. {server_name}: Server name. {server_id}: Server ID. {target_name}: Target name. {target_nick}: Target nickname. {target_mention}: Tag the target. {target_id}: Target ID.  | `>>addcommand hi Hello world!`
`>>addreactor` `>>addreac` | Adds an automatic reactor to the server. Whenever the given trigger word is detected the bot will react to the message with the given reaction. The :lcHello: above given in the example is a custom emote.  | `>>addreactor hi <:lcHello:309405155604824074>`
`>>addresponder` `>>addres` | Adds an auto-responder to the server. An automatic responder will reply with the set message to any sentence that conaints the chosen trigger in it as a standalone word. Responders can have special dynamic arguments in them like custom commands do. {author_name}: Message author name. {author_nick}: Message author nickname. {author_mention}: Tag the message author. {author_id}: Message author's ID. {channel_name}: Channel name. {channel_mention}: Channel tag. {channel_id}: Channel ID. {server_name}: Server name. {server_id}: Server ID. {target_name}: Target name. {target_nick}: Target nickname. {target_mention}: Tag the target. {target_id}: Target ID.  | `>>addresponder hi Hello there!`
`>>asciionlynames` `>>forceascii` | Toggles if only ASCII characters are allowed in names. The bot will check members each 60s for an invalid name and rename them if they are not proper. To change the default temporary name, use the asciitempname command. | `>>asciionlynames`
`>>asciitempname` `>>asciitemp` | Changes the default temporary name for those who the temp name was enforced on. | `>>asciitempname <ChangeMePleaseI'mLonely>`
`>>blockedwords` | Lists all blocked words on the server. | `>>blockedwords`
`>>blockinvites` `>>filterinvites` | Toggles if invite links should be automatically removed. When an invite link is removed, the message author is notified and the removal is logged. This ignores anybody with a Manage Server permission. | `>>blockinvites`
`>>blockwords` `>>blockword` | Adds all the words you list to the blocked words filter. If any of the words in the filter is sent, the message will be removed and the author will be notified. | `>>blockwords crap`
`>>bye` `>>goodbye` | Toggles if the bot should say when users leave the server. The goodbye feature is active by default. | `>>bye`
`>>byechannel` `>>byech` | Sets the channel the goodbye messages should be sent to. | `>>byechannel #welcome`
`>>byemessage` `>>byemsg` | This sets the message shown on the server when a member leaves. There are certain syntaxes for controlling what is displayed. {user_name} - Basic text of the leaving user's name. {user_discriminator} - The numbers after the # in the user's name. {user_mention} - A mention tag of the leaving user. {user_id} - The leaving user's discord ID. {server_name} - Text showing the server's name. {server_id} - The server's discord ID. {owner_name} - Basic text showing the name of the server owner. {owner_discriminator} - The numbers after the # in the owner's name. {owner_mention} - A mention tag of the server's owner. {owner_id} - The server owner's discord ID.  | `>>byemessage Hello {user_mention}, welcome to {server_name}!`
`>>chatterbot` | Toggles if the Chatterbot functions should be active. If active, when a message starts with a mention of Sigma, she will respond. This setting is active by default. | `>>chatterbot`
`>>colorroles` | Toggles the color role feature. This is deactivated by default. Once enabled members can use the colorme command to get a role with their requested color hex. Roles created with this feature have a SCR prefix in them and are created to be just one place under Sigma's top role with no permission changes. | `>>colorroles`
`>>customcommands` `>>customcmds` `>>custcmds` `>>ccmds` | Shows a list of the server's custom commands. The list is separated into pages of 10 items each. You can specify the page number you want to see. | `>>customcommands 4`
`>>deletecommands` `>>delcmds` | Toggles if messages that are a command should be automatically deleted. | `>>deletecommands`
`>>filterautowarn` | When a user triggers the blacklisted word filter, they will receive a warning. Like the warn command does, but automated. | `>>filterautowarn`
`>>greet` | Toggles if the bot should greet users when they enter the server. The greeting feature is active by default. | `>>greet`
`>>greetchannel` `>>greetch` | Sets the channel the greeting messages should be sent to, unless greetdm is active. | `>>greetchannel #welcome`
`>>greetdm` `>>greetpm` | Toggles if the bot should greet users by sending them a Direct Message, instead of writing the message in a channel. | `>>greetdm`
`>>greetmessage` `>>greetmsg` | This sets the message shown to joining members when they enter server. There are certain syntaxes for controlling what is displayed. {user_name} - Basic text of the joining user's name. {user_discriminator} - The numbers after the # in the user's name. {user_mention} - A mention tag of the joining user. {user_id} - The joining user's discord ID. {server_name} - Text showing the server's name. {server_id} - The server's discord ID. {owner_name} - Basic text showing the name of the server owner. {owner_discriminator} - The numbers after the # in the owner's name. {owner_mention} - A mention tag of the server's owner. {owner_id} - The server owner's discord ID.  | `>>greetmessage Hello {user_mention}, welcome to {server_name}!`
`>>inviteautowarn` | When a user triggers the invite blocker, they will receive a warning. Like the warn command does, but automated. | `>>inviteautowarn`
`>>prefix` | Sets the prefix that Sigma should respond to. This will be bound to your server and you can set it to anything you'd like. However, the prefix can not contain spaces. They will be automatically removed. | `>>prefix !!`
`>>reactors` `>>reacs` | Shows a list of the server's reaction triggers. The list is separated into pages of 10 items each. You can specify the page number you want to see. | `>>reactors 4`
`>>removecommand` `>>deletecommand` `>>remcmd` `>>delcmd` | Removes a custom command trigger used for custom commands from the server. This requires the Manage Server permission. | `>>removecommand hi`
`>>removereactor` `>>deletereactor` `>>remreac` `>>delreac` | Removes an automatic reaction trigger. | `>>removereactor hi`
`>>removeresponder` `>>deleteresponder` `>>remres` `>>delres` | Removes a custom command trigger used for custom commands from the server. Command requires the Manage Server permission. | `>>removeresponder hi`
`>>responders` `>>resps` | Shows a list of the server's custom responder triggers. The list is separated into pages of 10 items each. You can specify the page number you want to see. | `>>responders 4`
`>>unblockwords` `>>unblockword` | Removes a blocked word allowing people to send messages containing it. To purge the entire word filter enter -all as the command argument. | `>>unblockwords boobs`
`>>unflip` | Toggles if Sigma should respond to tables being flipped. | `>>unflip`
[Back To Top](#module-index)

### STATISTICS
Commands | Description | Example
----------|-------------|--------
`>>experience` `>>activity` `>>level` `>>exp` `>>xp` | Shows how much of Sigma's internal experience you obtained. Experience is earned by being an active member of the community. Yes, this is meant to be vague. | `>>experience @person`
`>>profile` `>>mystats` | Shows Sigma's statistics for the mentioned user. Their current experience, level and most used commands. | `>>profile @person`
`>>topcookies` | Shows the top 20 users who have the most cookies. A filter can be added, either global or total, sorting it by the amount they globaly have right now, which is the default, and the total amount of cookies that they have collected over time regardless of resets. | `>>topcookies global`
`>>topcurrency` `>>topkud` | Shows the top 20 users who have the most currency. A filter can be added, either global, local or total, sorting it by the amount they globaly have right now, which is the default, sorted by the amount that users have earned on this guild, and the total amount of currency that they have collected over time regardless of resets. | `>>topcurrency local`
`>>topexperience` `>>topexp` `>>topxp` | Shows the top 20 users who have the most experience. A filter can be added, either global, local or total, sorting it by the amount they globaly have right now, which is the default, sorted by the amount that users have earned on this guild, and the total amount of experience that they have collected over time regardless of resets. | `>>topexperience total`
`>>wallet` `>>currency` `>>money` `>>kud` | Shows how much of Sigma's internal currency you currently have. As well as how much you've earned on the current server and in total. Kud is earned by being an active member of the community. Yes, this is meant to be vague. | `>>wallet @person`
[Back To Top](#module-index)

### UTILITY
Commands | Description | Example
----------|-------------|--------
`>>avatar` `>>av` | Shows the mentioned user's avatar. If no user is mentioned, it shows the author's avatar. You can add "gif" to the end of the command to indicate that it's a gif. Or you can add "auto" to make the color strip the dominant color of the image. You can also add "static" to the end to make it return the full sized static version of your avatar. | `>>avatar @person`
`>>botinformation` `>>botinfo` `>>info` | Shows information about the bot, version, codename, authors, etc. | `>>botinformation`
`>>bots` | Lists the bots on the server where the command is used and shows their status. | `>>bots`
`>>channelid` `>>chid` `>>cid` | Shows the User ID of the mentioned channel. If no channel is mentioned, it will show the ID of the channel the command is used in. If you don't want the return message to be an embed, add "text" at the end. | `>>channelid #channel`
`>>channelinformation` `>>channelinfo` `>>chinfo` `>>cinfo` | Shows information and data about the mentioned channel. If no channel is mentioned, it will show data for the channel that the command is used in. | `>>channelinformation #channel`
`>>color` `>>colour` `>>clr` | Shows the inputted color. It accepts either a HEX code or an RGB array. | `>>color #1abc9c`
`>>convertcurrency` `>>convert` | Converts the amount of money inputed. The format of AMOUNT FROM_CURRENCY in TO_CURRENCY must be followed. | `>>convertcurrency 50 EUR in USD`
`>>emote` `>>emoji` `>>em` | Searches for an emoji by name. To make the search more precise you can add the ID of the emote or server that has that emote like in this example "lcMonika:200751504175398912". | `>>emote lcPain`
`>>ingame` | Shows the top played games on the server. | `>>ingame @person`
`>>lmgtfy` `>>letmegooglethatforyou` | Outputs a link that will google the query for you. | `>>lmgtfy Sexy Sneks`
`>>owners` | Shows a list of Sigma's owners. Users in this list have access to the administration module. | `>>owners`
`>>permissions` `>>perms` | Shows which permissions a user has and which they do not. If no user is mentioned, it will target the message author. | `>>permissions @person`
`>>roleinformation` `>>roleinfo` `>>rinfo` | Shows information and data about the inputted role. Roles mentions do not work here, lookup is done via role name. | `>>roleinformation`
`>>rolepopulation` `>>rolepop` | Shows the population of the inputted role. If no arguments are provided, it will show the top 20 roles by population. | `>>rolepopulation Warlard`
`>>servericon` `>>srvicon` `>>icon` | Shows the server's icon image. | `>>servericon`
`>>serverid` `>>guildid` `>>srvid` `>>sid` `>>gid` | Shows the Server ID of the server the command is used in. | `>>serverid`
`>>serverinformation` `>>serverinfo` `>>sinfo` | Shows information and data about the server that the command is used in. | `>>serverinformation`
`>>shortenurl` `>>shorten` `>>bitly` | Shortens a URL for you using BitLy. All URLs returned via Sigma are without ads, merely shortened using the service. | `>>shortenurl https://i.redd.it/ngwebbf5nwfz.jpg`
`>>statistics` `>>stats` | Shows Sigma's current statistics. Population, message and command counts, and rates since startup. As well as when the bot last started. | `>>statistics`
`>>status` | Shows the status of Sigma's machine. Processor information, memory, storage, network, etc. | `>>status`
`>>suggest` | Submits a suggestions to the owners of the bot to do stuff. Development and change wise. | `>>suggest Add some new stuff!!!`
`>>translation` `>>translate` `>>trans` | Translates a language from and to the given ones. If a conversion input is not stated, the first argument will be considered the input language. And the output will be in english. The language codes used abide by the ISO 639-1 format. For the whole list, you can go to this wikipedia article. https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes | `>>translation EN>JA Hello there!`
`>>userid` `>>uid` | Shows the User ID of the mentioned user. If no user is mentioned, it will show the author's ID. If you don't want the return message to be an embed, add "text" at the end. | `>>userid @person`
`>>userinformation` `>>userinfo` `>>uinfo` | Shows information and data about the mentioned user. If no user is mentioned, it will show data for the message author. | `>>userinformation @person`
`>>whoplays` | Generates a list of users playing the inputted game. | `>>whoplays Overwatch`
[Back To Top](#module-index)

### WARFRAME
Commands | Description | Example
----------|-------------|--------
`>>wfacolytechannel` `>>wfacolc` | Designates a channel for Warframe acolyte notifications. When an acolute is found it shows up there. To disable this, write disable after the command instead of a channel. | `>>wfacolytechannel #wf-acolytes`
`>>wfacolytes` `>>wfacol` | Shows data on the Stalker's acolytes. Their names, locations and health. | `>>wfacolytes`
`>>wfalertchannel` `>>wfac` | Designates a channel for Warframe alerts. When a new alert shows up the news will be posted there. To disable this, write disable after the command instead of a channel. | `>>wfalertchannel #wf-alerts`
`>>wfalerts` `>>wfa` | Shows the currently ongoing alerts in Warframe. As well as their respective rewards. | `>>wfalerts`
`>>wfbounties` `>>wfbounty` `>>wfjobs` `>>wfb` | Shows the rewards and mission information for the selected bounty tier. | `>>wfbounties 4`
`>>wffissurechannel` `>>wffc` | Designates a channel for Warframe void fissures. When a new void fissure shows up the news will be posted there. To disable this, write disable after the command instead of a channel. | `>>wffissurechannel #wf-fissures`
`>>wffissures` `>>wffissure` `>>wff` | Shows the current fissure locations in Warframe. As well as their tiers, locations and mission types. | `>>wffissures`
`>>wfinvasionchannel` `>>wfic` | Designates a channel for Warframe invasions. When a new invasion shows up the news will be posted there. To disable this, write disable after the command instead of a channel. | `>>wfinvasionchannel #wf-invasions`
`>>wfinvasions` `>>wfinvasion` `>>wfi` | Shows the current ongoing invasions in Warframe. As well as their factions, locations and rewards. | `>>wfinvasions`
`>>wfnews` `>>wfn` | Shows the current ative news in Warframe. | `>>wfnews`
`>>wfnewschannel` `>>wfnc` | Designates a channel for Warframe news. When Digital Extremes posts a new event for Warframe, it pops up there. To disable this, write disable after the command instead of a channel. | `>>wfnewschannel #wf-news`
`>>wfplainsofeidolon` `>>wfpoe` | Shows the current time on the Plains of Eidolon in warframe. As well as the next day/night cycle rotations. | `>>wfplainsofeidolon exact`
`>>wfpricecheck` `>>wfpc` `>>wfmarket` | Checks the price for the searched item. This will only list items by members that are currently online and in the game. The API requires a precise item name. | `>>wfpricecheck Blind Rage`
`>>wfsales` `>>wfsale` | Shows items that are currently on sale in Warframe's market. This list shows only items that have reduced prices by default. If you want it to list all promoted items regardless of reduction add "all" to the end of the command as in the example. The item list is also paginated. | `>>wfsales 2 all`
`>>wfsortie` `>>wfsorties` `>>wfs` | Shows the ongoing sortie missions in Warframe. | `>>wfsortie`
`>>wfsortiechannel` `>>wfsc` | Designates a channel for Warframe sorties. When a new sortie shows up the news will be posted there. To disable this, write disable after the command instead of a channel. | `>>wfsortiechannel #wf-sorties`
`>>wfsyndicates` `>>wfsyndicate` `>>wfsyndi` `>>wfsy` | Lists the best tradable offerings sold by each syndicate. Items with no current sell offers are listed first. Otherwise items are listed from most valuable to least valuable. This command is used to help you decide what to sell in case you have to much standing. For price checking refer to `wfpricecheck` aka. `wfpc` instead. | `>>wfsyndicates`
`>>wftag` `>>wftagrole` `>>wfnotify` `>>wfbind` | Binds a certain keyword from alerts and invasions. When this keyword appears during an event all roles bound to it's triggers will be mentioned. | `>>wftag aura Aura Squad`
`>>wftrials` `>>wftrial` `>>wfraids` `>>wfraid` `>>wft` `>>wfr` | Shows raid statistics for the inputted username. Note that DE hasn't been tracking this data forever. So some really old raids won't be shown due to having no data. The shortest raid time shown only counts victorious raids. | `>>wftrials AXAz0r`
`>>wfvoidtrader` `>>wfbarokiteer` `>>wfbaro` `>>baro` `>>wfvt` | Shows the items that Baro Ki'Teer is currently selling as well as the statistics such as total number of items, total amount of ducats and credits needed and where he's located. | `>>wfvoidtrader`
[Back To Top](#module-index)