from SPtoml import TOML

TOML("/home/spring/Documents/projects/info_lab4/maintask/test.toml").auto_deserialization()
print(TOML("/home/spring/Documents/projects/info_lab4/maintask/test.toml").get_obj())