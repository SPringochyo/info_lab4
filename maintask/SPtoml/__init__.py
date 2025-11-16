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

    SQ_BRACES = [LEFT_SQARE_BRACKET, RIGHT_SQARE_BRACKET]
    CR_BRACES = [LEFT_CURLY_BRACE, RIGHT_CURLY_BRACE]
    BRACES = SQ_BRACES + CR_BRACES

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


    def _array_of_tables(self, string, name) -> str:
        name = "self._toml_obj"
        lst = string[2:-2].split(self.DOT)

        for i in range(len(lst)):
            if lst[i] in eval(name).keys():
                if i == (len(lst) - 1):
                    eval(name)[lst[i]].append(dict())
            else:
                if i == (len(lst) - 1):
                    eval(name)[lst[i]] = list()
                    eval(name)[lst[i]].append(dict())
                else:
                    if type(eval(name)).__name__ == "dict":
                        eval(name)[lst[i]] = dict()
                    elif type(eval(name)).__name__ == "list":
                        eval(name)[lst[i]].append(dict())

            if type(eval(name)[lst[i]]).__name__ == "dict":
                name += f"['{lst[i]}']"
            elif type(eval(name)[lst[i]]).__name__ == "list":
                name += f"['{lst[i]}'][-1]"

        return name


    def _table(self, string, name) -> str:
        name = "self._toml_obj"
        lst = string[1:-1].split(self.DOT)

        for i in range(len(lst)):
            if lst[i] in eval(name).keys():
                pass
            else:
                if i == (len(lst) - 1):
                    eval(name)[lst[i]] = dict()
                else:
                    if type(eval(name)).__name__ == "dict":
                        eval(name)[lst[i]] = dict()
                    elif type(eval(name)).__name__ == "list":
                        pass

            if type(eval(name)[lst[i]]).__name__ == "dict":
                name += f"['{lst[i]}']"
            elif type(eval(name)[lst[i]]).__name__ == "list":
                name += f"['{lst[i]}'][-1]"

        return name


    def _key_value(self, string, name) -> None:
        i = string.find("=")
        exec(f"{name}[\'{string[:i]}\'] = {string[i+1:]}")


    def _key_value_create(self, string) -> dict:
        lst = [line.strip() for line in string.split(',')]
        out = dict()

        for line in lst:
            i = line.find("=")
            out[line[:i]] = line[i+1:].replace('"', '')

        return out


    def _inline_table(self, string, name) -> None:
        i = string.find("=")
        exec(f"{name}[\'{string[:i]}\'] = {self._key_value_create(string[i+2:-1])}")


    def _type_def(self, string, name) -> None:
        if ((string[:2] == self.LEFT_SQARE_BRACKET * 2) and
            (string[-2:] == self.RIGHT_SQARE_BRACKET * 2) and
            (string.count(self.LEFT_SQARE_BRACKET) == string.count(self.RIGHT_SQARE_BRACKET) == 2)):

            name = self._array_of_tables(string, name)

        elif ((string[0] == self.LEFT_SQARE_BRACKET) and
              (string[-1] == self.RIGHT_SQARE_BRACKET) and
              (string.count(self.LEFT_SQARE_BRACKET) == string.count(self.RIGHT_SQARE_BRACKET) == 1)):

            name = self._table(string, name)

        elif ((string[0] not in self.BRACES) and
              (string[-1] not in self.BRACES) and
              (self.EQUAL_SIGN.strip() in string) and
              (self.QUOTATION_MARK in string)):

            self._key_value(string, name)

        elif ((string[0] not in self.SQ_BRACES) and
              (string[-1] not in self.SQ_BRACES) and
              (self.EQUAL_SIGN.strip() in string)):

            self._inline_table(string, name)

        return name


    def parse(self) -> None:
        name = "self._toml_obj"

        for string in self.MAIN_LIST[:]:
            name = self._type_def(string, name)


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
