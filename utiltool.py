import string
import random
import threading
import queue as q



# 生成密码本
def makePwdtxt(obs:q.Queue):
    while True:
        num, repeat = obs.get()
        pwd_lst = []
        for _ in range(num):
            letter = ""
            for i in range(repeat):
                letter += random.choice(passwordrange)
            if letter not in pwd_lst:
                pwd_lst.append(letter)

        # 保存在文件中，追加
        dic = open("data/password.txt", 'a')
        # i 是元组
        for i in pwd_lst:
            dic.write(i)
            dic.write("\n")
        dic.close()
        print("线程：",threading.current_thread().name)
        print("{}  位密码已经生成。".format(repeat))



# 读取密码本
def readPwd():
    path = 'data/password.txt'
    with open(path, 'r') as fp:
        lines = fp.readlines()
        lines = [line.strip('\n') for line in lines]
    return lines


if __name__ == "__main__":
    lock = threading.Lock()
    obs = q.Queue()
    pwd_num = 100000
    stri = r"!@#$%^&*.\|[]{};'?/-_(),:+=><`~"
    passwordrange = string.digits + string.ascii_letters + stri
    for i in range(8, 17):
        obs.put((pwd_num, i))
    with lock:
        # 启动5个线程
        for j in range(5):
            t = threading.Thread(target=makePwdtxt, args=(obs,), name=f'makePwd{j}号')
            t.start()


