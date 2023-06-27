from FSM import *
from Utils.JsonUtils import *
from RestartException import RestartException
from RuntimeContent import RuntimeContent
from ScreenNode import ScreenNode
from Logger import *
from Utils.SavedInstanceUtils import *
import threading
import time
import os
from androguard.core.bytecodes import apk
import shutil
import sys

def write_log():
    Logger.get_instance().print('\nsuppress_keyboard_interrupt_message KeyboardInterrupt ...')
    Logger.get_instance().print('do something after Interrupt ...')
    StatRecorder.get_instance().print_result()
    RuntimeContent.get_instance().clear_state_list()
    RuntimeContent.get_instance().clear_screen_list()
    JsonUtils.dump_screen_map_to_json()
    SavedInstanceUtils.dump_pickle(RuntimeContent.get_instance())

def suppress_keyboard_interrupt_message():
    old_excepthook = sys.excepthook

    def new_hook(exctype, value, traceback):
        print("exctype: ", exctype)
        if exctype != KeyboardInterrupt:
            old_excepthook(exctype, value, traceback)
        else:
            Logger.get_instance().print('\nsuppress_keyboard_interrupt_message KeyboardInterrupt ...')
            Logger.get_instance().print('do something after Interrupt ...')
            StatRecorder.get_instance().print_result()
            RuntimeContent.get_instance().clear_state_list()
            RuntimeContent.get_instance().clear_screen_list()
            JsonUtils.dump_screen_map_to_json()
            SavedInstanceUtils.dump_pickle(RuntimeContent.get_instance())
    sys.excepthook = new_hook

def run(target_pkg_name):
    Config.get_instance().target_pkg_name = target_pkg_name
    # 清理所有的log
    RuntimeContent.get_instance().clear_all()

    Logger.get_instance().setup(Config.get_instance().get_log_file_name())
    fsm = FSM()
    if Config.get_instance().is_saved_start:
        runtime = SavedInstanceUtils.load_pickle(Config.get_instance().get_pickle_file_name())
    else:
        root = ScreenNode()
        root.ck_eles_text = "root"
        RuntimeContent.get_instance().set_last_screen_node(root)
        RuntimeContent.get_instance().put_screen_map("root", root)

    # suppress_keyboard_interrupt_message()
    # 计时开始
    StatRecorder.get_instance().set_start_time()

    restart_cnt = 0


    while True:
        ## 启动app
        d = Config.get_instance().get_device()

        d.app_start(Config.get_instance().get_target_pkg_name(), use_monkey=True)
        time.sleep(10)
        try:
            fsm.start()
        except RestartException as e:
            restart_cnt += 1
            Logger.get_instance().print("需要重启")
            logging.exception(e)
            StatRecorder.get_instance().print_result()
            RuntimeContent.get_instance().clear_state_list()
            RuntimeContent.get_instance().clear_screen_list()
            JsonUtils.dump_screen_map_to_json()
            SavedInstanceUtils.dump_pickle(RuntimeContent.get_instance())
            d.app_stop(Config.get_instance().get_target_pkg_name())
            time.sleep(10)
        except Exception as e:
            logging.exception(e)
            StatRecorder.get_instance().print_result()
            RuntimeContent.get_instance().clear_state_list()
            RuntimeContent.get_instance().clear_screen_list()
            JsonUtils.dump_screen_map_to_json()
            SavedInstanceUtils.dump_pickle(RuntimeContent.get_instance())
            break

    Logger.get_instance().print("程序结束")

def terminate_thread(thread):
    import ctypes
    if not thread.is_alive():
        print("不活跃？！")
        return

    exc = ctypes.py_object(KeyboardInterrupt)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

    write_log()

def create_path_ifnotexist(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_timestamp():
    timestamp = int(round(time.time() * 1000000))
    return timestamp

if __name__ == '__main__':
    app_path = Config.get_instance().app_path
    app_data_path = Config.get_instance().app_data_path
    if not os.path.exists(app_path):
        print("文件夹不存在: ", app_path)
        sys.exit()
    create_path_ifnotexist(app_data_path)

    for file in os.listdir(app_path):  # 遍历文件夹
        try:
            if os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
                continue
            if not file.endswith('apk'):
                continue
            a = apk.APK(os.path.join(app_path, file))
            package_name = a.get_package()
            app_name = a.get_app_name()
            permission = a.get_permissions()

            timestamp = get_timestamp()
            cur_app_path = os.path.join(app_data_path, package_name, str(timestamp))
            create_path_ifnotexist(cur_app_path)
            Config.get_instance().cur_app_path = cur_app_path

            print("currently running %s"%(package_name))

            # 卸载app
            os.system("adb shell pm uninstall %s"%(package_name))

            # 安装app
            os.system("adb install %s"%(os.path.join(app_path, file)))

            meta_data_file = open(os.path.join(cur_app_path, str(timestamp) + '.txt'), "w+")
            meta_data_file.writelines('package_name: ' + package_name + "\n" + "\n")
            meta_data_file.writelines('app_name: ' + app_name + "\n" + "\n")
            meta_data_file.writelines('permission: ' + str(permission) + "\n" + "\n")
            meta_data_file.flush()

            time.sleep(10)

            th = threading.Thread(target=run, args=(package_name, ))
            th.start()

            # # 等待5秒钟
            time.sleep(Config.get_instance().ever_app_run_time)

            terminate_thread(th)  # Signal termination

            th.join()

        except Exception as e:
            print("%s 自动化跑运行时报错了"%(Config.get_instance().target_pkg_name))
        finally:
            # 跑完卸载app
            os.system("adb shell pm uninstall %s" % (Config.get_instance().target_pkg_name))
            # 清除当前线程
            if Config.get_instance().target_pkg_name != "":
                os.system("adb shell pm clear %s"%(Config.get_instance().target_pkg_name))


    time.sleep(1000)