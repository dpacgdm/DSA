CASES = []

def _ser_tuple(r):
    if not r:
        return None
    return (r.val, _ser_tuple(r.left), _ser_tuple(r.right))

def t1(sol):
    TN = sol.TreeNode
    r = TN(1, TN(2), TN(3, TN(4), TN(5)))
    c = sol.Codec()
    assert _ser_tuple(c.deserialize(c.serialize(r))) == _ser_tuple(r)

def t2(sol):
    c = sol.Codec()
    assert c.deserialize(c.serialize(None)) is None

TESTS = [t1, t2]
