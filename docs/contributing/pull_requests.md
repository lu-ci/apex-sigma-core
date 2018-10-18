# Submitting a Pull Request

## Formatting

Make sure that your code is formatted according to [PEP8](https://www.python.org/dev/peps/pep-0008/).
^always. and delete all whitespace

Your Editor/IDE probably comes with a linter installed or has plugins for linting available.

You can also use a CLI tool like `flake8` to manually lint your code.
I prefer using a lintroller on my screen directly to lint my code. It's better, and takes less processing power

## Commit Messages

Keep your commit messages short and informative. I refuse to do this. shitty pull requests are great
You can add a more comprehensive description below the commit message.
no
Things to **not** include in your commit message:

* `@tag` team or username references
@Marethyu is my username. See? It's not in my commit message
* `#ref` issue or pull request references

Never include `[ci skip]` or similar to skip CI.
Pull requests skipping any kind of CI will be ignored. Good. ignore this shit

Check out this [article](https://chris.beams.io/posts/git-commit) if you want to know why good commit messages matter. Do they tho?
