import sys

sys.path.append("..")

from maintask.SPtoml import TOML
from maintask.SPxml import XML
from maintask.SPron import RON

okak = TOML("index.toml")
okak.auto_deserialization()
print(okak.get_obj())

some_xml = XML("index.bin")
some_xml.write("okak_xml")
