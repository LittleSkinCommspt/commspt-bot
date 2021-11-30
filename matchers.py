from typing import List

from graia.ariadne.message.parser.twilight import RegexMatch


class KeywordsMatch(RegexMatch):
    pattern: str

    def __init__(self, pattern) -> None:
        multi_selection = '|'.join(pattern)
        super().__init__(pattern=rf'.*({multi_selection}).*')


class CommandMatch(RegexMatch):
    pattern: str

    def __init__(self, pattern, with_params: bool = True) -> None:
        re_pattern = rf'(.*: )?&{pattern}[^\.] *' if with_params else rf'(.*: )?&{pattern}'
        super().__init__(pattern=re_pattern)
