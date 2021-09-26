import numpy as np

def remove_duplicate(L : list,
                     sort : bool = False) -> list :
    """
    Remove all duplicated items from a list L 
    
    Args: 
        - L (list) : Raw list with duplicated items.
        - sort (bool) : Ordering or not the list.

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

def signature(permutation : list) -> int :
    """
    Compute the signatures of a permutation (list of int)

    Args:
        - permutation (list) : list of int where i is the index of the list and i -> sigma(i) is the bijection. Example : [1,2,3,4] -> 1 
    
    Return:
        - prod (float) : signature of the permutation
    """
    prod = 1
    for j in range(len(permutation)) :
        for i in range(j) :
            prod *= (permutation[j]-permutation[i])/((j+1)-(i+1))

    return(prod)

def compute_determinant(M : np.ndarray) -> int :
    """
    Compute the determinant of a square matrix using the signature.

    Args:
        - M (np.darray) : matrix size NxN
    
    Return:
        - determinant (float) : determinant of the matrix
    """

    if not isinstance(M, np.ndarray) or len(M.shape) != 2 or M.shape[1] != M.shape[0] :
        raise Exception('Matrix format incorrect. Input a np.ndarray matrix NxN with N>1')

    if len(M) == 1 :
        return float(M)
    
    size = len(M)
    indexes_str = "".join(map(str,np.arange(1,size+1,1))) #create string : '1234..len(M)'
    permutations_str = permutations(indexes_str) #compute all permutations of the string
    sum = 0

    for permutation in permutations_str :

        permutation_int = [int(i) for i in permutation]
        sign = signature(permutation_int)

        prod_permutation = sign

        for i in range(len(permutation_int)) :
            prod_permutation *= M[permutation_int[i]-1,i]
        
        sum+=prod_permutation
    
    return(sum)