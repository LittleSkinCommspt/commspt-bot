from graia.ariadne.message.parser.twilight import Match, RegexMatch


class KeywordsMatch(RegexMatch):
    pattern: str

    def __init__(self, pattern: str = '') -> None:
        super().__init__()
        multi_selection = '|'.join(pattern)
        self.pattern = rf'.*({multi_selection}).*'

    @property
    def _src(self) -> str:
        return self.pattern
