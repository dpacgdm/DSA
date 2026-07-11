CASES=[]
def t1(sol):
    board=[["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
    got=sorted(sol.find_words(board, ["oath","pea","eat","rain"]))
    assert got==["eat","oath"]
def t2(sol):
    assert sol.find_words([["a"]], ["a"])==["a"]
TESTS=[t1,t2]
