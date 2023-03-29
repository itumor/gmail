import concurrent.futures

def worker(task):
    print(f"Processing task {task}")
    return task * 2

if __name__ == '__main__':
    tasks = [1, 2, 3, 4, 5]

    # create a thread pool with a maximum of 3 threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # submit each task to the executor
        futures = [executor.submit(worker, task) for task in tasks]

        # wait for all tasks to complete
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    print(f"Results: {results}")
