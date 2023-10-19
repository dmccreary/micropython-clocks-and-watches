from time import localtime

now = localtime()
print(now)

print('year:',   now[0])
print('month:',  now[1])
print('day:',    now[2])
print('hour:',   now[3])
print('minute:', now[4])
print('sec:',    now[5])
print('day of year:', now[6])
