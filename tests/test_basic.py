import lucy_compiler


def test_compile():
    assert lucy_compiler.compile(source='print("42")').stdout.strip() == "42"
