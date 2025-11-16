from SPtoml import TOML
from SPxml import XML

TOML("/home/spring/Documents/projects/info_lab4/maintask/index.toml").auto_deserialization()
some = XML("/home/spring/Documents/projects/info_lab4/maintask/index.bin")
some.write("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
print(some.get_obj())
