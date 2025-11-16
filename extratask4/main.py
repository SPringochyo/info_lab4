import time

from SPtoml import TOML
from SPxml import XML
from SPron import RON

start_time = time.time()

for i in range(100):

    TOML("index.toml").auto_deserialization()

    some_xml = XML("index.bin")
    some_xml.write("okak_xml")

    some_ron = RON("index.bin")
    some_ron.write("okak_ron")

end_time = time.time()
execution_time = end_time - start_time  
print(f"Затрачено времени: {execution_time} сек")