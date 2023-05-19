from ScreenCompareStrategy import ScreenCompareStrategy

def check_is_errorscreen(error_screen_list:list, screen_text:str, screen_compare_strategy: ScreenCompareStrategy) -> bool:
    for err_screen_text in error_screen_list:
        simi_flag, cur_similarity = screen_compare_strategy.compare_screen(screen_text, err_screen_text)
        if simi_flag is True:
            return True
    return False

def check_is_error_clickable_ele(error_clickable_ele_uid_list, clickable_ele_uid):
    for err_ele_uid in error_clickable_ele_uid_list:
        if err_ele_uid == clickable_ele_uid:
            return True
    return False

def check_screen_list(screen_list):
    if screen_list is None:
        return False
    if len(screen_list) >= 5:
        last_text = screen_list[-1]
        if screen_list[-2] == last_text and \
                screen_list[-3] == last_text and \
                screen_list[-4] == last_text and \
                screen_list[-5] == last_text:
            return True
    else:
        return False


def check_state_list_reverse(k, state_list, target) -> bool:
    if k > len(state_list):
        return False
    for i in range(k):
        if state_list[len(state_list) - 1 - i] != target:
            return False
    return True


def check_screen_list_reverse(k, screen_list) -> bool:
    if k <= 1:
        return False
    if screen_list is None or len(screen_list) == 0:
        return False
    if len(screen_list) < k:
        return False
    # step为1, 2, 3
    for step in range(1, 4, 1):
        res = check_screen_list_by_pattern_reverse(k, screen_list, step)
        if res is True:
            return True
    return False


def check_screen_list_by_pattern_reverse(k, screen_list, step) -> bool:
    l = 0
    for i in range(step):
        l += 1
    for cnt in range(0, k - 1, 1):
        for i in range(step):
            if l >= len(screen_list):
                return False
            elif screen_list[len(screen_list) - 1 - l] != screen_list[len(screen_list) - 1 - i]:
                return False
            else:
                l += 1
    return True


def check_screen_list_order(k, screen_list) -> bool:
    if k <= 1:
        raise Exception
    if screen_list is None or len(screen_list) == 0:
        raise Exception
    if len(screen_list) < k:
        return False
    # step为1, 2, 3
    for step in range(1, 4, 1):
        res = check_screen_list_by_pattern_order(k, screen_list, step)
        if res is True:
            return True
    return False


def check_screen_list_by_pattern_order(k, screen_list, step) -> bool:
    l = 0
    for i in range(step):
        l += 1
    for cnt in range(0, k - 1, 1):
        for i in range(step):
            if l >= len(screen_list):
                return False
            elif screen_list[l] != screen_list[i]:
                return False
            else:
                l += 1
    return True


def check_is_inputmethod_in_cur_screen(d):
    # 小米的输入法
    if d(packageName="com.sohu.inputmethod.sogou.xiaomi").exists():
        return True
    elif d(packageName="com.miui.securityinputmethod").exists():
        return True
    # pixel的输入法
    elif d(packageName="com.google.android.inputmethod.latin").exists():
        return True
    else:
        return False


def check_is_in_home_screen(cur_screen_pkg_name):
    # 小米的home screen
    if cur_screen_pkg_name == "com.miui.home":
        return True
    # pixel的home screen
    if cur_screen_pkg_name == "com.google.android.apps.nexuslauncher":
        return True
    return False