def largest_rectangle_area(heights: list[int]) -> int:
    st=[]; best=0
    for i,h in enumerate(heights+[0]):
        while st and heights[st[-1]] > h:
            H=heights[st.pop()]
            L=st[-1] if st else -1
            best=max(best, H*(i-L-1))
        st.append(i)
    return best
