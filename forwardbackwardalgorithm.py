# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 12:19:12 2018

@author: Mercedes
"""

def forwardAlgorithm(ObservedEmissions,States,emissiontable,initialvector,transitiontable):
    
    #induction
    """
    Purpose: Calculates the forward accumulator for each state at the first timecount
    Returned data form: dictionary (forward) key/value pairs
    The key is (timepoint,state); the value is the forward accumulator of the given state at the given time.
    
    The 'TimeCount' variable keeps track of what timepoint the algorithm is at. The first timepoint is one, so the 'timecount' is set at one for induction.
    
    The list containing the states (States) starts its index numbering at zero, so the count variable serving to reference the state list's index (statecount) starts at zero.  
    
    The dictionary of emission probabilities (emissiontable)'s keys (oekey) are in the form emissionPOS. 
    Because the index of the list of emissions (ObservedEmissions) starts at zero, but timecount starts at one, the emission's index is the timecount-1.
    The values are the probability of the emission given the POS, in decimal form.
    
    The dictionary of transition probabilities (transitiontable)'s keys are in the form PreviousstateCurrentstate.
    The values are the probability of the of the state the accumulator is at given the previous state being observed, in decimal form.
    """
    
    forward = {}
    TimeCount = 1
    statecount = 0
    OElength = len(ObservedEmissions)
    
    for state in States:
        oekey = ObservedEmissions[TimeCount-1]+state
        emissionprob = emissiontable[oekey]
        forward[TimeCount,state] = emissionprob*initialvector[statecount]
        statecount += 1
    #iteration
    """
    Now it's time to make the second, third, ....n-1, n timepoint forward accumulators.
    The forward accumulator for a given state at a given timepoint calculated as follows:
        For each state at the previous timepoint:
            Multiply the forward accumulator by the transition probability [previous timepoint state to current state] and the emission probability [observed emission given current state]
        Sum over the results of the multiplication just performed.
    The forward accumulators are added to the dictionary of forward accumulators (forward).
    
    The TimeCount variable keeps track of the current timepoint. The iteration begins at timepoint 2, so TimeCount starts at 2.
    When the forward accumulators of all states at the given timepoint have been calculated, 1 is added to TimeCount so the next timepoint's forward accumulators can be calculated.
    
    """
    
    TimeCount = 2

    for step in ObservedEmissions:
        while TimeCount <= OElength:
            for State in States:
                oekey = (ObservedEmissions[TimeCount-1])+State
                emissionprob = emissiontable[oekey]
                forward[TimeCount,State] = 0
                for previousstate in States:
                    ttkey = previousstate+State
                    transitionprob = transitiontable[ttkey]
                    forward[TimeCount,State] += forward[TimeCount-1,previousstate]*transitionprob*emissionprob
                
            TimeCount += 1
           #print("Starting timecount",timecount,"\n")
            
    #termination
    """
    Now that all forward accumulators have been calculated, we can calculate the probability of having observed all emissions observed in the sentence.
    This is done by multipling all of the forward accumulators together.
    The variable ProbabilityOfObservedEmissions represents, well, the probability of the string of observed emissions.
    ProbabilityOfObservedEmissions starts at 1 to give the for loop something to multiply the first forward accumulator with which ultimately doesn't matter.
    """
    
    ProbabilityOfObservedEmissions = 1
    for key in forward:
        ProbabilityOfObservedEmissions = ProbabilityOfObservedEmissions*forward[key]
    print("\nThe P(O) of this sentence is",ProbabilityOfObservedEmissions,"\n")
    
    return(forward)

def backwardAlgorithm(ObservedEmissions,States,emissiontable,initialvector,transitiontable):
    
    """
    Purpose: Calculates the backward accumulator for each state at the each timecount
    Returned data form: dictionary (backward) key/value pairs
    The key is (timepoint,state); the value is the forward accumulator of the given state at the given time.\
    
    The 'TimeCount' variable keeps track of what timepoint the algorithm is at. Since we're going backwards, we start at whatever timepoint the final emission is at.
    That timepoint equals the number of emissions in the sentence, which can be calculated as the length of the list of observed emissions (len(ObeservedEmissions)).
    
    The list containing the states (States) starts its index numbering at zero, so the count variable serving to reference the state list's index (statecount) ends at 1.  
    
    The dictionary of emission probabilities (emissiontable)'s keys (oekey) are in the form emissionPOS. 
    Because the index of the list of emissions (ObservedEmissions) starts at zero, but timecount starts at one, the emission's index is the timecount-1.
    The values are the probability of the emission given the POS, in decimal form.
    
    The dictionary of transition probabilities (transitiontable)'s keys are in the form PreviousstateCurrentstate.
    The values are the probability of the of the state the accumulator is at given the previous state being observed, in decimal form.
    """
    
    backward = {}
    OElength = len(ObservedEmissions)
    TimeCount = OElength
    
    #induction
    
    """
    Because we're moving backwards through the timecounts, we have already seen that end of the emissions will occur.
    Therefore, the backwards accumulator for all states at the final timepoint is one.
    """
    
    for state in States:
        backward[TimeCount,state] = 1

    #iteration
    
    """
    Now, onwards to iteration.
    Now it's time to calculate the non-final timepoint backward accumulators.
    The backward accumulator for a given state at a given timepoint calculated as follows:
        For each state at the next timepoint:
            Multiply the backward accumulator by the transition probability [current timepoint's state to next timepoint state] and the emission probability [observed emission given current state]
        Sum over the results of the multiplication just performed.
    The backward accumulators are added to the dictionary of backwards accumulators (backward).
    
    The TimeCount variable keeps track of the current timepoint. The iteration begins at the next-to-final timepoint, so TimeCount is set to the final timepoint-1.
    When the backward accumulators of all states at the given timepoint have been calculated, 1 is subtracted from TimeCount so the previous timepoint's backward accumulators can be calculated.
    
    """
    
    TimeCount = OElength-1
    for step in ObservedEmissions:
        while TimeCount > 0:
            for state in States:
                oekey = ObservedEmissions[TimeCount]+state
                emissionprob = emissiontable[oekey]
                backward[TimeCount,state] = 0
              # print(backward[timecount,state])
                for nextstate in States:
                    ttkey = state+nextstate
                    transitionprob = transitiontable[ttkey]
                    backward[TimeCount,state] += transitionprob*emissionprob*backward[TimeCount+1,state]
                   #print("backward accumulator", timecount, state, "is", backward[timecount,state],"\n")
            TimeCount -= 1                  
            
    #termination
    
    """
    Now that all backward accumulators have been calculated, we can calculate the probability of having observed all emissions observed in the sentence.
    This is done by multipling all of the backward accumulators together.
    The variable ProbabilityOfObservedEmissions represents, the probability of the string of observed emissions.
    ProbabilityOfObservedEmissions starts at 1 to give the for loop something to multiply the first forward accumulator with which ultimately doesn't matter.
    """
    
    ProbabilityOfObservedEmissions = 1
    for key in backward:
        ProbabilityOfObservedEmissions = ProbabilityOfObservedEmissions*backward[key]
        
    print("\nThe P(O) of this sentence is",ProbabilityOfObservedEmissions,"\n")
    return(backward)
    
States = ['DT','JJ','NN','VB']
ObservedEmissions = ['a','myth','is','a','female','moth']

emissiontable = {'aDT':0.85,'aJJ':0.05,'aNN':0.03,'aVB':0.05,'mythDT':0.01,'mythJJ':0.10,'mythNN':0.45,'mythVB':0.10,'isDT':0.02,'isJJ':0.02,'isNN':0.02,'isVB':0.60,'femaleDT':0.01,'femaleJJ':0.60,'femaleNN':0.25,'femaleVB':0.05,'mothDT':0.12,'mothJJ':0.13,'mothNN':0.25,'mothVB':0.20}
transitiontable = {'DTDT':0.03,'DTJJ':0.42,'DTNN':0.50,'DTVB':0.05,'JJDT':0.01,'JJJJ':0.25,'JJNN':0.65,'JJVB':0.09,'NNDT':0.07,'NNJJ':0.03,'NNNN':0.15,'NNVB':0.75,'VBDT':0.30,'VBJJ':0.25,'VBNN':0.15,'VBVB':0.30}
initialvector = [0.45,0.35,0.15,0.05]

print("\nStarting Forwards Algorithm!\n")
print("\nThe forward accumulators are:\n\n",forwardAlgorithm(ObservedEmissions,States,emissiontable,initialvector,transitiontable))

print("\nStarting Backwards Algorithm!\n")    
print("\nThe backwards accumulators are:\n\n",backwardAlgorithm(ObservedEmissions,States,emissiontable,initialvector,transitiontable))