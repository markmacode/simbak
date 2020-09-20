import os as _os

# SIMBAK_ENV:
#   normal
#   debug
SIMBAK_ENV = _os.getenv('SIMBAK_ENV', 'normal')
