# Linux Package Setup

This is a general setup guide for things that don't really need setting up.
More precisely, it's for things that are available as WYSIWYG packages.
You just install them via your prefered package manager, and that's it.

## Example

Let's take `git` and `ffmpeg` for example.

### Arch Linux

```sh
pacman -S git ffmpeg
```

*If you want to update your package mirror links,
the command is "`pacman -Sy`".
If you don't want to confirm stuff and just let it do its thing,
the argument is "`--noconfirm`".*

### Debian/Ubuntu

```sh
apt-get install gif ffmpeg
```

*If you want to update your package mirror links,
the command is "`apt-get update`".
If you don't want to confirm stuff and just let it do its thing,
the argument is "`-y`".*

### Fedora/CentOS

```sh
yum install git ffmpeg
```

*If you want to update your package mirror links,
the command is "`yum update`".
If you don't want to confirm stuff and just let it do its thing,
the argument is "`-y`".*
