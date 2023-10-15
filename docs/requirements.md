# Requirements

*\* - Requirements marked with an asterisk are completely optional
but impact some functionality or make handling, updating, etc. much easier.*

## You

What you need to work with this guide.
From downloading Sigma herself to being able to edit configuration files.

| Requirement      | Ver. | Rec.    | Guides                                                                                                                                          |
------------------|------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------
| Git*             | \*   | >= 2.30 | [Linux](../setup/linux/package) - [Windows](../setup/windows/git)                                                                               |
| UTF-8 Editor     | \*   | VSCode  | -                                                                                                                                               |
| Beer/Coffee/Tea* | \*   | Lots    | [Beer](https://www.wikihow.com/Drink-Beer) - [Coffee](https://www.wikihow.com/Start-Drinking-Coffee) - [Tea](https://www.wikihow.com/Drink-Tea) |

## Sigma

What Sigma needs in order to run in any amount.

| Requirement      | Ver.   | Rec.          | Guides                                                               |
------------------|--------|---------------|----------------------------------------------------------------------
| Python           | >= 3.6 | >= 3.9        | [Linux](../setup/linux/python) - [Windows](../setup/windows/python)  |
| MongoDB          | >= 4.0 | >= 4.4        | [Linux](../setup/linux/mongo) - [Windows](../setup/windows/mongo)    |
| FFMPEG*          | \*     | >= 2021.\*.\* | [Linux](../setup/linux/package) - [Windows](../setup/windows/ffmpeg) |
| MSVC Build Tools | \*     | \*            | [Windows](../setup/windows/msvc)                                     

Done with all that? Then let's start the easy but tedious parts.
You are expected to have knowledge on how to use a terminal/command line.
It's the absolute bare minimum and without that there's no going forward.

## Details

### Git

A tool used for repository management,
makes downloading and updating Sigma's code easier.

### UTF-8 Editor

UTF-8 is an encoding type for text files,
you need something that can read and write these without making a mess.
Pretty much any text editor works that's meant for code.
Notepad++, Atom, Visual Studio Code, etc.

### Beer/Coffee/Tea

I'm not explaining this.

### Python

Python is an interpreted language, not a compiled one,
so you need an interpretor, which is python's software package.
Without it you can't run any of Sigma's code.

### MongoDB

This is a database, it's where Sigma will store all the data she needs.
Settings, wallets, profiles, etc. Everything goes here.

### FFMPEG

Media encoding library. Used for Sigma's music functions.
Sigma can run without it but will not have music functionality.

### MSVC Build Tools

You only need these on Windows.
Some pip packages that Sigma requires need to be compiled.
To do that, you need Build Tools.
Don't blame me, you chose to run this on Windows...
