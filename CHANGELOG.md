# v0.4.0
- The log file path can now be specified.
- File logging is no longer done by default, it is optional.

# v0.3.1
- Hotfix, added dependent package (`python-dotenv`) to the installation.

# v0.3.0
- Improved logging once again.
- Added a Rotating Agent. This agent will do rotating backups up to a
"rotate limit" once the rotate limit is exceeded, it will remove the
oldest backup of that specified rotating backup spec.
- Plenty of housekeeping and bug fixes.

# v0.2.1
- Improved logging messages slightly.
- Will now log messages to files to the following locations.
    - Windows `%APPDATA%\simbak\` or `C:\Program Data\simbak\`
    - Linux `/var/log/simbak/`

# v0.2.0
- Removed `simbak/backup.py` module.
    - It contained only one public method `simbak.backup.backup()`, and
    wasn’t able to scale well.
    - Moved the one public method to `simbak/__init__.py` so that the
    method signature is smaller `simbak.backup()`
    - This can be the one and only quick backup method to use, which
    will perform a standard backup. It should meet the needs for most
    people, and keeps it simple. Other more complex backup solutions
    will be in the new `simbak/backup` package.
- There are now backup 'agents', which will perform different backups,
for now there is only a `NormalAgent`.
- Added unit tests.

# v0.1.2
- Critical error with logging fixed, logging should now work normally.

# v0.1.1
- Improved logging.
    - Added messages to make it more clear what simbak is doing.
    - Log files are now stored.
- Established that we are using semantic versioning.

# v0.1.0
- Completed the readme (for now).
- Cleaned the imports of simbak so that it's clear what the public API
is.
- Simbak can now be called from the command line as an executable like:
`simbak ...`
- Fixed an issue where setup.py didn't actually package simbak itself.

# v0.0.1
- We're here.