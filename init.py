from faker import Faker


def init_files(dir, n, k):
    for i in range(n):
        f = Faker()
        with open(f"{dir}/{i}.txt", "w") as fp:
            for _ in range(k):
                fp.write(f.text())


if __name__ == "__main__":
    init_files("./out", 1000, 4)
