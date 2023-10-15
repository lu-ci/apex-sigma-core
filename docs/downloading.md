# Downloading and Updating

Before we do anything, we need Sigma's repository which contains all her code.
If you installed Git, which was optional above, use the "Git" section,
otherwise the "Manual" one.

## Manual

You can download the entire repository
from [here](https://gitlab.com/lu-ci/sigma/apex-sigma/-/archive/master/apex-sigma-master.zip) as a ZIP file.
Once it's done downloading just extract it to where you want Sigma's files to be.

Updating manually is crude, you re-download the ZIP above and overwrite the
entire directory where Sigma's files are.

## Git

Open the location where you want to clone Sigma's repository in a terminal.
And hit the good old clone command with her repository [URI](https://gitlab.com/lu-ci/sigma/apex-sigma.git).

```
git clone https://gitlab.com/lu-ci/sigma/apex-sigma.git
```

Updating with git pretty much works the same,
except you don't need to clone it again,
you just run the following from Sigma's directory.

```
git pull
```

Easy, huh?

Neither of these touch your configuration or data.
The configuration files are not a part of the repository,
and the data is stored in the database.