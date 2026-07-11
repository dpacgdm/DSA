def count_primes(n: int) -> int:
    if n <= 2:
        return 0
    is_p = [True]*n
    is_p[0] = is_p[1] = False
    p = 2
    while p*p < n:
        if is_p[p]:
            step = p
            start = p*p
            is_p[start:n:step] = [False]*len(range(start, n, step))
        p += 1
    return sum(is_p)
