from typing import List

from graia.application.message.parser.signature import NormalMatch


class KeywordsMatch(NormalMatch):
    pattern: str

    def __init__(self, pattern) -> None:
        multi_selection = '|'.join(pattern)
        super().__init__(pattern=rf'.*({multi_selection}).*')

    def operator(self):
        return self.pattern


class CommandMatch(NormalMatch):
    pattern: str

    def __init__(self, pattern, with_params: bool = True) -> None:
        re_pattern = rf'(.*: )?&{pattern}[^\.] *' if with_params else rf'(.*: )?&{pattern}'
        super().__init__(pattern=re_pattern)

    def operator(self):
        return self.pattern
