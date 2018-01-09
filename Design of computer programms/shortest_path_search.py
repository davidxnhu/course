def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    # your code here
    
    if is_goal(start):
        return [start]
    
    explored=set()
    frontier=[[start]]
    while frontier:
        path=frontier.pop(0)
        current_state=path[-1]
        
        for (state,action) in successors(current_state).items():
            if state not in explored:
                explored.add(state)
                path2=path+[action,state]
                
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    
    
    return Fail
    
Fail=[]


def mc_problem2(start=(3, 3, 1, 0, 0, 0), goal=None):
    if goal is None:
        def goal_fn(state): return state[:3]==(0,0,0)
    else:
        def goal_fn(state): return state==goal
    return shortest_path_search(start,csuccessors,goal_fn)


def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors."""
    M1, C1, B1, M2, C2, B2 = state
    # your code here
    if C1>M1 or C2>M2:
        return {}
    
    items={}
    if C1>=1 and B1>=1:
        items[(M1,C1-1,B1-1,M2,C2+1,B2+1)]='C->'
    if M1>=1 and B1>=1:
        items[(M1-1,C1,B1-1,M2+1,C2,B2+1)]='M->'
    if M1>=2 and B1>=1:
        items[(M1-2,C1,B1-1,M2+2,C2,B2+1)]='MM->'
    if M1>=1 and C1>=1 and B1>=1:
        items[(M1-1,C1-1,B1-1,M2+1,C2+1,B2+1)]='MC->'
    if C1>=2 and B1>=1:
        items[(M1,C1-2,B1-1,M2,C2+2,B2+1)]='CC->'
    if C2>=1 and B2>=1:
        items[(M1,C1+1,B1+1,M2,C2-1,B2-1)]='<-C'
    if M2>=1 and B2>=1:
        items[(M1+1,C1,B1+1,M2-1,C2,B2-1)]='<-M'
    if M2>=2 and B2>=1:
        items[(M1+2,C1,B1+1,M2-2,C2,B2-1)]='<-MM'
    if M2>=1 and C2>=1 and B2>=1:
        items[(M1+1,C1+1,B1+1,M2-1,C2-1,B2-1)]='<-MC'
    if C2>=2 and B2>=1:
        items[(M1,C1+2,B1+1,M2,C2-2,B2-1)]='<-CC'
    
    return items
