import enum
import re


def preprocess_html(html):
    body = re.search(r"<body.*<\/body>", html, flags=re.S).group(0)
    body = re.sub(r"<script.*?<\/script>", "", body, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = re.sub(r"[\n\r]", "", body)
    body = re.sub(r"\t+", " ", body)
    return body


# Token-Type
class TT(enum.Enum):
    open = 1
    close = 2
    string = 3
    comment = 4


class Token:
    def __init__(self, token, ttype, level):
        self.token = token
        self.ttype = ttype
        self.tag = self.get_tag(token, ttype)
        self.level = level

    def get_tag(self, token, ttype):
        if ttype != TT.open and ttype != TT.close:
            return None
        else:
            return re.sub(r"[<\/>]", "", token.split(" ")[0])

    def is_tag(self):
        return self.ttype == TT.open or self.ttype == TT.close

    def is_string(self):
        return self.ttype == TT.string

    def compare(self, other):
        if self.ttype == TT.string:
            return self.token == other.token
        elif self.ttype == other.ttype:
            return self.tag == other.tag and self.level == other.level
        return False

    def is_same_level(self, other):
        return self.level == other.level

    def is_self_closing(self):
        return self.tag.lower() in ["img", "br", "area", "input"]

    def __str__(self):
        if self.ttype == TT.string:
            return self.token
        elif self.ttype == TT.open:
            return f"<{self.tag}>"
        elif self.ttype == TT.close:
            return f"</{self.tag}>"
        else:
            return self.token


def tokenize(html):
    tokens = []
    self_closing = ["img", "br", "area", "input"]
    level = 0

    idx = -1
    while idx < len(html) - 1:
        idx += 1
        token = ""
        c = html[idx]
        c_n = html[idx + 1]

        if c == "<" and c_n == "/":
            while c != ">" and idx < len(html) - 1:
                token += c
                idx += 1
                c = html[idx]
            token += c
            level -= 1
            tokens.append(Token(token, TT.close, level))
            continue

        if c == "<" and c_n == "!":
            while c != ">" and idx < len(html) - 1:
                token += c
                idx += 1
                c = html[idx]
            token += c
            tokens.append(Token(token, TT.comment, level))
            continue

        if c == "<" and c_n != "/" and c_n != "!":
            while c != ">" and idx < len(html) - 1:
                token += c
                idx += 1
                c = html[idx]
            token += c
            t = Token(token, TT.open, level)
            tokens.append(t)
            if not t.is_self_closing():
                level += 1
            continue

        if c not in [" ", "\n", "\t"]:
            while c_n != "<" and idx < len(html) - 2:
                token += c
                idx += 1
                c = html[idx]
                c_n = html[idx + 1]
            if token:
                tokens.append(Token(token + c, TT.string, level))

    return tokens