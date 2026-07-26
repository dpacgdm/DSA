def simplify_path(path: str) -> str:
    stack = []
    for tok in path.split('/'):
        if tok == '' or tok == '.':
            continue
        if tok == '..':
            if stack:
                stack.pop()
        else:
            stack.append(tok)
    return '/' + '/'.join(stack)
