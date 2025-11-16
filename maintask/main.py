from SPtoml import TOML

TOML("/home/spring/Documents/projects/info_lab4/maintask/index.toml").auto_deserialization()
print(TOML("/home/spring/Documents/projects/info_lab4/maintask/index.toml").get_obj())