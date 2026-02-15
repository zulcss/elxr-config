def test_users(host):
    """Ensure that root and user was created."""
    passwd = host.file("/etc/passwd")
    assert passwd.contains("root")
    assert passwd.contains("user")
