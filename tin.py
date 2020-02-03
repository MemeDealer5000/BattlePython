n, s = input().split(" ")
n = int(n)
s = int(s)
pigeons_speed = input().split(" ")
speed_list = [int(i) for i in pigeons_speed]
offset_count = 0
for i in range(n):
    for j in range(i):
        i_time = int(s/speed_list[i]) + i
        j_time = int(s/speed_list[j]) + j
        if i_time < j_time:
            offset_count += 1
print(offset_count)
