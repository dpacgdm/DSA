PRIMARY = "simplify_path"
CASES = [
    (("/home/",), "/home"),
    (("/../",), "/"),
    (("/home//foo/",), "/home/foo"),
    (("/a/./b/../../c/",), "/c"),
    (("/a//b/../c/",), "/a/c"),
]
