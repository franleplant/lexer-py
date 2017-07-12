from common import get_category_for_id
from test import lex_test, get_next_token_test

def buildAction(category, end=False):
    def action(c, data, token):
        token['lexeme'] += c
        token["category"] = category
        return end
    return action

def buildErrorAction(error):
    def action(c, data, token):
        token['lexeme'] += c
        token["category"] = "ERROR"
        data["error"] = "ERROR: " + error
    return action

def actionNull(c, data, token):
    pass

def actionIdTryReserved(c, data, token):
    token["category"] = get_category_for_id(token["lexeme"])
    data["index"] -= 1

def actionId(c, data, token):
    token['lexeme'] += c
    token["category"] = get_category_for_id(token["lexeme"])


def actionLambda(c, data, token):
    data["index"] -= 1


delta = [
    ("INITIAL"            , lambda c: c.isspace()                     , "INITIAL"            , actionNull                              ),
    ("INITIAL"            , lambda c: c == "("                        , "END"                , buildAction("PAROPEN", True)         ),
    ("INITIAL"            , lambda c: c == ")"                        , "END"                , buildAction("PARCLOSE", True)        ),
    ("INITIAL"            , lambda c: c == '+' or c == '-' or c == '*', "TRAILING_WHITESPACE", buildAction("OPMAT")                 ),
    ("INITIAL"            , lambda c: c == "="                        , "TRAILING_WHITESPACE", buildAction("OPREL")                 ),
    ("INITIAL"            , lambda c: c == '>' or c == '<'            , "OPREL_COMPOSITE"    , buildAction("OPREL")                 ),
    ("INITIAL"            , lambda c: c == '"'                        , "STRING"             , buildAction("STRING")                ),
    ("INITIAL"            , lambda c: c.isalpha()                     , "ID"                 , buildAction("ID")                    ),
    ("INITIAL"            , lambda c: c.isdigit()                     , "NUMBER"             , buildAction("NUMBER")                ),
    ("INITIAL"            , lambda c: True                            , "ERROR"              , buildErrorAction("BAD INIT TOKEN")   ),

    ("TRAILING_WHITESPACE", lambda c: c.isspace()                     , "END"                , actionNull                                ),
    ("TRAILING_WHITESPACE", lambda c: True                            , "END"                , buildErrorAction("WHITESPACE EXPECTED")),

    ("OPREL_COMPOSITE"    , lambda c: c == "="                        , "TRAILING_WHITESPACE", buildAction("OPREL")                        ),
    ("OPREL_COMPOSITE"    , lambda c: c.isspace()                     , "TRAILING_WHITESPACE", actionLambda                                  ),
    ("OPREL_COMPOSITE"    , lambda c: True                            , "ERROR"              , buildErrorAction("WHITESPACE OR = EXPECTED")),

    ("ID"                 , lambda c: c.isalpha()                     , "ID"                 , actionId                      ),
    ("ID"                 , lambda c: c.isspace()                     , "TRAILING_WHITESPACE", actionIdTryReserved           ),
    ("ID"                 , lambda c: c == ")"                        , "END"                , actionIdTryReserved           ),
    ("ID"                 , lambda c: True                            , "ERROR"              , buildErrorAction("BAD ID")    ),

    ("NUMBER"             , lambda c: c.isdigit()                     , "NUMBER"             , buildAction("NUMBER")         ),
    ("NUMBER"             , lambda c: c.isspace()                     , "TRAILING_WHITESPACE", actionLambda                    ),
    ("NUMBER"             , lambda c: c == ")"                        , "END"                , actionLambda                    ),
    ("NUMBER"             , lambda c: True                            , "ERROR"              , buildErrorAction("BAD NUMBER")),

    ("STRING"             , lambda c: c == '"'                        , "STRING_END"         , buildAction("STRING")         ),
    ("STRING"             , lambda c: True                            , "STRING"             , buildAction("STRING")         ),

    ("STRING_END"         , lambda c: c.isspace()                     , "TRAILING_WHITESPACE", actionLambda                    ),
    ("STRING_END"         , lambda c: c == ")"                        , "END"                , actionLambda                    ),
    ("STRING_END"         , lambda c: True                            , "ERROR"              , buildErrorAction("BAD STRING")),
]






def get_next_token(src, start_index):
    data = {
        "index": start_index,
        "state": "INITIAL",
        "error": False,
    }

    token = {
        "lexeme": "",
        "category": "",
    }


    while True:
        if data["state"] == "END" or data["state"] == "ERROR":
            break

        if data['index'] >= len(src):
            break;

        c = src[data['index']]

        found = False
        for (state, is_input, next_state, action) in delta:
            if state != data["state"]:
                continue

            if not is_input(c):
                continue

            found = True
            data['index'] += 1
            action(c, data, token)
            data["state"] = next_state
            break

        if not found:
            print "ERROR"
            break

    if token["category"] == "":
        token = None

    return (data["error"], token, data["index"])


def lex(src):
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
            # print (token["category"], token["lexeme"])
        start_index = last_index

    return tokens

print get_next_token("define", 0)
print get_next_token("define ", 0)
print get_next_token("hello", 0)
print get_next_token("123", 0)
print get_next_token('"hello"', 0)
print get_next_token("123 hello", 0)
print get_next_token("hello 123", 0)

get_next_token_test(get_next_token)
lex_test(lex)
