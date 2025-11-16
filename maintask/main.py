from SPtoml import TOML
from SPron import RON

TOML("/home/spring/Documents/projects/info_lab4/maintask/test.toml").auto_deserialization()
some = RON("/home/spring/Documents/projects/info_lab4/maintask/test.bin")
some.write("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
