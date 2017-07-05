def get_category_for_id(s):
    if s == "define":
        return "DEFINE"
    elif s == "if":
        return "IF"
    elif s == "and":
        return "AND"
    else:
        return "ID"
