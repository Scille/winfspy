from winfspy.plumbing import SecurityDescriptor


def test_security_descriptor():
    string = "O:BAG:BAD:P(A;;FA;;;SY)(A;;FA;;;BA)(A;;FA;;;WD)"
    sd = SecurityDescriptor.from_string(string)
    assert sd.to_string() == string
