from services.mislead_detector import check_is_mislead

res = check_is_mislead("")
assert res == False

res = check_is_mislead("hello")
assert res == False
