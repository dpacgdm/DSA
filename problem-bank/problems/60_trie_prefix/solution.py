def exist(board: list[list[str]], word: str) -> bool:
    R, C = len(board), len(board[0])
    def dfs(r,c,k):
        if k == len(word):
            return True
        if r<0 or c<0 or r>=R or c>=C or board[r][c] != word[k]:
            return False
        tmp = board[r][c]
        board[r][c] = '#'
        ok = dfs(r+1,c,k+1) or dfs(r-1,c,k+1) or dfs(r,c+1,k+1) or dfs(r,c-1,k+1)
        board[r][c] = tmp
        return ok
    for i in range(R):
        for j in range(C):
            if dfs(i,j,0):
                return True
    return False
