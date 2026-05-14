from llm_wiki.verification.verifier import verify_answer


def test_supported_and_unsupported():
    out = verify_answer("MICA uses attention.", ["MICA uses attention in model"])
    assert out["claims"][0]["status"] in {"supported", "partially_supported"}
    out2 = verify_answer("X Y Z U.", ["alpha beta"])
    assert out2["claims"][0]["status"] == "unsupported"
