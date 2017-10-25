# Discord Application Creation

To have a Discord bot, you need to be a registered Discord user.
This guide will show you how to create an official Discord application, and get
the required credentials for setting Sigma up.

## Creating A New Application

Go ahead and open up the Discord application page
[here](https://discordapp.com/developers/applications/me).
You'll find a pretty barren place if you've not done this before,
that looks kind of like this.

![My Apps Empty Image](https://i.imgur.com/htTN9AL.png)

Click that big **New App** button/filed, and a new page should open up.
It's time to fill in details about your application.

![Application Details Empty Image](https://i.imgur.com/6QNP1eb.png)

The only required field is the name, and don't worry, everything is changeable.
You can name it whatever you want to name it as.
For example, I set up a new application like this.

![Application Details Filled Image](https://i.imgur.com/f5hJK0U.png)

When you are satisfied, smack that **Create App** button.
You will be taken to a new page now that looks like this.

![Application Page Image](https://i.imgur.com/dp2sIig.png)

We need to tell Discord that, yes, this is a Bot we are making.
So press the **Create a Bot User** button.
A pop-up will appear asking if you are sure.
You are indeed sure, so press **Yes, do it!**.
The page will change with new details now and will look like this.

![Application Bot Page Image](https://i.imgur.com/NAzVJZp.png)

Let's explain some of these things before we continue.
You'll see a **Public Bot** and **Require OAuth2 Code Grant** checkboxes.
The first toggles if other people are able to add your bot to their servers freely.
The second is an advanced option for developers, we suggest keeping it off.
If it is on, you might not be able to add the bot to any server.

**Don't forget to hit the `Save Changes` button on the bottom right!**

## Getting The Needed Credentials

From the page of your application, you are going to need a few details.
Mainly the application's **Client ID** and **Token**.
Because this happens a lot,
please note that the `Token` is **not** the `Client Secret`!

And before we continue, while the Client ID is public at all times,
you should **never give your token to anyone**.

In your applications details, you should clearly see both the ID.
With the exception of the Token that has a `click to reveal` text.
Click that to see your token. It will appear like in the example image.

![Application Credentials Image](https://i.imgur.com/Ef4IUZg.png)
*(Don't worry, this is just an example and the credentials here are invalid.)*

Write those down somewhere, for example I'd put them in a notepad for the time being.
You'll need the Client ID for the next section, and the Token for the
[configuration](https://sigma.readthedocs.io/en/latest/configuration/core/).

```yml
ID: 353367205146001420
Token: MzUzMzY3MjA1MTQ2MDAxNDIw.DIuq0Q.Me4j6mufIPy_0XJh-JlRgRZ7864
```

If you have made any, save changes.
Now that you have the credentials needed, keep them handy.

## Inviting The Bot

To invite the bot to a server you need an invite link.
An invite link is created with a simple template and the bot's Client ID.


* Template: `https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID_GOES_HERE&scope=bot`
* Example: `https://discordapp.com/oauth2/authorize?client_id=353367205146001420&scope=bot`

Open the link you've made in your browser and a page like this will appear.

![Invite Page Image](https://i.imgur.com/3jWMs0h.png)

Select a server that you want to invite the bot to from the dropdown list.
And press that **Authorize** button.

**You're all set, the bot should be on your server now!**
