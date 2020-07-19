from mirai import MessageChain, Plain, Source


def getAll(l: list):
    text = ''
    for _i in l:
        i_text = _i.text
        if _i.text.strip() != '':
            text = f'{text} {i_text}'
    return text.strip()


def getQuote(l: list):
    i_l = list()
    for _i in l:
        if isinstance(_i, Plain):
            i_l.append(_i)
    return getAll(i_l)
