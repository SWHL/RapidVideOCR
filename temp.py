import multiprocessing
import time


cond = multiprocessing.Condition()


def domywork(processid):
    print(processid, end='')


class myprocess(multiprocessing.Process):
    def __init__(self, nowprocessid, processid, jobcnt, processcnt, cond):
        multiprocessing.Process.__init__(self)  # *** 注意不要忘记初始化父进程 ***

        self.nowprocessid = nowprocessid
        self.processid = processid
        self.jobcnt = jobcnt
        self.processcnt = processcnt
        self.cond = cond

    def run(self) -> None:
        for i in range(self.jobcnt):
            with self.cond:
                while self.nowprocessid.value != self.processid:
                    self.cond.wait()

                # 控制轮到下一个进程（一共开了processcnt个进程，所以模processcnt）来执行打印
                # 注意：这里进程号要从1开始，即：myprocess(nowprocessid, i + 1, jobcnt, prccnt, cond)
                self.nowprocessid.value = (self.nowprocessid.value % self.processcnt) + 1

                # 处理进程的各自业务
                domywork(self.processid)

                # 通知其他所有进程
                self.cond.notify_all()


if __name__ == '__main__':
    mprclist = []
    jobcnt = 20
    prccnt = 5
    nowprocessid = multiprocessing.Value('i', 1)

    for i in range(prccnt):
        mprc = myprocess(nowprocessid, i + 1, jobcnt, prccnt, cond)  # 注意：cond对象必须传给进程类
        mprclist.append(mprc)
        mprc.start()

    for i in mprclist:
        i.join()

    print('\nfinished')