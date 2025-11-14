class TOML:

    LEFT_SQARE_BRACKET = "["
    RIGHT_SQARE_BRACKET = "]"
    LEFT_CURLY_BRACE = "{"
    RIGHT_CURLY_BRACE = "}"
    EQUAL_SIGN = " = "
    QUOTATION_MARK = '"'
    COMMA = ", "
    DOT = "."
    END_OF_LINE = "\n"

    _toml_obj = dict()

    def __init__(self, filename: str = "") -> None:
        self.FILE_NAME = filename
        self.MAIN_LIST = self._convert_to_list()


    def _convert_to_list(self) -> list[str]:
        with open(self.FILE_NAME, "r") as file:

            lst = []
            for s in file.readlines():
                if s.strip():
                    lst.append(s.strip().replace(self.EQUAL_SIGN, "="))

        return lst


    def parse(self) -> None:

        for string in self.MAIN_LIST[:]:
            if (string[0] == self.LEFT_SQARE_BRACKET) and (string[-1] == self.RIGHT_SQARE_BRACKET):
                name = "self._toml_obj"

                if self.DOT not in string:
                    if ((name + f"['{string[1:-1]}']") in globals()) or (f"['{string[1:-1]}']" in eval(f"'{name}.keys()'")):
                        pass
                    else:
                        exec(f"{name}['{string[1:-1]}'] = dict()")
                    name += f"['{string[1:-1]}']"

                elif self.DOT in string:
                    lst = string[1:-1].split(self.DOT)

                    for i in range(len(lst)):
                        if ((name + f"['{lst[i]}']") in globals()) or (f"['{lst[i]}']" in eval(f"{name}").keys()):
                            continue
                        else:
                            exec(f"{name}['{lst[i]}'] = dict()")
                        name += f"['{lst[i]}']"
            else:
                i = string.find("=")
                exec(f"{name}[\"{string[:i]}\"] = {string[i+1:]}")


    def deserialization(self, filename) -> None:
        filename += ".bin"
        object = self._toml_obj

        with open(filename, 'wb') as file:
            obj_str = str(object)
            obj_bytes = obj_str.encode('utf-8')
            file.write(len(obj_bytes).to_bytes(8, byteorder='little'))
            file.write(obj_bytes)


    def auto_deserialization(self) -> None:
        filename = self.FILE_NAME[:self.FILE_NAME.rfind(".")]
        self.parse()
        self.deserialization(filename)


    def serialization(filename) -> dict:
        with open(filename, 'rb') as file:
            data_len = int.from_bytes(file.read(8), byteorder='little')
            obj_bytes = file.read(data_len)
            obj_str = obj_bytes.decode('utf-8')

        return eval(obj_str)


    def get_obj(self) -> dict:
        if not(self._toml_obj):
            raise ValueError("Объекта не существует, или объект пуст")
        return self._toml_obj
