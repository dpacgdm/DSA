def daily_temperatures(temps: list[int]) -> list[int]:
    n = len(temps)
    ans = [0]*n
    st = []
    for i,t in enumerate(temps):
        while st and temps[st[-1]] < t:
            j = st.pop()
            ans[j] = i - j
        st.append(i)
    return ans
