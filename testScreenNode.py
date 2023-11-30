from ScreenNode import *

a = ScreenNode()
a.ck_eles_text = "aa"

b = ScreenNode()
b.ck_eles_text = "aa"

s = set()
s.add(a)
s.add(b)
print(s)