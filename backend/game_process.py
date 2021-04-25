from game.game_handler import GameHandler
from extensions import g_redis
import sys
import subprocess
import time
import threading


def start_game(table_id):
    DETACH = 0x8
    subprocess.Popen(['py', '-3', 'game_process.py', table_id], shell=False,
            stdin=None, stdout=None, stderr=None, close_fds=None, creationflags=DETACH)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Can\'t start without a table id in argvs')
    game_handler = GameHandler(sys.argv[1])
    main_thread = threading.Thread(target=game_handler.start_game)
    main_thread.start()
    update_thread = threading.Thread(target=game_handler.update_to_redis_periodically)
    update_thread.start()
    main_thread.join()
    time.sleep(60)
    sys.exit()
