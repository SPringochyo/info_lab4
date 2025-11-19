import time
import sys
import dict2xml

sys.path.append("..")

from tomllib import *

from maintask.SPtoml import TOML
from maintask.SPxml import XML
from maintask.SPron import RON

start_time = time.time()

for i in range(100):
    TOML("index.toml").auto_deserialization()

    some_xml = XML("index.bin")
    some_xml.write("okak_xml")

    some_ron = RON("index.bin")
    some_ron.write("okak_ron")

end_time = time.time()
execution_time = end_time - start_time
print(f"Затрачено времени самописными модулями: {execution_time} сек")


start_time2 = time.time()

for i in range(100):
    with open("index.toml", "rb") as file:
        mdo = load(file)
        dict2xml.dict2xml(mdo)
        
end_time2 = time.time()
execution_time2 = end_time2 - start_time2
print(f"Затрачено времени импортированными модулями: {execution_time2} сек")