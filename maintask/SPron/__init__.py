class RON:

    _main_string = ""

    def __init__(self, filename: str = "") -> None:
        self.FILE_NAME = filename
        self._ron_obj = self.serialization(filename)


    def deserialization(self, filename) -> None:
        filename += ".bin"
        object = self._ron_obj

        with open(filename, 'wb') as file:
            obj_str = str(object)
            obj_bytes = obj_str.encode('utf-8')
            file.write(len(obj_bytes).to_bytes(8, byteorder='little'))
            file.write(obj_bytes)


    def serialization(self, filename) -> dict:
        with open(filename, 'rb') as file:
            data_len = int.from_bytes(file.read(8), byteorder='little')
            obj_bytes = file.read(data_len)
            obj_str = obj_bytes.decode('utf-8')

        return eval(obj_str)


    def _dict_write(self, obj, flag = 1) -> str:
        string = ''

        for key in obj.keys():
            if type(obj[key]).__name__ == "str":
                string += '    '*flag + key + ": " + '"' + obj[key] + '"' + ",\n"
            elif type(obj[key]).__name__ == "dict":
                string += '    '*flag + key + ": (\n" + self._dict_write(obj[key], flag + 1) + '    '*flag + "),\n"
            elif type(obj[key]).__name__ == "list":
                string += '    '*flag + key + ": [\n" + self._list_write(obj[key], flag + 1) + '    '*flag + "],\n"

        return string


    def _list_write(self, obj, flag = 1) -> str:
        string = ''

        for dct in obj:
            string += '    '*flag + "(\n" + self._dict_write(dct, flag + 1) + '    '*flag + "),\n"

        return string


    def write(self, filename) -> None:
        filename += ".ron"
        with open(filename, "a+") as file:
            file.write("RON(\n")
            file.write(self._dict_write(self._ron_obj))
            file.write(")")


    def get_obj(self) -> dict:
        if not(self._ron_obj):
            raise ValueError("Объекта не существует, или объект пуст")
        return self._ron_obj
