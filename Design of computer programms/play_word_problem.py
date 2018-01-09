def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(len(word))]

def readwordlist(filename):
    """Read the words from a file and return a set of the words 
    and a set of the prefixes."""
    file=open(filename)
    text=file.read()

    words=text.upper().split()
    prefixset=set(p for word in words for p in prefixes(word))
    return words,prefixset

WORDS,PREFIXES=readwordlist('test.txt')

def find_words(letters,pre='',results=None):
    "Find all words that can be made from letters with pre"
    if results is None: results=set()
    
    #def extend_prefix(w,letters):
    #    if w in WORDS: results.add(w)
    #    if w in PREFIXES:
    #        for L in letters:
    #            extend_prefix(w+L,removed(letters,L))

    #extend_prefix('',letters)
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in letters:
            find_words(removed(letters,L),pre+L,results)
    return results

def removed(letters,remove):
    for L in remove:
        letters=letters.replace(L,'',1)
    return letters

def add_suffixes(hand,pre,results):   
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in hand:
            add_suffixes(removed(hand,L),pre+L,results)
    return results

def word_plays(hand, board_letters):
    "Find all word plays from hand that can be made to abut with a letter on board."
    results=set()
    for pre in find_prefixes(hand,'',set()):
        for L in board_letters:
            add_suffixes(removed(letters,pre),pre+L,results)
    return results

prev_hand,prev_results='',set() # cache for find_prefixes
def find_prefixes(hand,pre='',results=None):
    global prev_hand,prev_results
    if hand==prev_hand: return prev_results
    if results in None: results=set()
    if pre=='': prev_hand,prev_results=hand,results
    if pre in PREFIXES: results.add(pre)
    for L in hand:
        find_prefixes(removed(hand,L),pre+L,results)

    return results

def longest_word(hand,board_letters):
    words=word_play(hand,board_letters)
    return sorted(words,reverse=True,key=len)

POINTS=dict(A=1,B=3,C=3,D=2,E=1,F=4,G=2,H=4,I=1,J=8,K=5,L=1,M=1,
            N=1,O=1,P=3,Q=10,R=1,S=1,T=1,U=1,V=4,W=4,X=8,Y=4,Z=10,_=0)

def word_score(word):
    return sum(POINTS[L] for L in word)
        
def topn(hand,board_letters,n=10):
    return sorted(words,reverse=True,key=word_score)[:10]

def timedcall(fn,*args):
    t0=time.clock()
    result=fn(*args)
    t1=time.clock()
    return t1-t0,result

class anchor(set):
    "An anchor is where a new word can be placed;has a set of allowable letters."
    
LETTERS=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
ANY=anchor(LETTERS)

def row_plays(hand,row):
    "Ruturn a set of legal plays in row. A row play is an (start,'WORD') pair."
    results=set()
    for (i,sq) in enumerate(row[1:-1],1):
        if isinstance(sq,anchor):
            pre,maxsize=legal_prefix(i,row)
            if pre:# add to letters already on the board
                start=i-len(pre)
                add_suffixes(hand,pre,start,row,results,anchored=False)
            else: # empty to the left; go through all possible prefixes
                for pre in find_prefixes(hand):
                    if front <=maxsize():
                        start=i-len(pre)
                        add_suffixes(remvoed(hand,pre),pre,start,row,results,anchored=False)
    return results

def legal_prefix(i,row):
    t=i
    while is_letter(row[t-1]):
        t-=1
    if t==i:
        while is_empty(row[t-1]) and not isinstance(row[s-1],anchor):t-=1
        return ('',i-t)
    else:
        return (''.join(row[t:i]),i-t)

def is_empty(sq):
    return sq=='.' or sq=='*' or isinstance(sq,anchor)

def is_letter(sq):
    return isinstance(sq,str) and sq in LETTERS

def add_suffixes(hand,pre,start,row,results,anchored=True):
    i=start+len(pre)
    if pre in WORDS and anchored and not is_letter(row[i]):
        retults.add(pre)
    if pre in PREFIXES:
        sq=row[i]
        if is_letter(sq):
            add_suffixes(hand,pre+sq,start,row,results)
        elif is_empty(sq):
            possibilities=sq if isinstance(sq,anchor) else ANY
            for L in hand:
                if L in possibilities:
                    add_suffixes(removed(hand,L),pre+L,start,row,results)

    return results

