N=8

def successors(state):
    results={}
    occupied=()
    for (c,squares) in state:
        if c!='@':
            occupied+=squares
    
    for (num,(c,squares)) in enumerate(state):
        if c !='@' and c!='|': # check if it is a car
            car_length=len(squares)
            if squares[0]/N == squares[1]/N:   # check if it is horizontal
                i=-1
                new_state=state
                while (squares[0]+i) not in occupied: # check if it can move
                    new_state=replace(new_state,num,car_length,-1)
                    results[new_state]=(c,i)
                    i-=1
                i=1
                new_state=state
                while (squares[car_length-1]+i) not in occupied:
                    new_state=replace(new_state,num,car_length,1)
                    results[new_state]=(c,i)
                    i+=1
            
            else:
                i=-1
                new_state=state
                while (squares[0]+i*N) not in occupied:
                    new_state=replace(new_state,num,car_length,-N)
                    results[new_state]=(c,i*N)
                    i-=1
                i=1
                new_state=state
                while (squares[car_length-1]+i*N) not in occupied:
                    new_state=replace(new_state,num,car_length,N)
                    results[new_state]=(c,i*N)
                    i+=1
    return results
    
def replace(state,num,car_length,i):
    "update state with the legal action, sign of i determines the direction"
    temp=list(state)
    (c,squares)=temp[num]  # take our squares and convert to list
    temp2=list(squares)
    if i>0:
        temp2=temp2[1:]+[temp2[car_length-1]+i]
    if i<0:
        temp2=[temp2[0]+i]+temp2[:-1]
    
    temp[num]=(c,tuple(temp2))
    return tuple(temp)

def show(state, N=N):
    "Print a representation of a state as an NxN grid."
    # Initialize and fill in the board.
    board = ['.'] * N**2
    for (c, squares) in state:
        for s in squares:
            board[s] = c
    # Now print it out
    for i,s in enumerate(board):
        print s,
        if i % N == N - 1: print

def is_goal(state):
    d=dict(state)
    return set(d['*'])&set(d['@'])

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []

def solve_parking_puzzle(start, N=N):
    """Solve the puzzle described by the starting position (a tuple 
    of (object, locations) pairs).  Return a path of [state, action, ...]
    alternating items; an action is a pair (object, distance_moved),
    such as ('B', 16) to move 'B' two squares down on the N=8 grid."""
    return shortest_path_search(start,successors,is_goal)

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]


def locs(start, n, incr=1):
    "Return a tuple of n locations, starting at start and incrementing by incr."
    result=(start,)
    while n>1:
        start+=incr
        result+=(start,)
        n-=1
    return result


def grid(cars, N=N):
    """Return a tuple of (object, locations) pairs -- the format expected for
    this puzzle.  This function includes a wall pair, ('|', (0, ...)) to 
    indicate there are walls all around the NxN grid, except at the goal 
    location, which is the middle of the right-hand wall; there is a goal
    pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
    tuple of pairs like ('*', (26, 27)). The return result is a big tuple
    of the 'cars' pairs along with the walls and goal pairs."""
    result=(('@',(N-1+(N-1)/2*N,)),)
    for (c,squares) in cars:
        result+=((c,squares),)
    pos=tuple([i for i in range(N)])
    for i in range(N,N*(N-1)):
        if (i%N==0 or i%N==N-1) and i!=N-1+(N-1)/2*N:
            pos+=(i,)
    pos+=tuple([i for i in range(N*(N-1),N*N)])
    result+=(('|',pos),)

    return result
    

puzzle1 = (
 ('@', (31,)),
 ('*', (26, 27)), 
 ('G', (9, 10)),
 ('Y', (14, 22, 30)), 
 ('P', (17, 25, 33)), 
 ('O', (41, 49)), 
 ('B', (20, 28, 36)), 
 ('A', (45, 46)), 
 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
        40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

puzzle2 = grid((
    ('*', locs(26, 2)),
    ('B', locs(20, 3, N)),
    ('P', locs(33, 3)),
    ('O', locs(41, 2, N)),
    ('Y', locs(51, 3))))

puzzle3 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 3, N)),
    ('P', locs(36, 3)),
    ('O', locs(45, 2, N)),
    ('Y', locs(49, 3))))

puzzle4 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2)),
    ('S', locs(51, 3))))


print path_actions(solve_parking_puzzle(puzzle4))

