import enum
import re
from tokenizer import preprocess_html, tokenize, Token, TT


# Match-Type
class MT(enum.Enum):
    normal = 1
    field = 2
    optional = 3
    iterator = 4


class WrapperEntry:
    def __init__(self, tokens, mtype):
        self.tokens = tokens
        self.mtype = mtype

    def compare(self, t):
        return self.mtype == MT.normal and t.compare(self.tokens[0])

    def __str__(self):
        tks = "".join([t.__str__() for t in self.tokens])
        if self.mtype == MT.normal:
            return tks
        if self.mtype == MT.field:
            return "#PCDATA"
        if self.mtype == MT.optional:
            return f"( {tks} )?"
        if self.mtype == MT.iterator:
            return f"( {tks} )+"


def search_down(terminal, tokens, idx):
    stack = -1

    while True:
        if idx > len(tokens) - 1:
            return False
        if stack == 0:
            if terminal.compare(tokens[idx]):
                return idx

        if terminal.tag == tokens[idx].tag:
            if tokens[idx].ttype == TT.open:
                stack += 1
            elif tokens[idx].ttype == TT.close:
                stack -= 1

        idx += 1


def search_up(terminal, tokens, idx):
    stack = -1

    while True:
        if not idx >= 0:
            return False
        if stack == 0:
            if terminal.compare(tokens[idx]):
                return idx

        if terminal.tag == tokens[idx].tag:
            if tokens[idx].ttype == TT.close:
                stack += 1
            elif tokens[idx].ttype == TT.open:
                stack -= 1

        idx -= 1


def match_iterator(a, b, idx_a, idx_b):
    term_idx = idx_a - 1
    terminal_tag = a[term_idx]
    while not terminal_tag.is_tag():
        term_idx -= 1
        terminal_tag = a[term_idx]

    if terminal_tag.is_self_closing():
        print("Failed to match iterator")
        print(f"Terminal TAG: {terminal_tag}")
        return None, idx_a, idx_b

    for idx, smp in [(idx_a, a), (idx_b, b)]:
        init_idx = idx

        # Find square candidate down
        idx = search_down(terminal_tag, smp, idx)
        if not idx:
            print("Search down failed")
            continue
        smp1 = list(smp[init_idx : idx + 1])

        # Find square candidate up
        idx = search_up(smp[init_idx], smp, init_idx - 1)
        if not idx:
            print("Search up failed")
            continue
        smp2 = list(smp[idx:init_idx])

        if len(smp1) - len(smp2) > 10:
            print("! Length difference too great !")
            idx = search_up(smp[init_idx], smp, idx - 1)
            if not idx:
                print("Search up SECOND failed")
                continue
            smp2 = list(smp[idx:init_idx])

        print("Square 1:")
        print(*smp1)

        print("Square 2:")
        print(*smp2)

        square = road_runner(smp1, smp2)

        if not square:
            break

        idx = init_idx
        print(f"terminal: {terminal_tag}")
        while idx < len(smp) - 1:
            if smp[idx].compare(smp[init_idx]):
                idx = search_down(terminal_tag, smp, idx)
                idx += 1
            else:
                break

        if init_idx == idx_a:
            return square, idx - 1, idx_b - 1
        elif init_idx == idx_b:
            return square, idx_a - 1, idx - 1

    print("Failed to match iterator")
    return None, idx_a, idx_b


def match_optional(a, b, idx_a, idx_b):
    init_idx_a = idx_a
    init_idx_b = idx_b

    tag_a = a[idx_a]
    tag_b = b[idx_b]

    optional_a = []
    optional_b = []

    a_stack = 0
    b_stack = 0

    while True:
        idx_a += 1
        idx_b += 1

        if idx_a > len(a) - 1 or idx_b > len(b) - 1:
            print("Error: couldn't find optional match")
            return False, init_idx_b + 1, init_idx_b + 1

        optional_a.append(a[idx_a - 1])
        optional_b.append(b[idx_b - 1])

        token_a = a[idx_a]
        token_b = b[idx_b]

        if (
            token_a.tag == tag_b.tag
            and tag_b.ttype == TT.close
            and token_a.ttype == TT.open
        ):
            a_stack += 1
        if (
            token_b.tag == tag_a.tag
            and tag_a.ttype == TT.close
            and token_b.ttype == TT.open
        ):
            b_stack += 1

        if token_a.compare(tag_b):
            if a_stack == 0:
                print(f"Opt match: {token_a}, {tag_b}")
                return optional_a, idx_a - 1, init_idx_b - 1
            else:
                a_stack -= 1

        if token_b.compare(tag_a):
            if b_stack == 0:
                print(f"Opt match: {token_b}, {tag_a}")
                return optional_b, init_idx_a - 1, idx_b - 1
            else:
                b_stack -= 1


