"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming. 
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""

import itertools

def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    ## your code here; you are free to define additional functions if needed
    orderings=list(itertools.permutations([1,2,3,4,5],5))
    orderings2=list(itertools.permutations([1,2,3,4,5],4))
    for (Hamming, Knuth, Minsky, Simon, Wilkes) in orderings:
        if Knuth==Simon+1: #6
            for (laptop,droid,tablet,iphone) in orderings2:
                if (laptop==3    #1
                    and (iphone==2 or tablet==2)  #12
                    and tablet!=5):    #8   
                    for (programmer,writer,manager,designer) in orderings2:
                        if (Wilkes!=programmer     #2
                            and designer!=4   #7
                            and ((Wilkes==programmer and Hamming==droid) or (Wilkes==droid and Hamming==programmer)) #3
                            and Minsky != writer  #4
                            and Knuth !=manager
                            and tablet!=manager   #5
                            and designer != droid   #9
                            and Knuth == manager+1  #10
                            and ((laptop==1 and Wilkes==writer) or (Wilkes==1 and laptop==writer))):   #11
                            return  sorted(['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes'],key=eval)


print logic_puzzle()
