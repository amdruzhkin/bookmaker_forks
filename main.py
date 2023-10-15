import time

from forks import Forks

if __name__ == '__main__':
    start_time = time.time()
    forks = Forks()
    forks.run()
    print(f"Seconds: {time.time() - start_time}")