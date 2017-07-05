from common import get_category_for_id
from test import lex_test, get_next_token_test

def lex(src):
    print "+++++++++++++++"
    print "ANALYSING", src
    print "+++++++++++++++"
    start_index = 0
    tokens = []
    src = src + " "
    while True:
        if start_index >= len(src):
            break
        (error, token, last_index) = get_next_token(src, start_index)
        if error:
            print error, token, last_index
            break

        if token:
            tokens.append(token)
            print (token["category"], token["lexeme"])
        start_index = last_index

    return tokens

def get_next_token(src, start_index):
    data = {
        "i": start_index,
        "state": "INITIAL",
        "error": False,
    }

    token = {
        "lexeme": "",
        "category": "",
    }

    while True:
        # print "===="
        # print data
        # print token
        # print "++++"

        if data['i'] >= len(src):
            break;

        c = src[data['i']]

        if data["state"] == "INITIAL":
            if c.isspace():
                data['i'] += 1

            elif c == '(':
                # fold lexeme
                token['lexeme'] += c
                # categorize
                token["category"] = "PAROPEN"
                # next chart
                data['i'] += 1

                # lambda transition
                break
            elif c == ')':
                token['lexeme'] += c
                token["category"] = "PARCLOSE"
                data['i'] += 1

                # lambda transition
                break
            elif c == '+' or c == '-' or c == '*':
                token['lexeme'] += c
                token["category"] = "OPMAT"
                data['i'] += 1

                # transition
                # TRAILING WHITESPACE
                data['state'] = "WHITESPACE"

            elif c == '=':
                token['lexeme'] += c
                token["category"] = "OPREL"
                data['i'] += 1

                # transition
                data['state'] = "WHITESPACE"

            elif c == '>' or c == '<':
                token['lexeme'] += c
                token["category"] = "OPREL"
                data['i'] += 1

                # transition
                data["state"] = "OPREL_COMPOSITE"

            elif c == "\"":
                token['lexeme'] += c
                token["category"] = "STRING"
                data['i'] += 1

                # transition
                data["state"] = "STRING"

            elif c.isalpha():
                token['lexeme'] += c
                token["category"] = "ID"
                data['i'] += 1

                # transition
                data["state"] = "ID"

            elif c.isdigit():
                token['lexeme'] += c
                token["category"] = "NUMBER"
                data['i'] += 1

                # transition
                data["state"] = "NUMBER"

            else:
                data["error"] = "ERROR: NOT RECOGNIZED TOKEN"
                break;

        elif data["state"] == "WHITESPACE":
            # this only makese sure that a single whitespace is after something
            if c.isspace():
                # token['lexeme'] += c
                # token["category"] = "PAROPEN"
                data['i'] += 1

                # lambda transition
                break
            else:
                token['lexeme'] += c
                token["category"] = "ERROR"
                data['i'] += 1

                data["error"] = "ERROR: WHITEPSACE MISSING"
                break;

        elif data["state"] == "OPREL_COMPOSITE":
            if c == "=":
                token['lexeme'] += c
                token["category"] = "OPREL"
                data['i'] += 1

                # transition
                data['state'] = "WHITESPACE"
            elif c.isspace():
                # no next char
                # data['i'] += 1

                # transition
                data['state'] = "WHITESPACE"

        elif data["state"] == "ID":
            if c.isalpha():
                token['lexeme'] += c
                token["category"] = "ID"
                data['i'] += 1

                # transition
                data["state"] = "ID"

            elif c.isspace():
                # no next char
                # data['i'] += 1
                token["category"] = get_category_for_id(token["lexeme"])

                # transition
                data['state'] = "WHITESPACE"

            elif c == ")":
                token["category"] = get_category_for_id(token["lexeme"])

                # lambda transition
                break

            else:
                token['lexeme'] += c
                token["category"] = "ERROR"
                data['i'] += 1

                data["error"] = "ERROR: NOT RECOGNIZED TOKEN"
                break;

        elif data["state"] == "NUMBER":
            if c.isdigit():
                token['lexeme'] += c
                token["category"] = "NUMBER"
                data['i'] += 1

                # transition
                data["state"] = "NUMBER"

            elif c.isspace():
                # no next char
                # data['i'] += 1

                # transition
                data['state'] = "WHITESPACE"

            elif c == ")":
                # TODO Should we always increase i ++ and only in special cases do i-- to stay on the same char ?
                # lambda transition
                break

            else:
                token['lexeme'] += c
                token["category"] = "ERROR"
                data['i'] += 1

                data["error"] = "ERROR: NOT RECOGNIZED TOKEN"
                break;

        elif data["state"] == "STRING":
            token['lexeme'] += c
            token["category"] = "STRING"
            data['i'] += 1

            if c == "\"":
                # transition
                data["state"] = "STRING_END"

            else:
                # transition
                data["state"] = "STRING"

        elif data["state"] == "STRING_END":
            if c.isspace():
                # no next char
                # data['i'] += 1

                # transition
                data['state'] = "WHITESPACE"

            elif c == ")":
                # lambda transition
                break

            else:
                token['lexeme'] += c
                token["category"] = "ERROR"
                data['i'] += 1

                data["error"] = "ERROR: NOT RECOGNIZED TOKEN"
                break;


        else:
            token['lexeme'] += c
            token["category"] = "ERROR"
            data['i'] += 1

            data["error"] = "ERROR: NOT RECOGNIZED TOKEN"
            break;


    # This procedure could return a token or nothing
    if token["category"] == "":
        token = None

    return (data["error"], token, data["i"])


get_next_token_test(get_next_token)
lex_test(lex)
