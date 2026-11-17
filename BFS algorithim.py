from collections import deque
# BFS alg
def bfs(maze,start,end):
    rows=len(maze)
    cols=len(maze[0])
    queue=deque([(start,[start])])
    visited={start}

    available_move=[
        (0,1),#right
        (1,0),# down
        (0,-1),#left
        (-1,0)#up
    ]
    while queue:
        (x,y),path=queue.popleft()
        if (x,y)==end:
            return path,visited

        for dx,dy in available_move:
            nx,ny=x+dx,y+dy
            if(0<=nx<rows
               and
               0<=ny<cols
               and
               maze[nx][ny]==0
               and
               (nx,ny) not in visited):
                visited.add((nx,ny))
                queue.append(((nx,ny),path+[(nx,ny)]))
    return None,visited



# maze

maze1 = [
    [0,0,0,1,0,0,0,0,0,0],
    [1,1,0,1,0,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,1,0,0,0],
    [1,1,1,1,1,0,1,1,1,0],
    [0,0,0,0,1,0,0,0,0,0],
    [0,1,1,0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,0,0,0]
]

maze2 = [
    [0,0,0,1,0,0,0,0,1,0,0,0,0,0,0],
    [1,1,0,1,0,1,1,0,1,0,1,1,1,1,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,0,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0],
    [1,1,1,0,1,1,1,1,1,1,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,1,0],
    [1,1,1,1,1,1,0,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,0,1,1,1,1,1,0,1,1,1,0],
    [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
    [1,1,0,1,1,1,1,1,0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

maze3 = [
    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
    [0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0],
    [0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0],
    [1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0],
    [1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
#choose
print("choose maze ")
print("1:maze10x10 ")
print("2:maze15x15 ")
print("3:maze21x21 ")

choose=input("enter your chooes\n")
if choose=="1":
    maze=maze1
elif choose=="2":
    maze=maze2
elif choose=="3":
    maze=maze3
else:
    print("false input")
    exit()

# Display Maze 

rows = len(maze)
cols = len(maze[0])

print("\nYour Maze :")

for i in range(rows):
    row_cells = []

    for j in range(cols):
        if maze[i][j] == 0:
            if i >=10 and j>=10:
                row_cells.append(f"({i},{j})")
            elif i>=10 :
                row_cells.append(f"({i}, {j})")
            elif j>=10 :
                row_cells.append(f"( {i},{j})")
            else :
                row_cells.append(f"( {i}, {j})")
                
        else:
            row_cells.append(f"#######")

    print(" ".join(row_cells))

rows=len(maze)
cols=len(maze[0])
#choose the start point
print("start pos")
sx=int(input("row : "))
sy=int(input("col : "))
start=(sx,sy)

#choose the end point
print("end pos")
ex=int(input("row : "))
ey=int(input("col : "))
end=(ex,ey)

#check point
if sx < 0 or sx >= rows or sy < 0 or sy >= cols:
    print("false start")

elif(ex < 0 or ex >= rows or ey < 0 or ey >= cols):
    print("false end")

elif (maze[sx][sy] == 1):
    print("start in the wall")
    print("start in the wall")
elif(maze[ex][ey] == 1):
    print("end in the wall")

else:
    #run t BFS alg
    path,visited=bfs(maze,start,end)
    print("number visit node =",len(visited)-1)
    if path:   
        print("the path ->\n")
        print(path)
        print("number off steps =",len(path)-1)
        print(" \n final path")
        for i in range(rows):
            for j in range(cols): 
                if(i,j)==start:
                    print("S",end=" ")
                elif(i,j)==end:
                    print("G",end=" ")
                elif maze[i][j] == 1:
                    print("#", end=" ")
                elif (i, j) in path:
                     idx = path.index((i, j))
                     next_i, next_j = path[idx + 1]

                     if next_j == j + 1:
                        print("→", end=" ")
                     elif next_i == i + 1:
                        print("↓", end=" ")
                     elif next_i == i - 1:
                        print("↑", end=" ")
                     elif next_j == j - 1:
                        print("←", end=" ")
                else:
                    print(".",end=" ")
            print("\n")

    else:
        print("\nNo Path Found!")            




    
