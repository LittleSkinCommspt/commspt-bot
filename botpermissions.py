from typing import List

class groupPermissions(object):
    '''处理 `Member` 的权限'''
    adminsList = 'admins.list'
    blockusersList = 'blockusers.list'

    qq: int

    def __init__(self, qq: int):
        '''检查用户权限或进行权限操作
        
        :params qq: QQ 号'''
        self.qq = qq

    def _readBlockList(self) -> List[int]:
        with open(self.blockusersList, 'r+') as f:
            return [int(_i) for _i in f.read().split()]

    def _writeBlockList(self, l: list) -> None:
        _l = [str(_i) for _i in l]
        with open(self.blockusersList, 'w+') as f:
            f.writelines([f'{_i}\n' for _i in _l])

    def _readAdminList(self) -> List[int]:
        with open(self.adminsList, 'r+') as f:
            _l = [int(_i) for _i in f.read().split()]
        return _l

    def isAdmin(self) -> bool:
        '''是否为 admin'''
        return self.qq in self._readAdminList()

    def isBlocked(self) -> bool:
        '''是否已被 block'''
        _l = self._readBlockList()
        return self.qq in _l

    def blockme(self) -> bool:
        '''封禁自己
        
        成功 True
        
        :params userId: 被封禁对象的 QQ'''
        _l = self._readBlockList()
        if self.qq in _l:  # 用户已被 block
            return False
        else:
            _l.append(self.qq)
            self._writeBlockList(_l)
            return True

    def unblockme(self) -> bool:
        '''解除自己的封禁
        
        成功 True
        
        :params userId: 被解除封禁的对象的 QQ'''
        _l = self._readBlockList()
        if not self.qq in _l:  # 用户没被 block
            return False
        else:
            del _l[_l.index(self.qq)]
            self._writeBlockList(_l)
            return True

