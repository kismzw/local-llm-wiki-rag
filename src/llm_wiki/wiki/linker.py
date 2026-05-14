def extract_wikilinks(text: str) -> list[str]:
    out = []
    i = 0
    while i < len(text):
        s = text.find("[[", i)
        if s < 0:
            break
        e = text.find("]]", s + 2)
        if e < 0:
            break
        out.append(text[s + 2:e])
        i = e + 2
    return out
