from src.main_loop import MainLoop
import argparse


def parse_cli():
    parser = argparse.ArgumentParser(description='Automatic assistant')
    parser.add_argument('-name', '--name', help='username of the user', required=True)
    parser.add_argument('-task', '--task', help='description of the task to do by the assistant', required=True)
    args = parser.parse_args()
    return args


def main():
    args = parse_cli()
    username, task = args.name, args.task

    executor = MainLoop(username)
    res = executor.do_the_task(task)
    print(res)


main()

