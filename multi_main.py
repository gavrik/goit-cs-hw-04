import multiprocessing as mp
from time import sleep

#
# the several functions will be imported from th_main file
#

from th_main import consolidation, list_files, find_word


def worker(results_data, mid, files_list, words_list, path):
    print("start process", mid)
    res = {}
    for f in files_list:
        res = find_word(f"{path}/{f}", words_list)
        # print(f, res)
        results_data.put(res)


def workflow(nt, files_list, words_list, path):
    process = []
    results_data = mp.Queue()
    for p in range(nt):
        pid = mp.Process(
            target=worker,
            name=str(p),
            args=(results_data, p, files_list[p], words_list, path))
        pid.start()
        process.append(pid)

    # sleep(2)

    while len(process) > 0:
        for w in process:
            if not w.is_alive():
                print("Worker is dead: ", w.name)
                process.remove(w)
            else:
                print("Worker is still alive: ", w.name)
        sleep(1)
    return results_data


if __name__ == "__main__":

    path = "./out"  # folder where files located
    words = ["the", "it", "close"]  # words for searching
    n = 4  # Threads

    lf = list_files(n, path)
    # print(lf)
    # exit(1)
    res = workflow(n, lf, words, path)

    gres = {}
    for w in words:
        gres[w] = 0

    while not res.empty():
        # print(res.get())
        consolidation(res.get(), gres)

    print(gres)
