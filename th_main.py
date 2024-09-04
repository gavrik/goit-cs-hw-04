from threading import Thread
from time import sleep
import os


def list_files(n, path):
    dl = os.listdir(path)
    k, m = divmod(len(dl), n)
    return [dl[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


def find_word(file, words):
    res = {}

    for w in words:
        res[w] = 0

    with open(file, 'r') as fp:
        for line in fp:
            for w in words:
                if w in line:
                    res[w] += 1

    return res


def worker(results_data, thid, files_list, words_list, path):
    print("start thread:", thid)
    res = {}
    gres = {}
    for w in words_list:
        gres[w] = 0
    for f in files_list:
        res = find_word(f"{path}/{f}", words_list)
        # print(f, res)
        consolidation(res, gres)
    results_data[thid] = gres
    # return gres


def consolidation(data, gdata):
    for k, v in data.items():
        gdata[k] += v


def workflow(nt, files_list, words_list, path):
    threads = []
    results_data = [None] * nt
    for t in range(nt):
        th = Thread(
            target=worker,
            name=str(t),
            args=(results_data, t, files_list[t], words_list, path))
        th.start()
        threads.append(th)

    # sleep(2)

    while len(threads) > 0:
        for w in threads:
            if not w.is_alive():
                print("Worker is dead: ", w.name)
                threads.remove(w)
            else:
                print("Worker is still alive: ", w.name)
        sleep(1)
    return results_data


if __name__ == "__main__":
    # r = find_word("./out/1.txt", ["open", "close", "it"])
    # print(r)

    path = "./out"  # folder where files located
    words = ["the", "it", "close"]  # words for searching
    n = 4  # Threads

    lf = list_files(n, path)
    # print(lf)
    # exit(1)
    res = workflow(n, lf, words, path)
    # print(res)

    gres = {}
    for w in words:
        gres[w] = 0

    for r in res:
        consolidation(r, gres)

    print(gres)
