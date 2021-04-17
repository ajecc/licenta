from game.game_handler import GameHandler
import sys
import asyncio
import subprocess


def start_game(table_id):
    subprocess.call(['py', '-3', 'game/game_process.py', table_id])


async def _main():
    game_handler = GameHandler(sys.argv[1])
    main_task = asyncio.create_task(game_handler.start_game())
    asyncio.create_task(game_handler.update_to_redis_periodically())
    await main_task
    sys.exit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Can\'t start without a table id in argvs')
    asyncio.run(_main())
