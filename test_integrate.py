import signal
import subprocess
import platform


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

sys_platform = platform.platform().lower()
if 'windows' in sys_platform:
    os_type = 'win'
else:
    os_type = 'linux'

with open('apk_pkgName.txt') as f:
    content = f.readlines()
pkgName_appName_list = [item.rstrip('\n') for item in content]
for pkgName_appName in pkgName_appName_list:
    try:
        pkgName, appName = pkgName_appName.split(' | ')
        appName = appName.strip('\'')
        # print(os_type)
        # print(pkgName,appName)
        # TODO 还有'get_pp_from_dynamically_running_app', 'dynamic_ui_depth', 'dynamic_pp_parsing'需要配置
        if os_type == 'linux':
            execute_cmd_with_timeout('./run.sh {} {} {}'.format(pkgName, appName, config_settings['dynamic_ui_depth']))
        elif os_type == 'win':
            execute_cmd_with_timeout(
                'PowerShell.exe ./run.ps1 {} {} {}'.format(pkgName, appName, config_settings['dynamic_ui_depth']))
    except Exception:
        print('error occurred, continue...')

