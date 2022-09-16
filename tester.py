#coding: incdec

assert b"a++ ++a a-- --a".decode('incdec') == "((a, a := a+1)[0]) ((a, a := a+1)[1]) ((a, a := a-1)[0]) ((a, a := a-1)[1])"
assert b"'a++ ++a a-- --a'".decode('incdec') == "'a++ ++a a-- --a'"
assert b'"a++ ++a a-- --a"'.decode('incdec') == '"a++ ++a a-- --a"'

i = 6
assert i-- == 6
assert i == 5
assert ++i == 6
assert --i == 5
assert i++ == 5
assert i == 6
