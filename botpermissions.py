class groupPermissions():
    adminsList = 'admins.list'
    blockusersList = 'blockusers.list'

    def __init__(self, qq: int):
        '''检查用户权限或进行权限操作
        
        :params qq: QQ 号'''
        self.qq = qq

    def _readBlockList(self) -> list:
        with open(self.blockusersList, 'r+') as f:
            return [int(_i) for _i in f.read().split()]

    def _writeBlockList(self, l: list):
        with open(self.blockusersList, 'w+') as f:
            f.writelines([str(_i) for _i in l])

    def isAdmin(self) -> bool:
        '''是否为 admin'''
        with open(self.adminsList, 'r+') as f:
            _l = [int(_i) for _i in f.read().split()]
        return self.qq in _l

    def isBlocked(self) -> bool:
        '''是否已被 block'''
        with open(self.blockusersList, 'r+') as f:
            _l = [int(_i) for _i in f.read().split()]
        return self.qq in _l

    def block(self, userId: int) -> bool:
        '''封禁 userId
        
        成功 True
        
        :params userId: 被封禁对象的 QQ'''
        _l = self._readBlockList()
        if userId in _l:  # 用户已被 block
            return False
        else:
            self._writeBlockList(_l.append(userId))
            return True

    def unblock(self, userId: int) -> bool:
        '''解除 userId 的封禁
        
        成功 True
        
        :params userId: 被解除封禁的对象的 QQ'''
        _l = self._readBlockList()
        if not userId in _l:  # 用户没被 block
            return False
        else:
            del _l[_l.index(userId)]
            self._writeBlockList(_l)
            return True

