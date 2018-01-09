def pour_problem(X,Y,goal,start=(0,0)):
    #X, Y are the capacity of two glasses
    if goal in start:
        return [start]

    explored=set()
    frontiers=[[start]]

    while frontiers:
        route=frontiers.pop(0)
        (x,y)=route[-1]

        for (state,action) in next_step(x,y,X,Y).items():
            if state not in explored:
                explored.add(state)
                route2=route+[action,state]

                if goal in state:
                    return route2
                else:
                    frontiers.append(route2)


    return Fail

Fail=[]

def next_step(x,y,X,Y):
    assert x<=X and y<=Y
    return {((0,x+y) if x+y<Y else (x-(Y-y),Y)):'pull from x to y',
            ((x+y,0) if x+y<X else (X,y-(X-x))):'pull from y to x',
            (x,Y):'fill y',
            (X,y):'fill x',
            (0,y):'empty x',
            (x,0):'empty y',
            }
            

print pour_problem(9,4,6)
