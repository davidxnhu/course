def mc_problem(start=(3,3,1,0,0,0),goal=None):
    if goal == start:
        return [start]

    explored=set()
    frontier=[[start]]

    while frontier:
        path=frontier.pop(0)
        current_state=path[-1]

        for (state,action) in csuccessors(current_state).items():
            M1,C1,B1,M2,C2,B2=state
            if state not in explored:
                explored.add(state)
                path2=path+[action,state]
                if goal == start or (M1==0 and C1==0 and B1==0):
                    return path2
                else:
                    frontier.append(path2)

    return Fail

Fail=[]





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


print mc_problem((3,1,1,0,0,0))
