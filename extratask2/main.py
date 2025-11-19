# Запусти это в одном терминале, затем перейди в maintask
# и запусти там main в другом терминале, затем сравни

from tomllib import *

with open("index.toml", "rb") as file:
    print(load(file))