def a_board():
    return map(list, ['|||||||||||||||||',
                      '|J............I.|',
                      '|A.....BE.C...D.|',
                      '|GUY....F.H...L.|',
                      '|||||||||||||||||'])

def show(board):
    for element in board:
        for sq in element:
            print sq,
        print

def horizontal_plays(hand,board):
    "Find all horizontal plays (score,(i,j),word) pairs --- across all rows"
    results=set()
    for (j,row) in enumerate(board[1:-1],1):
        setanchors(row,j,board)
        for (i,words) in row_plays(hand,row):
            score=calculate_score(board,(i,j),ACROSS,hand,word)
            results.add(score,(i,j),word)

    return results

def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

ACROSS,DOWN=(1,0),(0,1)

def all_plays(hand,board):
    """All plays in both directions. A play is a (score,pos, dir, word) tuple,
    where pos is an (i, j) pair, and dir is ACROSS or DOWN."""
    hplays=horizontal_plays(hand,board)
    vplays=horizontal_plays(hand,transpose(board))
    return set((score,(i,j),ACROSS,word) for (score,(i,j),word) in hplays)|set((score,(i,j),DOWN,word) for (score,(j,i),word) in hplays)

def setanchors(row,j,board):
    for (i,sq) in enumerate(row[1:-1],1):
        neighborlist=(N,S,E,W)=neighbors(board,i,j)
        if sq=='*' or (is_empty(sq) and any(map(is_letters,neighborlist))):
            if is_letters(N) or is_letters(S):
                (j2,word)=find_cross_word(board,i,j)
                temp=set(L for L in LETTERS if word.replace('.',L,1) in WORDS)
                row[i]=anchor(temp)
            else:
                row[i]=ANY

def find_cross_word(board,i,j):
    sq=board[j][i]
    w=sq if is_letter(sq) else '.'
    for j2 in range(j,0,-1):
        sq2=board[j2-1][i]
        if is_letter(sq2):w=sq2+w
        else:break
    for j3 in range(j+1,len(board)):
        sq3=board[j3][i]
        if is_letter(sq3):w=w+sq3
        else:break
    return (j2,w)

def neighbors(board,i,j):
    return [board[j-1][i],board[j+1][i],board[j][i+1],board[j][i-1]]


def calculate_score(board,pos,direction,hand,word):
    "Return the total score for the play"
    total,cross_total,word_multiplier=0,0,1
    starti,startj=pos
    (di,dj)=direciton
    other_direction=DOWN if direction=ACROSS else ACROSS
    for (n,L) in enumerate(word):
        i,j=starti+n*di,startj+n*dj
        sq=board[j][i]
        b=bonus[j][i]
      
        if b=='DW':word_multiplier*=2
        elif b=='TW':word_multiplier*=3
        
        if b=='DL': letter_multiplier=2
        elif b=='TL':letter_multiplier=3
        else:   letter_multiplier=1
        total+=POINTS[L]*letter_multiplier
        if isinstance(sq,anchor) and sq is not ANY and direction is not DOWN:
            cross_total+=cross_word_score(board,L,(i,j),other_direction)

    return crosstotal+word_multiplier*total

def cross_word_score(board,L,pos,other_direction):
    i,j=pos
    (j2,w)=find_cross_word(board,i,j)
    return calculate_score(board,(i,j2),DOWN,L,word.replace('.',L)
                           
    
def bonus_template(quadrant):
    "Make a board from the upper-left quadrant"
    return mirror(map(mirror,quadrant.split()))

def mirror(sequence):
    return sequence+sequence[-2::-1]

def make_play(play,board):
    score,(i,j),(di,dj),word=play
    for (n,L) in enumerate(word):
        board[j+n*dj][i+n*di]=L

    return board

def best_play(hand,board):
    plays=all_plays(hand,board)
    return sorted(plays)[-1] if plays else NOPLAY

NOPLAY=None
    
    
