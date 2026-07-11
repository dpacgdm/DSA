def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    Trie={}
    for w in words:
        node=Trie
        for ch in w:
            node=node.setdefault(ch, {})
        node['$']=w
    R,C=len(board),len(board[0])
    out=[]
    def dfs(r,c,node):
        ch=board[r][c]
        nxt=node.get(ch)
        if not nxt:
            return
        word=nxt.pop('$', None)
        if word is not None:
            out.append(word)
        board[r][c]='#'
        for nr,nc in ((r+1,c),(r-1,c),(r,c+1),(r,c-1)):
            if 0<=nr<R and 0<=nc<C and board[nr][nc]!='#':
                dfs(nr,nc,nxt)
        board[r][c]=ch
        if not nxt:
            node.pop(ch, None)
    for i in range(R):
        for j in range(C):
            dfs(i,j,Trie)
    return out