def match_str_tag(a, b, idx_a, idx_b):
    token_a: Token = a[idx_a]
    token_b: Token = b[idx_b]

    match = []
    if token_a.is_tag():
        if token_a.is_self_closing():
            match.append(token_a)
            idx_a += 1
        else:
            while True:
                match.append(a[idx_a])
                if a[idx_a].tag == token_a.tag and a[idx_a].ttype == TT.close:
                    break
                idx_a += 1
        return match, idx_a, idx_b

    if token_b.is_tag():
        if token_b.is_self_closing():
            match.append(token_b)
            idx_b += 1
        else:
            while True:
                match.append(b[idx_b])
                if b[idx_b].tag == token_b.tag and b[idx_b].ttype == TT.close:
                    break
                idx_b += 1
        return match, idx_a, idx_b


def generalize_wrapper(wrapper, match):
    new_wrapper = []

    open_token = match[0]
    close_token = match[-1]

    idx = len(wrapper) - 1
    while idx >= 0:
        if wrapper[idx].compare(close_token):
            while not wrapper[idx].compare(open_token):
                idx -= 1
        else:
            new_wrapper = wrapper[0 : idx + 1]
            break

        idx -= 1

    print(f"Wrapper (old, new) ({len(wrapper)}, {len(new_wrapper)})")

    return new_wrapper


def road_runner(a, b):
    wrapper = []
    idx_a, idx_b = 0, 0

    count = 0
    while True:
        if idx_a > len(a) - 1 or idx_b > len(b) - 1:
            return wrapper

        token_a: Token = a[idx_a]
        token_b: Token = b[idx_b]

        # TOKEN mismatch
        if not token_a.compare(token_b):
            # TAG mismatch
            if token_a.is_tag() and token_b.is_tag():
                print(f"{count} - Matching iterator (a, b): ({token_a}, {token_b})")
                match, idx_a, idx_b = match_iterator(a, b, idx_a, idx_b)
                if match:
                    wrapper = generalize_wrapper(wrapper, match)
                    wrapper.append(WrapperEntry(match, MT.iterator))
                else:
                    print(f"{count} - Matching optional (a, b): ({token_a}, {token_b})")
                    match, idx_a, idx_b = match_optional(a, b, idx_a, idx_b)
                    if not match:
                        print_wrapper(wrapper)
                        return False
                    wrapper.append(WrapperEntry(match, MT.optional))
            # STRING mismatch
            elif token_a.is_string() and token_b.is_string():
                print(f"{count} - Matching string (a, b): ({token_a}, {token_b})")
                wrapper.append(WrapperEntry(["#PCDATA"], MT.field))
            else:
                print(f"(STRING, TAG) - ({token_a}, {token_b}) mismatch occured")
                match, idx_a, idx_b = match_str_tag(a, b, idx_a, idx_b)
                wrapper.append(WrapperEntry(match, MT.optional))

            # print("\n")
            # print_wrapper(wrapper)
            # print("\n")
        else:
            wrapper.append(WrapperEntry([token_a], MT.normal))
            print(f"{count} - Found Match: ({token_a}, {token_b})")

        idx_a += 1
        idx_b += 1
        count += 1

        # print_wrapper(wrapper)


def sp_print(str, spaces):
    out = " " * spaces + str
    print(out)


def print_wrapper(wrapper):
    spaces = 0
    for we in wrapper:
        if we.mtype == MT.normal:
            if we.tokens[0].ttype == TT.open:
                sp_print(we.__str__(), spaces)
                if not we.tokens[0].is_self_closing():
                    spaces += 2
            elif we.tokens[0].ttype == TT.close:
                spaces -= 2
                sp_print(we.__str__(), spaces)
            else:
                sp_print(we.__str__(), spaces)
        else:
            sp_print(we.__str__(), spaces)


def auto_extract(sites):
    for idx, site in enumerate(sites):
        if idx != 0:
            continue
        p_names = list(site.keys())
        p_htmls = list(site.values())

        a = preprocess_html(p_htmls[0])
        b = preprocess_html(p_htmls[1])
        tokens_a = tokenize(a)
        tokens_b = tokenize(b)

        print(f"---- {p_names[0]} ----")
        print("TOKENS:", *tokens_a[:20], "...", sep=" ", end="\n\n")

        print(f"---- {p_names[1]} ----")
        print("TOKENS:", *tokens_b[:20], "...", sep=" ", end="\n\n")

        wrapper = road_runner(tokens_a, tokens_b)

        print(f"---- {p_names[0]} ----")
        # print(*wrapper, sep="\n")
        print_wrapper(wrapper)

        exit()