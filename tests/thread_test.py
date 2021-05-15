from multiprocessing import Pool, Queue

visited = set()
#queue = Queue()

pool_size=5


def prun():
    value = queue.get()
    print(value)
    value = value + 1
    if value < 10:
        queue.put(value)
        queue.put(value + 1)


def start():
    queue = Queue()
    queue.put(0)
    pool = Pool(3)
    print(queue.empty())
    while not queue.empty():
        print('running')
        pool.apply_async(prun)
    pool.close()
    pool.join()





start()
