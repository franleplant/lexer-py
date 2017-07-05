
def get_next_token_test(get_next_token):
    (_, token, _) = get_next_token("hello", 0)
    assert token == {"category": "ID", "lexeme": "hello"}, "Simple word"

    (_, token, _) = get_next_token("12345", 0)
    assert token == {"category": "NUMBER", "lexeme": "12345"}, "Simple number"

    (_, token, _) = get_next_token(">=", 0)
    assert token == {"category": "OPREL", "lexeme": ">="}
    (_, token, _) = get_next_token(">= ", 0)
    assert token == {"category": "OPREL", "lexeme": ">="}

    (_, token, _) = get_next_token('"hello 123"', 0)
    assert token == {"category": "STRING", "lexeme": '"hello 123"'}

    print ">>>> GET_NEXT_TOKEN_TEST: OK"



def lex_test(lex):
    tokens = lex("> 123")
    expected = [
        {"category": "OPREL", "lexeme": ">"},
        {"category": "NUMBER", "lexeme": "123"},
    ]
    assert tokens == expected, "Should work"

    tokens = lex("hello ")
    expected = [
        {"category": "ID", "lexeme": "hello"},
    ]
    assert tokens == expected, "EOF testing"

    tokens = lex("abc123")
    expected = []
    assert tokens == expected, "fail case"


    tokens = lex("(define (myfn x y)\n  (+ 123 x y))")
    expected = [
        {"category": "PAROPEN", "lexeme": "("},
        {"category": "DEFINE", "lexeme": "define"},
        {"category": "PAROPEN", "lexeme": "("},
        {"category": "ID", "lexeme": "myfn"},
        {"category": "ID", "lexeme": "x"},
        {"category": "ID", "lexeme": "y"},
        {"category": "PARCLOSE", "lexeme": ")"},
        {"category": "PAROPEN", "lexeme": "("},
        {"category": "OPMAT", "lexeme": "+"},
        {"category": "NUMBER", "lexeme": "123"},
        {"category": "ID", "lexeme": "x"},
        {"category": "ID", "lexeme": "y"},
        {"category": "PARCLOSE", "lexeme": ")"},
        {"category": "PARCLOSE", "lexeme": ")"},
    ]
    assert tokens == expected, "integrated case"

    print ">>>> LEX_TEST: OK"
