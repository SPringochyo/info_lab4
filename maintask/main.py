from SPtoml import TOML
from SPxml import XML
from SPron import RON

TOML("index.toml").auto_deserialization()

some_xml = XML("index.bin")
some_xml.write("okak_xml")

some_ron = RON("index.bin")
some_ron.write("okak_ron")
