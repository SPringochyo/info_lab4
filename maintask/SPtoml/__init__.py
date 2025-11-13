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

    toml_obj = dict()

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

        command = ""

        for string in self.MAIN_LIST[:]:
            if (string[:2] == self.LEFT_SQARE_BRACKET * 2) and (string[-2:] == self.RIGHT_SQARE_BRACKET * 2):
                name = "self.toml_obj"

                if self.DOT not in string:

                    if ((name + f"['{string[2:-2]}']") in globals()) or (f"['{string[2:-2]}']" in eval(f"'{name}.keys()'")):
                        pass
                    else:
                        exec(f"{name}['{string[2:-2]}'] = dict()")

                    name += f"['{string[2:-2]}']"

                elif self.DOT in string:
                    lst = string[2:-2].split(self.DOT)

                    for i in range(len(lst)):

                        if ((name + f"['{lst[i]}']") in globals()) or (f"['{lst[i]}']" in eval(f"{name}").keys()):
                            continue
                        else:
                            exec(f"{name}['{lst[i]}'] = dict()")
                        name += f"['{lst[i]}']"

            else:
                i = string.find("=")
                exec(f"{name}[\"{string[:i]}\"] = {string[i+1:]}")


    def get_obj(self) -> str or dict:
        if not(self.toml_obj):
            raise ValueError("Объекта не существует, или объект пуст")
        return self.toml_obj
