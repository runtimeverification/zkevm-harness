from zkevm_harness.hello import hello


def test_hello() -> None:
    assert hello('World') == 'Hello, World!'
