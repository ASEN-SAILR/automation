from multiprocessing import Process
import time

def main():
    process = Process(target=printt)
    process.start()
    # time.sleep(5)
    # print(process.is_alive())
    if process.is_alive():
        process.terminate()
    time.sleep(2)
    print(process.is_alive())

def printt():
    t = time.time()
    while True:
        if time.time()-t>1:
            t = time.time()
            print('Hello\n')

if __name__ == "__main__":
    main()














