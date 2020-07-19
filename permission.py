def check(senderqq: int):
    with open('admins.list', 'r+') as f:
        l = [int(i) for i in f.read().split()]
    return senderqq in l

def _read_block():
    with open('blockusers.list', 'r+') as f:
        return [int(i) for i in f.read().split()]

def _write_block(l: list):
    with open('blockusers.list', 'w+') as f:
        f.writelines([str(i) for i in l])

def blockuser(userqq: int):
    l = _read_block()
    if userqq in l:
        return False
    else:
        l.append(userqq)
        _write_block(l)
        return True


def allowuser(userqq: int):
    l = _read_block()
    if not userqq in l:
        return False
    else:
        del l[l.index(userqq)]
        _write_block(l)
        return True


def isblocked(senderqq: int):
    with open('blockusers.list', 'r+') as f:
        l = [int(i) for i in f.read().split()]
    return senderqq in l
