#!/usr/bin/env python3

from fractions import Fraction

def P(space, event):
    return Fraction(len(event & space), len(space))


D = {1,2,3,4,5,6}
even = {2, 4, 6}

print("probability of even die roll is:", P(D, even), sep=" ")

def cross(A, B):
    return {a+b for a in A for b in B}

# +==================================================================================================================+
# |                                                                                                                  |
# | 23 balls in an urn: 8 white, 6 blue and 9 red. We select six balls at random. What is the probability of         |
# | each of the following outcomes:                                                                                  |
# |      i. all six balls are red                                                                                    |
# |     ii. 3 are blue, 2 are white, and 1 is red                                                                    |
# |    iii. exactly 4 balls are white                                                                                |
# |                                                                                                                  |
# +==================================================================================================================+


urn = cross('W', ''.join(map(str, [i+1 for i in range(8)]))) | \
      cross('B', ''.join(map(str, [i+1 for i in range(6)]))) | \
      cross('R', ''.join(map(str, [i+1 for i in range(9)])))



from itertools import combinations

C6 = {''.join(map(str, x)) for x in combinations(urn, 6)}

from math import factorial

def nChooseK(n, k):
    return factorial(n) // (factorial(n-k)*factorial(k))

assert len(C6)==nChooseK(23, 6)


red6 = {x for x in C6 if x.count('R')==6}

blue3white2red1 = {x for x in C6 if x.count('B')==3 and x.count('W')==2 and x.count('R')==1}

white4 = {x for x in C6 if x.count('W')==4}

print ("probability that all six balls are red is: "               , P(C6,  red6           ), sep="")
print ("probability that 3 are blue, 2 are white and 1 is red is: ", P(C6,  blue3white2red1), sep="")
print ("probability that exactly 4 are white is: "                 , P(C6,  white4         ), sep="")


assert P(C6, red6) == Fraction(nChooseK(9, 6), len(C6))

assert P(C6, blue3white2red1) == Fraction(nChooseK(8, 2)*nChooseK(6, 3)*nChooseK(9, 1), len(C6))
assert P(C6, blue3white2red1) == Fraction( (8*7)*(6*5*4)*9, factorial(2)*factorial(3)*factorial(1)*len(C6))

assert P(C6, white4) == Fraction( nChooseK(8, 4)*nChooseK(15, 2), len(C6) )

print ("\n\n")

# Let's modify P so that the event can be either a set or a predicate
# -------------------------------------------------------------------
def P(space, event):
    def suchThat(event):
        return {x for x in space if event(x)}
    
    if callable(event):
        event = suchThat(event)

    return Fraction(len(event), len(space))

def even(x):
    return x%2==0

assert P(D, even)==P(D, {2, 4, 6})==0.5

# we can now calculate the probability that the sum of three dice is a prime number
D3 = {(d1, d2, d3) for d1 in D for d2 in D for d3 in D}
import math

def is_prime(n): return n > 1 and not any(n % i == 0 for i in range(2, math.floor(math.sqrt(n))+1))



print ("The probability that the sum of three dice is a prime is: ", P(D3, lambda x: is_prime(sum(x))))

print ("\n\n")


# +==================================================================================================================+
# |                                                                                                                  |
# | Card problems                                                                                                    |
# |      i. probability of a flush                                                                                   |
# |                                                                                                                  |
# +==================================================================================================================+


suits='SDHC'
ranks='23456789TJQKA'
deck = cross(suits, ranks)
assert len(deck)==52

hands = {''.join(combo) for combo in combinations(deck, 5)}

assert len(hands)==nChooseK(len(deck), 5)

import random

print ( random.sample(hands, 5))

def flush(hand):
    return any(hand.count(suit)==5 for suit in suits)

print( "probability of a flush: ", P(hands, flush) )

def nOfAKind(n):
    def nOfAKind(hand):
        return any(hand.count(rank)==n for rank in ranks)
    return nOfAKind

def twoPair(hand):
    return [hand.count(rank)==2 for rank in ranks].count(True)==2

def fullHouse(hand):
    return ([hand.count(rank) in {2,3} for rank in ranks].count(True)==2) and not twoPair(hand)
    # the below also works and is perhaps cleaner (albeit, more verbose)
    # return ([hand.count(rank) == 2 for rank in ranks].count(True)==1) and \
    #       ([hand.count(rank) == 3 for rank in ranks].count(True)==1) 

print( "probability of a four or a kind: " , P(hands, nOfAKind(4)) )
print( "probability of a three or a kind: ", P(hands, nOfAKind(3)) )
print( "probability of two pair:  "        , P(hands, twoPair))
print( "probability of a pair: "           , P(hands, nOfAKind(2)) )
print( "probability of a full house: "     , P(hands, fullHouse))

