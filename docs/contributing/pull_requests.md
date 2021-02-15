# Submitting a Pull Request

## Formatting

Make sure that your code is formatted according to [PEP8](https://www.python.org/dev/peps/pep-0008/).

Your Editor/IDE probably comes with a linter installed or has plugins for linting available.

You can also use a CLI tool like `flake8` to manually lint your code.

## Commit Messages

Keep your commit messages short and informative. You can add a more comprehensive description below the commit message.

Things to **not** include in your commit message:

* `@tag` team or username references
* `#ref` issue or pull request references

Never include `[ci skip]` or similar to skip CI. Pull requests skipping any kind of CI will be ignored.

Check out this [article](https://chris.beams.io/posts/git-commit) if you want to know why good commit messages matter.
