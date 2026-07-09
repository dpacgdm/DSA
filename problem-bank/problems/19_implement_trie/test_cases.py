def test_lc_example(sol):
    t = sol.Trie()
    t.insert("apple")
    assert t.search("apple") is True
    assert t.search("app") is False
    assert t.starts_with("app") is True
    t.insert("app")
    assert t.search("app") is True

def test_empty_prefix(sol):
    t = sol.Trie()
    t.insert("a")
    assert t.starts_with("") is True
    assert t.search("") is False

def test_branch(sol):
    t = sol.Trie()
    t.insert("cat")
    t.insert("car")
    assert t.starts_with("ca") is True
    assert t.search("ca") is False
    assert t.search("cat") is True
    assert t.search("car") is True
    assert t.search("cap") is False

TESTS = [test_lc_example, test_empty_prefix, test_branch]
CASES = []
