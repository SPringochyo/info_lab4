class XML:

    _main_string = ""

    def __init__(self, filename: str = "") -> None:
        self.FILE_NAME = filename
        self._xml_obj = self.serialization(filename)


    def deserialization(self, filename) -> None:
        filename += ".bin"
        object = self._xml_obj

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
                if key == "text":
                    string += '    '*flag + obj[key] + "\n"
            elif type(obj[key]).__name__ == "dict":
                if "__" in key:
                    ky = key[:key.find("__")]
                    string += '    '*flag + f"<{ky}{self._attribute_create(obj[key])}>\n" + self._dict_write(obj[key], flag + 1) + '    '*flag + f"</{ky}>\n"
                else:
                    string += '    '*flag + f"<{key}{self._attribute_create(obj[key])}>\n" + self._dict_write(obj[key], flag + 1) + '    '*flag + f"</{key}>\n"
            elif type(obj[key]).__name__ == "list":
                string += '    '*flag + f"<{key}{self._attribute_create(obj[key][0])}>\n" + self._list_write(obj[key], flag + 1) + '    '*flag + f"</{key}>\n"

        return string


    def _attribute_create(self, obj) -> str:
        out = list()
        for key in obj.keys():
            if key != "text" and type(obj[key]).__name__ == "str":
                out.append(f"{key}=\"{obj[key]}\"")

        return " " + " ".join(out) if out else " ".join(out)


    def _list_write(self, obj, flag = 1) -> str:
        string = ''

        for dct in obj:
            string += self._dict_write(dct, flag)

        return string


    def write(self, filename) -> None:
        filename += ".xml"
        with open(filename, "a+") as file:
            file.write("<xml>\n")
            file.write(self._dict_write(self._xml_obj))
            file.write("</xml>")


    def get_obj(self) -> dict:
        if not(self._xml_obj):
            raise ValueError("Объекта не существует, или объект пуст")
        return self._xml_obj
