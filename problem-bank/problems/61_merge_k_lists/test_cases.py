CASES = []
def _to_list(node):
    out=[]
    while node:
        out.append(node.val); node=node.next
    return out
def _from(vals, sol):
    dummy=sol.ListNode(0); c=dummy
    for v in vals:
        c.next=sol.ListNode(v); c=c.next
    return dummy.next
def t1(sol):
    lists=[_from([1,4,5],sol), _from([1,3,4],sol), _from([2,6],sol)]
    assert _to_list(sol.merge_k_lists(lists))==[1,1,2,3,4,4,5,6]
def t2(sol):
    assert sol.merge_k_lists([]) is None
def t3(sol):
    assert sol.merge_k_lists([None]) is None
TESTS=[t1,t2,t3]
