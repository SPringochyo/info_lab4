class TOML:

    def __init__(self, filename: str = "") -> None:
        self.FILE_NAME = filename


    LEFT_SQARE_BRACKET = "["
    RIGHT_SQARE_BRACKET = "]"
    LEFT_CURLY_BRACE = "{"
    RIGHT_CURLY_BRACE = "}"
    EQUAL_SIGN = " = "
    QUOTATION_MARK = '"'
    COMMA = ", "
    END_OF_LINE = "\n"


    def _make_key_value_pair(self, key : str, value : str) -> str:
        return key + self.EQUAL_SIGN + self.QUOTATION_MARK + value + self.QUOTATION_MARK


    def _make_table_name(self, table_name : str) -> str:
        return self.LEFT_SQARE_BRACKET + table_name + self.RIGHT_SQARE_BRACKET
