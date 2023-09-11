from FSM import *
from Utils.JsonUtils import *
from Utils.SavedInstanceUtils import *
from queue import Queue
from FridaLibs.mq_producer import Producer
from Utils.DrawGraphUtils import *


def suppress_keyboard_interrupt_message():
    old_excepthook = sys.excepthook

    def new_hook(exctype, value, traceback):
        if exctype != KeyboardInterrupt:
            old_excepthook(exctype, value, traceback)
        else:
            LogUtils.log_info('\nKeyboardInterrupt ...')
            LogUtils.log_info('do something after Interrupt ...')
            StatRecorder.get_instance().print_result()
            StatRecorder.get_instance().print_coverage()
            RuntimeContent.get_instance().clear_state_list()
            RuntimeContent.get_instance().clear_screen_list()
            JsonUtils.dump_screen_map_to_json()
            SavedInstanceUtils.dump_pickle(RuntimeContent.get_instance())

            # 绘制App界面跳转图
            if Config.get_instance().isDrawAppCallGraph:
                DrawGraphUtils.draw_callgraph(Config.get_instance().get_CollectDataName())

    sys.excepthook = new_hook


if __name__ == "__main__":
    pkgName = sys.argv[1]
    appName = sys.argv[2]
    depth = sys.argv[3]
    with open('tmp.txt', 'w') as f:
        f.write(pkgName + ";" + appName + ";" + depth)
    LogUtils.setup()
    if Config.get_instance().is_saved_start:
        runtime = SavedInstanceUtils.load_pickle(Config.get_instance().get_pickle_file_name())
        root = runtime.screen_map["root"]
    else:
        root = ScreenNode()
        root.ck_eles_text = "root"
        RuntimeContent.get_instance().set_last_screen_node(root)
        RuntimeContent.get_instance().set_last_clickable_ele_uid("dummy_root_element")
        RuntimeContent.get_instance().put_screen_map("root", root)

    suppress_keyboard_interrupt_message()

    # 计时开始
    StatRecorder.get_instance().set_start_time()

    restart_cnt = 0

    # 启动app
    d = Config.get_instance().get_device()
    d.app_start(Config.get_instance().get_target_pkg_name(), use_monkey=True)
    RuntimeContent.get_instance().set_last_screen_node(root)
    time.sleep(10)

    # frida开始hook
    queue = Queue()
    # 后台线程
    producer = Producer('Producer', queue, daemon=True)
    producer.start()

    # 控制FSM线程, 重启会继续运行
    while True:
        # FSM开始运行
        consumer_fsm = FSM('Consumer', queue)
        consumer_fsm.start()
        consumer_fsm.join()

        # fsm线程触发了RestartException
        if consumer_fsm.exit_code == 1:
            StatRecorder.get_instance().inc_restart_cnt()
            LogUtils.log_info("需要重启")
            # logging.exception(consumer_fsm.exception)
            # logging.exception(consumer_fsm.exc_traceback)
            StatRecorder.get_instance().print_result()
            StatRecorder.get_instance().print_coverage()
            RuntimeContent.get_instance().clear_state_list()
            RuntimeContent.get_instance().clear_screen_list()
            JsonUtils.dump_screen_map_to_json()
            SavedInstanceUtils.dump_pickle(RuntimeContent.get_instance())
            # 重启
            d.app_stop(Config.get_instance().get_target_pkg_name())
            time.sleep(5)
            d.app_start(Config.get_instance().get_target_pkg_name(), use_monkey=True)
            time.sleep(5)
            RuntimeContent.get_instance().set_last_screen_node(root)
        # fsm线程触发了TerminateException
        elif consumer_fsm.exit_code == 2:
            LogUtils.log_info("程序结束")
            # logging.exception(consumer_fsm.exception)
            # logging.exception(consumer_fsm.exc_traceback)
            StatRecorder.get_instance().print_result()
            StatRecorder.get_instance().print_coverage()
            RuntimeContent.get_instance().clear_state_list()
            RuntimeContent.get_instance().clear_screen_list()
            JsonUtils.dump_screen_map_to_json()
            SavedInstanceUtils.dump_pickle(RuntimeContent.get_instance())
            break
        # fsm线程触发了未知错误
        else:
            LogUtils.log_info("未知情况退出")
            logging.exception(consumer_fsm.exception)
            logging.exception(consumer_fsm.exc_traceback)
            StatRecorder.get_instance().print_result()
            StatRecorder.get_instance().print_coverage()
            RuntimeContent.get_instance().clear_state_list()
            RuntimeContent.get_instance().clear_screen_list()
            JsonUtils.dump_screen_map_to_json()
            SavedInstanceUtils.dump_pickle(RuntimeContent.get_instance())
            break

    # 程序收尾

    # 绘制App界面跳转图
    if Config.get_instance().isDrawAppCallGraph:
        DrawGraphUtils.draw_callgraph(Config.get_instance().get_CollectDataName())

