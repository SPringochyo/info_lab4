from SPtoml import TOML
from SPxml import XML
from SPron import RON

okak = TOML("index.toml")
okak.auto_deserialization()
print(okak.get_obj())
