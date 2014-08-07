"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
codeskulptor.set_timeout(100)

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    result = []
    for item in list1:
        if item not in result:
            result.append(item)
    return result

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    result = []
    for item in list1:
        if item in list2:
            result.append(item)
    return result

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    result = []
    #choose the smaller-sized list to be the iterating list in the
    #for loop
    iterating_list = []
    iterated_list = []
    if len(list1) <= len(list2):
        iterating_list = list1[:]
        iterated_list = list2[:]
    else:
        iterating_list = list2[:]
        iterated_list = list1[:]
        
    while (len(iterating_list) > 0) and (len(iterated_list) > 0):
#        print iterating_list
#        print iterated_list
#        print result
#        print
#        print len(iterating_list)
#        print len(iterated_list)
#        print
        iterating_list_item = iterating_list[0]
        iterated_list_item = iterated_list[0]
        if iterating_list_item <= iterated_list_item:
            result.append(iterating_list_item)
            iterating_list.pop(0)
        else:
            result.append(iterated_list_item)
            iterated_list.pop(0)
    
    if len(iterating_list) > 0:
        result.extend(iterating_list)
    elif len(iterated_list) > 0:
        result.extend(iterated_list)
    #print result    
    return result

#print merge([1, 2, 3], [4, 5, 6]) #expected [1, 2, 3, 4, 5, 6] 
#print merge([8, 19, 32, 47], [1, 5, 7, 8]) #expected [1, 5, 7, 8, 8, 19, 32, 47]

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) == 0 or len(list1) == 1:
        return list1
    else:
        middle_index = len(list1)/2
        first_half = list1[ :middle_index]
        second_half = list1[middle_index: ]
#        list2 = merge(first_half, second_half)
#        print first_half, second_half
        return merge(merge_sort(first_half), merge_sort(second_half)) 
    
#print merge_sort([2, 6, 8, 10]) #expected [2, 6, 8, 10] 
#print merge_sort([2, 8, 6, 10])

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [""]
    elif len(word) == 1:
        return [""] + [word]
    else:
        first_letter = word[0]
        #print first_letter
        rest_letters = word[1: ]
        #print rest_letters
        rest_strings = gen_all_strings(rest_letters)
        #print rest_strings
        first_letter_strings = []
        for rest_word in rest_strings:
            for idx in range(len(rest_word)+1):
                string = ""
                if idx == 0:
                    string = first_letter + rest_word
                elif idx == len(rest_word):
                    string = rest_word + first_letter
                else:
                    string = rest_word[ :idx] + first_letter + rest_word[idx: ]
                first_letter_strings.append(string)             
    #print first_letter_strings
    return first_letter_strings + rest_strings

#print gen_all_strings('a')
#print gen_all_strings('ab') #expected (order doesn't matter) ['', 'b', 'a', 'ab', 'ba'] but received ['ab', '', 'b']

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(WORDFILE)
    netfile = urllib2.urlopen(url)
    
    word_list = []
    for word in netfile.readlines():
        word = word[:-1]
        word_list.append(word)
    #print word_list
    return word_list

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    
