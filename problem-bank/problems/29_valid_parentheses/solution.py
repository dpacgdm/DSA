def is_valid(s: str) -> bool:
    pair = {')':'(', ']':'[', '}':'{'}
    st = []
    for ch in s:
        if ch in '([{':
            st.append(ch)
        else:
            if not st or st[-1] != pair[ch]:
                return False
            st.pop()
    return not st
