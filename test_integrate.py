import signal
import subprocess
import platform
def get_OS_type():
    sys_platform = platform.platform().lower()
    os_type = ''
    if "windows" in sys_platform:
        os_type = 'win'
    elif "darwin" in sys_platform or 'mac' in sys_platform:
        os_type = 'mac'
    elif "linux" in sys_platform:
        os_type = 'linux'
    else:
        print('Unknown OS,regard as linux...')
        os_type = 'linux'
    return os_type


def execute_cmd_with_timeout(cmd, timeout=600):
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, shell=True)
    try:
        p.wait(timeout)
    except subprocess.TimeoutExpired:
        p.send_signal(signal.SIGINT)
        p.wait()

config_settings = {'ui_static': 'true', 'ui_dynamic': 'true', 'code_inspection': 'true',
                       'pp_print_permission_info': 'true', 'pp_print_sdk_info': 'true',
                       'pp_print_sensitive_item': 'true', 'pp_print_others': 'true', 'pp_print_long_sentences': 'true',
                       'dynamic_print_full_ui_content': 'true', 'dynamic_print_sensitive_item': 'true',
                       'get_pp_from_app_store': 'true', 'get_pp_from_dynamically_running_app': 'false',
                       'dynamic_ui_depth': '3', 'dynamic_pp_parsing': 'true'}

with open('apk_pkgName.txt') as f:
    content = f.readlines()
pkgName_appName_list = [item.rstrip('\n') for item in content]
for pkgName_appName in pkgName_appName_list:
    try:
        pkgName, appName = pkgName_appName.split(' | ')
        appName = appName.strip('\'')
        if get_OS_type() in ['linux', 'mac']:
            execute_cmd_with_timeout('./run.sh {} {} {}'.format(pkgName, appName, config_settings['dynamic_ui_depth']))
        elif get_OS_type() == 'win':
            execute_cmd_with_timeout(
                'PowerShell.exe .\run.ps1 {} {} {}'.format(pkgName, appName, config_settings['dynamic_ui_depth']))
    except Exception:
        print('error occurred, continue...')