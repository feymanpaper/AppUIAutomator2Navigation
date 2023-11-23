# producer.py
import json
import os
import subprocess
import threading
import time
from queue import Queue
from test_integrate import get_OS_type
from get_urls import get_pp_from_app_store, get_pkg_names_from_input_list


def producer_thread(queue, data):
    # 模拟保存数据到队列
    print("Adding data to queue:", data)
    time.sleep(2)  # 模拟保存操作耗时
    # 将数据放入队列中
    queue.put(data)


def consumer_thread(queue):
    processed_pp = set()

    while True:
        # 从队列中获取数据
        print('consumer thread waiting for data...')
        data = queue.get()
        print("Processing data:", data)
        # 缓冲5s，等待写入
        time.sleep(5)
        # 进行相应的处理操作
        pp_url_path, pkgName_appName = data.split('||')
        pkgName, appName = pkgName_appName.split('|')
        # 判断之前是否已经处理完成这个app的隐私政策，如果已经处理完成过，就没有必要继续重新处理
        if pkgName in processed_pp:
            print(f"{pkgName} has been processed before...")
            continue
        # 在这里进行其他处理操作
        app_pp = {}
        with open(pp_url_path, 'r', encoding='utf-8') as f:
            content = f.readlines()
            content = [item.strip('\n') for item in content]
            print('content in txt file of PrivacyPolicy', content)
            pp_url = content
            print('pp_url:', pp_url)
            if len(pp_url) == 1:
                if 'html' in pp_url[0]:
                    app_pp[pkgName] = [pp_url[0][:pp_url[0].index('html') + 4]][:]
                elif 'htm' in pp_url[0]:
                    app_pp[pkgName] = [pp_url[0][:pp_url[0].index('htm') + 3]][:]
                else:
                    if pp_url[0].endswith('.1.1'):
                        # 只有这一个结果，还是不合格的，视为没找到隐私政策
                        print('privacy policy not in ', pkgName)
                        pp_urls, missing_urls = get_pp_from_app_store(
                            get_pkg_names_from_input_list([pkgName]))
                        app_pp.update(pp_urls)
                    else:
                        app_pp[pkgName] = pp_url[:]

            elif len(pp_url) > 1:
                app_pp[pkgName] = pp_url[:]
        # 将最终输出给隐私政策分析模块的文件修改为 包名:[应用名，[url列表]]的形式
        if type(app_pp[pkgName]) == list:
            app_pp[pkgName] = [appName, app_pp[pkgName][:]]
        else:
            app_pp[pkgName] = [appName, [app_pp[pkgName][:]]]

        with open(os.path.join('..', 'Privacy-compliance-detection-2.1', 'core', 'pkgName_url.json'), 'w',
                  encoding='utf-8') as f:
            json.dump(app_pp, f, indent=4, ensure_ascii=False)
        # 调用隐私政策处理模块
        os_type = get_OS_type()
        print('call pp analysis module in consumer_thread!')
        if os_type == 'win':
            subprocess.run(['python', 'privacy-policy-main.py'],
                           cwd=os.path.join('..', 'Privacy-compliance-detection-2.1', 'core'),
                           timeout=600)
        elif os_type in ['linux', 'mac']:
            subprocess.run(['python3', 'privacy-policy-main.py'],
                           cwd=os.path.join('..', 'Privacy-compliance-detection-2.1', 'core'),
                           timeout=600)
        # TODO 需要加一个检测机制,判断这个应用的隐私政策到底解析成功没有.没有成功的话,还得靠原本的逻辑.
        #  逻辑可以用最简单的,看PrivacyPolicySaveDir里有没有这个应用的json解析结果.
        files_in_privacy_policy_save_dir = os.listdir(
            os.path.join('..', 'Privacy-compliance-detection-2.1', 'core', 'PrivacyPolicySaveDir'))
        if pkgName + '.json' in files_in_privacy_policy_save_dir and pkgName + '_sdk.json' in files_in_privacy_policy_save_dir:
            with open('successful_analysis_pp.txt', 'a', encoding='utf-8') as f:
                f.write(pkgName + '\n')
            processed_pp.add(pkgName)
            print('pp analysis in consumer done.')


def main_thread():
    # 创建一个阻塞队列
    queue = Queue()

    # 创建守护线程
    consumer = threading.Thread(target=consumer_thread, args=(queue,))
    consumer.daemon = True
    consumer.start()

    # 在主线程中调用生产者方法
    producer_thread(queue, "Hello, world!")


if __name__ == '__main__':
    main_thread()