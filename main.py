import numpy as np

def remove_duplicate(L : list,
                     sort : bool = False) -> list :
    """
    Remove all duplicated items from a list L 
    
    Args: 
        - L (list) : Raw list with duplicated items.
        - sort (bool) : Ordering or not the list
    Returns: 
        - L_f (list) : List with no duplicated items.
    """

    if sort : return list(set(L))
    else : return list(dict.fromkeys(L).keys()) 

def permutations(string):
    """
    Create all permutations of a string with non-repeating characters

    Args: 
        - string (str) : string to permute.
    Returns: 
        - permutation_list (list) : List with every permutations of the string.
    """
    permutation_list = []
    if len(string) == 1:
        return string

    else:
        for char in string:
            for new_string in permutations(string.replace(char, "", 1)) :
                #add at the extracted char every permutations lenght len(str)-1 without the extracted char
                permutation_list.append(char + new_string)

    return permutation_list