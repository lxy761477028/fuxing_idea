import requests
import threading
import time


t1 = time.time()

ls = "这东西本质上是以色列媒体的震惊体震惊！我国（这里指以色列）绝密情报部门精锐特工从远东带回绝密疫苗。……充分说明全世界人民对震惊体新闻都有刚性需求……实际上新冠疫苗已经上市了，只是还没有大范围铺开，前段时间报道浙江已经可以预约了，疫苗本体价格200元，注射费用28元，非常便宜。多说两句摩萨德早年以穷尽天涯海角追猎纳粹余孽和执行跨国突袭行动著称，由于打的多数是死老虎，再加上美国犹太人把持的媒体机器的渲染，名气很大，声望很高。这些年据说衰落的很厉害，被伊朗革命卫队重击了好几次。实际上，对于一个情报部门来说，最不需要的东西就是知名度……类似中情局，克格勃，摩萨德这类情报部门，经常因为行动搞出的动静太大，闹的满城风雨，实际上是手法拙劣，湿活干的太多造成的，特别是中情局，很难说现在的中情局对于美国国家利益来说究竟还是不是一个正资产。真正厉害的情报部门是类似冷战期间东德的情报部门斯塔西，它在冷战时期的知名度其实并不高，口号是“我们无处不在”但又极为低调，渗透能力极强又几乎不干湿活，很多信息是东欧剧变两德合并后才披露的，还创下了一项不可思议的记录——无人叛变。还有一些情报部门也很强，比如亚洲某大国的情报部门，你知道叫什么名字吗？反正我不知道"


num = 1000
def get_stock(code):
    url = 'http://192.168.0.114:6745/publish-model'
    data = {"query": ls}
    res = requests.get(url=url, json=data)
    print('%s\n' % res.text)

#多线程异步,加速抓取
#根据有几个股票代码,就创建几个线程

threads = [threading.Thread(target=get_stock, args=(code, )) for code in range(num)]
#Thread创建线程实例
'''
threads=[ ]
for code in codes:
    thread=threading.Thread(target=get_stock,args=(code, ))
    threads.append(thread)
'''
for t in threads:
    t.start()  #启动一个线程
for t in threads:
    t.join()  #等待每个线程执行结束

t2 = time.time()

print(str(t2-t1))




