# Simbak

Simbak is a simple backup solution that is aimed towards individuals who just want a quick and easy way to backup their files. Backups are stored as `tar.gz` files, so there is no dependence on any application to restore you backups.

# Benefits of simbak

- Simbak uses tar and gzip in order to store the backups, so that recovering the data in backups does not depend on simbak itself.
- Simbak is also very light, portable, and very easy to use, meaning that there's no large application to install.
- It's free and open source, meaning anyone can contribute or change simbak to meet their own needs.

# Getting started

**Note:** This is in early development and changes to the API may be frequent. This project uses [semantic versioning](https://semver.org). The format of versions are `{major}.{minor}.{patch}`, so so while we are at version `0.x.x` *assume* that each minor release has API changes. 

## Installation
To install simbak you can simple use [pip](https://pypi.org/project/pip/).

```bash
$ pip install simbak
```

## Using simbak

### Command line

You can use simbak in many ways, the fastest way would be to use the `simbak` command in the terminal directly.

```bash
$ simbak [...]
```

You can also use the simbak module itself through the python executable.

```bash
$ python3 -m simbak [...]
```

### In Python

You can use simbak within your own python code, and you can make python scripts to use simbak (a python script is prettier than shell script).

```python
from simbak import backup

backup.backup(...)
```

### Example usages

Each of these examples will achieve the same reults. They will create a backup of `/home/projects/my_project/` and `/home/docs/important.txt` and it will store the backup in `/backups/backups` and `/local/backups`. The backup will be a `tar.gz` file and it will have the name of `important--yyyy-mm-dd--hh-mm-ss`, the time is stamped at the end of the backup to ensure the file is unique and not conflicting with other backups.

#### Python script example

```python
# backup.py

from simbak import backup

backup.backup(
    sources=[
        "/home/projects/my_project/",
        "/home/docs/important.txt",
    ],
    destinations=[
        "/local/backups/",
        "/remote/backups/",
    ],
    name="important"
)
```

You can then run this script through the terminal using  `$ python backup.py`.

#### Bash script example

**Note**: I am using a backslash at the end of each line in order to have a command spread across multiple lines, this helps readability.

```bash
# backup.bash

simbak \
    --source \
        "/home/projects/my_project/" \
        "/home/docs/important.txt" \
    --destination \
        "/local/backups/" \
        "/remote/backups/" \
    --name "important"
```

#### Terminal

Using simbak directly in the terminal isn't recommended unless you are backing up one directory or file to one location, as you can see the lines can get quite long.

```bash
$ simbak -s "/home/projects/my_project/" "/home/docs/important.txt" -d "/local/backups/" "/remote/backups/" --name "important"
```
