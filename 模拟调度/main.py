import random

class PCB:
    def __init__(self, pid, priority, arr_time, all_time, cpu_time, start_block, block_time, state):  ##初始化进程
        self.pid = pid  # 进程名
        self.priority = priority  # 进程优先度
        self.arr_time = arr_time  # 进程到达时间
        self.all_time = all_time  # 进程还需运行时间
        self.cpu_time = cpu_time  # 进程已运行时间
        self.start_block = start_block  # 进程开始阻塞时间
        self.block_time = block_time  # 进程已阻塞时间
        self.state = state  # 进程状态

    def output(self):  # hrrn输出
        print("进程" + str(self.pid), "优先级：" + str(self.priority), "到达时间:" + str(self.arr_time),
              "还需运行时间:" + str(self.all_time), "已运行时间:" + str(self.cpu_time),
              "开始阻塞时间：" + str(self.start_block), "阻塞时间：" + str(self.block_time), "状态：" + self.state)

    def Output(self):  # sjf fcfs输出
        print("进程" + str(self.pid), "到达时间:" + str(self.arr_time),
              "还需运行时间:" + str(self.all_time), "已运行时间:" + str(self.cpu_time))

    def toBlock(self):  # 将状态置为Block
        self.state = "Block"

    def toRun(self):  # 将状态置为Run
        self.state = "Run"

    def toFinish(self):  # 将状态置为Finish
        self.state = "Finish"

    def toReady(self):  # 将状态置为Ready
        self.state = "Ready"

    def running(self):  # 进程运行时状态变化
        self.all_time -= 1
        self.cpu_time += 1

    def toBlocking(self):  # 进程将要开始阻塞的状态变化
        if self.start_block > 0:
            self.start_block -= 1

    def blocking(self):  # 进程阻塞时的状态变化
        if self.block_time > 0:
            self.block_time -= 1
        self.priority += 1


def init(num):  # 初始化进程，生成四个进程并按到达时间将它们放入列表list1
    list1 = []
    for i in range(num):
        list1.append(PCB(str(i), random.randint(1, 10), random.randint(10, 15),
                         random.randint(1, 10), 0, random.randint(5, 10), random.randint(1, 10), "Ready"))
    for i in range(len(list1) - 1):  # 对list里的进程按到达时间进行排序
        for j in range(i + 1, len(list1)):
            if list1[i].arr_time > list1[j].arr_time:
                list1[i], list1[j] = list1[j], list1[i]
    return list1


def fcfs(list1):  # first come first service 先来先服务
    time = 0
    while 1:
        print("系统当前时间:", time)
        if time >= list1[0].arr_time:
            list1[0].running()
            list1[0].Output()
            if list1[0].all_time == 0:
                print("进程" + list1[0].pid + "执行完毕,周转时间：" + str(time - list1[0].arr_time + 1) + "\n")
                list1.remove(list1[0])
        time += 1
        if not list1:
            break


def sjf(list1):  # short test job first抢占式短作业优先
    list2 = []  # 就绪队列
    time = 0
    while 1:
        len_list2 = len(list2)
        print("系统当前时间:", time)
        if list1:
            i = 0
            while 1:  # 将进程放入就绪队列，就绪队列的第一个是正在执行的进程
                if time == list1[i].arr_time:
                    list2.append(list1[i])
                    list1.remove(list1[i])
                    pid = list2[0].pid  # 获取就绪队列第一个进程的进程ID
                    i -= 1
                i += 1
                if i >= len(list1):
                    break
        if len(list2) >= 2 and len(list2) != len_list2:  # 如果队列中有超过两个作业，就判断就绪队列中还需时间最短的作业
            len_list2 = len(list2)
            for i in range(len(list2) - 1):
                for j in range(i + 1, len(list2)):
                    if list2[i].all_time > list2[j].all_time:
                        list2[i], list2[j] = list2[j], list2[i]
        if list2:  # 执行过程
            if pid != list2[0].pid:  # 如果正在执行的进程改变，则发生抢占
                print("发生抢占，进程" + list2[0].pid + "开始执行")
                pid = list2[0].pid
            list2[0].running()
            list2[0].Output()
            if list2[0].all_time == 0:
                print("进程" + list2[0].pid + "执行完毕,周转时间：" + str(time - list2[0].arr_time + 1) + "\n")
                list2.remove(list2[0])
                if list2:
                    pid = list2[0].pid
        time += 1
        if not list2 and not list1:
            break


def hrrn(list1):  # 动态优先度最高优先
    list2 = []  # 就绪队列
    list3 = []  # 阻塞队列
    time = 0
    while 1:
        print("系统当前时间:", time)
        if list1:
            i = 0
            while 1:  # 将进程放入就绪队列
                if time == list1[i].arr_time:
                    list2.append(list1[i])
                    list1.remove(list1[i])
                    pid = list2[0].pid
                    i -= 1
                i += 1
                if i >= len(list1):
                    break
        for i in range(len(list2) - 1):  # 将就绪队列的进程按优先级大小排列
            for j in range(i + 1, len(list2)):
                if list2[i].priority < list2[j].priority:
                    list2[i].toReady()
                    list2[i], list2[j] = list2[j], list2[i]
        if list2:  # 执行过程
            if pid != list2[0].pid:
                print("发生抢占，进程" + list2[0].pid + "开始执行")
                pid = list2[0].pid
            if list2[0].start_block > 0 or list2[0].block_time <= 0:
                list2[0].toRun()
                list2[0].running()
                list2[0].toBlocking()
            for i in range(1, len(list2)):
                list2[i].priority += 1
                list2[i].toBlocking()
        if list3:  ##阻塞队列
            for i in list3:
                i.blocking()

        for i in list2:
            i.output()
        for i in list3:
            i.output()

        if list2:  # 当进程开始阻塞时间为0，将进程放入阻塞队列
            i = 0
            while 1:
                if list2:
                    if list2[i].start_block == 0 and list2[i].block_time != 0:
                        print("进程" + list2[i].pid + "开始阻塞，进入阻塞队列")
                        list2[i].toBlock()
                        list3.append(list2[i])
                        list2.remove(list2[i])
                        i -= 1
                i += 1
                if i >= len(list2):
                    break

        if list3:  # 当进程阻塞时间为0，将进程放入就绪队列
            i = 0
            while 1:
                if list3[i].block_time == 0:
                    print("进程" + list3[i].pid + "阻塞结束，进入就绪队列")
                    list3[i].toReady()
                    list2.append(list3[i])
                    list3.remove(list3[i])
                    pid = list2[0].pid
                    i -= 1
                i += 1
                if i >= len(list3):
                    break

        if list2:  # 进程执行完毕则移出就绪队列
            if list2[0].all_time <= 0:
                list2[0].toFinish()  # 设置进程状态到完成
                print("进程" + list2[0].pid + "执行完毕，周转时间：" + str(time - list2[0].arr_time + 1),
                      "状态：" + list2[0].state + "\n")
                list2.remove(list2[0])
                if list2:
                    pid = list2[0].pid

        time += 1
        if not (list1 or list2 or list3):
            break


if __name__ == "__main__":
    while 1:
        n = input("1、first come first service \n2、short test job first \n3、highest response ratio next\ninput:")
        if n == "1":
            list1 = init(4)
            for i in list1:
                i.Output()
            fcfs(list1)
        elif n == "2":
            list1 = init(4)
            for i in list1:
                i.Output()
            sjf(list1)
        elif n == "3":
            list1 = init(4)
            for i in list1:
                i.output()
            hrrn(list1)
        else:
            print("输入错误，请重新输入！")
