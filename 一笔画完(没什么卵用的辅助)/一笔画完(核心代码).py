# org:起点坐标，[行，列]。count:统计走了多少网格。record:记录走过的方向
def dfs(org, count, record):
    if marked[org[0]][org[1]]:
        # 如果count == num表示已经全部走完
        if count == num:
            global path
            path = record
            return True
        else:
            for k, v in d.items():
                o_x, o_y = org[0], org[1]
                x, y = v[0], v[1]
                o_x += x
                o_y += y
                if 0 <= o_y < l_x and 0 <= o_x < h_y:
                    marked[org[0]][org[1]] = 0
                    if dfs([o_x, o_y], count + 1, record + k):
                        return True
                    else:
                        # 不满足条件的时候会进行回溯，需要把已经改过的标记改过来
                        marked[org[0]][org[1]] = 1
    return False

if __name__ == '__main__':
    # 用于接收深度优先搜索得到的路径结果
    path = None
    # 移动的方向，u向上，d向下，l向左，r向右。ps:[行，列]
    d = {'u': [-1, 0], 'd': [1, 0], 'l': [0, -1], 'r': [0, 1]}
    h_y = int(input("请输入有几行："))
    l_x = int(input("请输入有几列："))
    blank = int(input("请输入有几个空白格："))
    # 可以走的方格数
    num = h_y * l_x - blank
    # 初始化整个网格，1代表可以走或未走过，0表示不可以走或已走过
    marked = [[1 for _ in range(l_x)] for _ in range(h_y)]
    origin = [int(i) - 1 for i in input("请输入起点坐标(格式：行+空格+列)：").split()]
    for j in range(blank):
        bl = [int(i) - 1 for i in input("请输入第{}个空格坐标(格式：行+空格+列)：".format(j + 1)).split()]
        # 将网格中的空白格标记为不可走
        marked[bl[0]][bl[1]] = 0
    dfs(origin, 1, '')
    for p in path:
        if p == 'u':
            print("u↑", end=' ')
        elif p == 'd':
            print("d↓", end=' ')
        elif p == 'l':
            print("l←", end=' ')
        else:
            print("r→", end=' ')
