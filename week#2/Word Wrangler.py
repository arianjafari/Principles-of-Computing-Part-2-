"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    new_list = []
    
    
    for item in list1:
        if item not in new_list:
            new_list.append(item)
    
    return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    new_list = []
    
    for item1 in list1:
        for item2 in list2:
            if item2 == item1:
                new_list.append(item1)
    
    return new_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    new_list = []
    
    new_1 = list1[:]
    new_2 = list2[:]
    
    while len(new_1) != 0 and len(new_2) != 0:
        list_10 = new_1[0]
        list_20 = new_2[0]
        if list_10 < list_20:
            new_list.append(list_10)
            new_1.pop(0)
        else:
            new_list.append(list_20)
            new_2.pop(0)

                
    
    return new_list + (new_1)+ (new_2)
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    else:
        first_half = merge_sort(list1[0:len(list1)//2])
        second_half = merge_sort(list1[len(list1)//2:])
        return merge(first_half, second_half)
    
    

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    result = []
    if len(word) < 1:
        
        return [word]
    
    else:
        first = word[0]
        rest = word[1:]
        
        rest_strings = gen_all_strings(rest)
        
        
        for item in rest_strings:
            
            for idx in range(len(item)+1):
                
                result.append(item[0:idx]+first+item[idx:])
   
        
    return result+rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    a_file = urllib2.urlopen(codeskulptor.file2url(filename))
    return list(a_file.readlines())

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

#print remove_duplicates(['a','b','b','c'])
#print remove_duplicates([0,0, 1, 2, 3, 4])
#print intersect(['a','b','c','d','g'], ['a','c','d','e','f','b']) 
print merge([1,2,3,5], [2,3,4,4,5,6]) 
#print merge([1, 2, 3], [4, 5, 6])
print gen_all_strings("aab")