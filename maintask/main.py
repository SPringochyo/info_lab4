from SPtoml import TOML

In = TOML("/home/spring/Documents/projects/info_lab4/maintask/index.toml")
In.parse()
In.deserialization('obj.bin')

print(TOML.serialization('obj.bin'))
