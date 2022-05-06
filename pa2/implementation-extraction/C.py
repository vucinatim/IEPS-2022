import enum
import re


# Token-Type
class TT(enum.Enum):
    tag = 1
    string = 2
    comment = 3


# Match-Type
class MT(enum.Enum):
    normal = 1
    field = 2
    optional = 3
    iterator = 4


def preprocess_html(html):
    body = re.search(r"<body.*<\/body>", html, flags=re.S).group(0)
    body = re.sub(r"<script.*?<\/script>", "", body, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = re.sub(r"\n", "", body)
    return body


def tokenize(html):
    tokens = []

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
            tokens.append((token, TT.tag, token))
            continue

        if c == "<" and c_n == "!":
            while c != ">" and idx < len(html) - 1:
                token += c
                idx += 1
                c = html[idx]
            token += c
            tokens.append(("<!-- -->", TT.comment, token))
            continue

        if c == "<" and c_n != "/" and c_n != "!":
            while c != ">" and idx < len(html) - 1:
                token += c
                idx += 1
                c = html[idx]
            token += c
            tag = (token.split(" ")[0] + ">").replace(">>", ">")
            tokens.append((tag, TT.tag, token))
            continue

        if c not in [" ", "\n", "\t"]:
            while c_n != "<" and idx < len(html) - 2:
                token += c
                idx += 1
                c = html[idx]
                c_n = html[idx + 1]
            if token:
                tokens.append((token, TT.string, token))

    return tokens


def match_iterator(a, b, idx_a, idx_b):
    terminal_tag = a[idx_a - 1]

    for idx, smp in [(idx_a, a), (idx_b, b)]:
        init_idx = idx
        while True:
            if idx > len(smp) - 1:
                break
            if smp[idx] == terminal_tag:
                smp1 = list(smp[init_idx : idx + 1])
                smp2 = []
                idx = init_idx
                while True:
                    if smp[idx] == smp[init_idx]:
                        smp2 = list(smp[idx : init_idx + 1])
                        idx -= 1
                        break

                square = road_runner(smp1, smp2)

                return (MT.iterator, road_runner(smp1, smp2))

            idx += 1


def match_optional(a, b, idx_a, idx_b):
    init_idx_a = idx_a
    init_idx_b = idx_b

    tag_a = a[idx_a]
    tag_b = b[idx_b]

    optional_a = []
    optional_b = []

    while True:
        idx_a += 1
        idx_b += 1

        if idx_a > len(a) - 1 or idx_b > len(b) - 1:
            print("Error: couldn't find optional match")
            exit()
            return None

        token_a = a[idx_a]
        token_b = b[idx_b]

        optional_a.append(token_a[2])
        optional_b.append(token_b[2])

        if token_a == tag_b:
            return (MT.optional, optional_a), idx_a, init_idx_b

        if token_b == tag_a:
            return (MT.optional, optional_b), init_idx_a, idx_b


def road_runner(a, b):
    wrapper = []
    spaces = 0
    idx_a, idx_b = 0, 0

    token_a = a[idx_a]
    token_b = b[idx_b]

    while True:
        if idx_a > len(a) - 1 or idx_b > len(b) - 1:
            return wrapper

        # TOKEN mismatch
        if token_a[2] != token_b[2]:
            # TAG mismatch
            if token_a[1] == TT.tag and token_b == TT.tag:
                match, idx_a, idx_b = match_iterator(a, b, idx_a, idx_b)
                if not match:
                    match, idx_a, idx_b = match_optional(a, b, idx_a, idx_b)
                wrapper.append(match)
            # STRING mismatch
            elif token_a[1] == TT.string and token_b == TT.string:
                wrapper.append((MT.normal, "#PCDATA"))
            else:
                print("Error: STRING - TAG mismatch occured")
        else:
            wrapper.append(token_a[2])

        idx_a += 1
        idx_b += 1


def auto_extract(sites):
    for idx, site in enumerate(sites):
        p_names = list(site.keys())
        p_htmls = list(site.values())

        a = preprocess_html(p_htmls[0])
        b = preprocess_html(p_htmls[1])
        tokens_a = tokenize(a)
        tokens_b = tokenize(b)

        neki = [0, 1, 2, 3, 4, 5]
        print(neki[0:4])

        # out = road_runner(tokens_a, tokens_b)

        print(f"---- {p_names[0]} ----")
        print(*tokens_a, sep="\n")

        print(f"---- {p_names[0]} ----")
        print(*tokens_b, sep="\n")
        exit()