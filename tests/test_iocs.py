from socbot.iocs import classify_and_build, extract_iocs_from_text


def test_extract_iocs_from_text():
    text = "see http://Example.com/a?b=1 and 8.8.8.8 and test.com and 44d88612fea8a8f36de82e1278abb02f"
    iocs = extract_iocs_from_text(text)
    assert "8.8.8.8" in iocs
    assert "test.com" in iocs
    assert "44d88612fea8a8f36de82e1278abb02f" in iocs


def test_classify_and_normalize_domain():
    ioc = classify_and_build("Example.COM.")
    assert ioc is not None
    assert ioc.type == "domain"
    assert ioc.normalized == "example.com"


def test_classify_ip():
    ioc = classify_and_build("8.8.8.8")
    assert ioc is not None
    assert ioc.type == "ip"


def test_reject_bad_ip():
    assert classify_and_build("999.999.999.999") is None
