# Core

The core consists of 4 configuration files controlling
various parameters and information. Stuff like Discord authentication, 
database and cache connection information, etc.
These files are `cache.yml` , `database.yml` , `discord.yml`

and `preferences.yml` .

## Examples

### discord.yml

```yml
bot:    true
token: '72b302bf297a228a75730123efef7c41'
owners:
  - 137951917644054529
  - 125750263687413760
  - 217078934976724992
  - 208974392644861952
```

### database.yml

```yml
database: sigma
auth:     false
host:    'localhost'
port:     27017
username: null
password: null
```

### cache.yml

```yml
type: 'memory'
time: 60
size: 10000
host: 'localhost'
port: 6379
```

### preferences.yml

```yml
dev_mode:         false
status_rotation:  true
text_only:        false
music_only:       false
prefix:           '>>'
currency:         'Kud'
currency_icon:    '⚜️'
website:          'https://luciascipher.com/sigma'
syslog_channel:   123456789123456789
movelog_channel:  123456789123456789
errorlog_channel: 123456789123456789
key_to_my_heart:  'how_about_no'
```
