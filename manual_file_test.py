# Test script used to manually debug the file watcher. Should not be included or executed within Comfy itself.

def init_fw_test():

    import os
    import time
    import watcher
    from utils import cuteprint

    watcher.init_watcher(os.getenv('CUTE_COMFY_PATH_OVERRIDE'))
    cuteprint('File watcher initialized. Waiting for changes...')
    
    while True:
        time.sleep(1)

if __name__ == '__main__':
    init_fw_test()
