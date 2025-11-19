import sys

sys.path.append("..")

from maintask.SPtoml import TOML
from maintask.SPxml import XML
from maintask.SPron import RON

okak = TOML("index.toml")
okak.auto_deserialization()

some_ron = RON("index.bin")
some_ron.write("okak_ron")
