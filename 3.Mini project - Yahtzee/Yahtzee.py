"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    maximum = 0
    
    for dice in hand:
        current_maximum = 0
        for current_dice in hand:
            if (current_dice == dice):
                current_maximum += dice
        if current_maximum > maximum:
            maximum = current_maximum
    return maximum


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    result = 0
    outcomes = [x for x in range(1, num_die_sides+1)]
    sequences = gen_all_sequences(outcomes, num_free_dice)
    probability = (1.0/num_die_sides)**num_free_dice
    
    for outcome in sequences:
        hand = held_dice + outcome
        hand_score = score(hand)
        result += (hand_score * probability)
    return result

#helper for gen_all_holds(hand):
#def generate_hold(hand):
    

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    answer_set = [hand]
    for idx in range(0, len(hand)):
        answer_set += list(gen_all_sequences(hand, idx))
    
    result = [()]
    for hold in answer_set:
        hold = list(hold)
        hold.sort()
        count = 0
        for value in hold:
            if hold.count(value) > hand.count(value):
                count += 1
        if count == 0:
            result.append(tuple(hold))
    return set(result)

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    expected_score = 0.0
    all_holds = gen_all_holds(hand)
    result = {}
    for hold in all_holds:
        num_free_dice = len(hand) - len(hold)
        value = expected_value(hold, num_die_sides, num_free_dice)
        result[value] = hold
    expected_score = max(result)
    return (expected_score, result[expected_score])


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



