import logging
import sys
import time
from FSM import *
from Config import Config
from JsonHelper import dump_screen_map_to_json
from RestartException import RestartException
from RuntimeContent import RuntimeContent
from ScreenCompareStrategy import ScreenCompareStrategy, LCSComparator
from ScreenNode import ScreenNode
from StatRecorder import StatRecorder
from Logger import *


def suppress_keyboard_interrupt_message():
    old_excepthook = sys.excepthook

    def new_hook(exctype, value, traceback):
        if exctype != KeyboardInterrupt:
            old_excepthook(exctype, value, traceback)
        else:
            Logger.get_instance().print('\nKeyboardInterrupt ...')
            Logger.get_instance().print('do something after Interrupt ...')
            StatRecorder.get_instance().print_result()
            file_name = Config.get_instance().get_target_pkg_name() + "_" + "interupt"
            dump_screen_map_to_json(file_name)
    sys.excepthook = new_hook


if __name__ == "__main__":
    Logger.get_instance().setup(Config.get_instance().get_log_file_name())
    FSM = FSM()
    root = ScreenNode()
    root.ck_eles_text = "root"
    RuntimeContent.get_instance().set_last_screen_node(root)
    RuntimeContent.get_instance().put_screen_map("root", root)

    suppress_keyboard_interrupt_message()
    # 计时开始
    StatRecorder.get_instance().set_start_time()

    restart_cnt = 0
    while True:
        ## 启动app
        d = RuntimeContent.get_instance().get_device()
        d.app_start(Config.get_instance().get_target_pkg_name(), use_monkey=True)
        time.sleep(10)
        try:
            FSM.start()
        except RestartException as e:
            restart_cnt += 1
            Logger.get_instance().print("需要重启")
            logging.exception(e)
            StatRecorder.get_instance().print_result()
            file_name = Config.get_instance().get_target_pkg_name() + "_" + str(restart_cnt)
            dump_screen_map_to_json(file_name)
            RuntimeContent.get_instance().clear_state_list()
            RuntimeContent.get_instance().clear_screen_list()
            d.app_stop(Config.get_instance().get_target_pkg_name())
            time.sleep(10)
        except Exception as e:
            logging.exception(e)
            break

    Logger.get_instance().print("程序结束")
    StatRecorder.get_instance().print_result()
