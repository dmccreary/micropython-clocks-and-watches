import time

now = time.localtime()
label = ('year', 'month', 'mday', 'hour', 'minute', 'second', 'weekday', 'yearday')
for i in range(8):
    print(label[i], ':', now[i])

print()
print("Date: {}/{}/{}".format(now[1], now[2], now[0]))
print("Time: {}:{}".format(now[3], now[4]))