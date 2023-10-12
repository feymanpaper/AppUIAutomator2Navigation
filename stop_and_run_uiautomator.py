import uiautomator2 as u2
def rerun_uiautomator2():
    d = u2.connect()
    if d.uiautomator.running():
        print('uiautomator is running, stopping...')
        d.uiautomator.stop()
    print('start uiautomator2...')
    d.uiautomator.start()


if __name__ == '__main__':
    rerun_uiautomator2()
