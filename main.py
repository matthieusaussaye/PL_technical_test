import numpy as np
from typing import *
from nptyping import *


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
    if not all([isinstance(L,list),isinstance(sort,bool)]) : #test the types
        raise Exception(f'Incorrect types - L : {type(L)} instead of list, sort : {type(sort)} instead of bool')

    if sort : return list(set(L))
    else : return list(dict.fromkeys(L).keys()) 

def permutations(word : str) -> List[str] :
    """
    Create all permutations of a string with non-repeating characters

    Args: 
        - word (str) : word to permute.

    Returns: 
        - permutation_list (list) : List with every permutations of the word.
    """

    if not isinstance(word,str) :
        raise Exception(f'Incorrect type : {type(word)}')

    permutation_list = []


    if len(word) == 1 or len(word) == 0 :
        return [word]

    else:
        for char in word:
            for new_string in permutations(word.replace(char, "", 1)) :
                #add at the extracted char every permutations lenght len(str)-1 without the extracted char
                permutation_list.append(char + new_string)

    return permutation_list

def signature(permutation : List[int]) -> int : #to add test 
    """
    Compute the signatures of a permutation (list of int)

    Args:
        - permutation (list) : list of int where i is the index of the list and i -> sigma(i) is the bijection. Example : [1,2,3,4] -> 1 
    
    Return:
        - prod (float) : signature of the permutation
    """

    prod = 1
    #signature = prod [perm(j)-perm(i)]/[j-i]
    for j in range(len(permutation)) :
        for i in range(j) :
            prod *= (permutation[j]-permutation[i])/((j+1)-(i+1))

    return(prod)

def compute_determinant(M : Union[NDArray[(int)],NDArray[(float)]]) -> int :
    """
    Compute the determinant of a square matrix using the signature.

    Args:
        - M (np.darray) : matrix size NxN
    
    Return:
        - determinant (float) : determinant of the matrix
    """

    if not isinstance(M, np.ndarray) :
        raise Exception('Matrix type incorrect. Input a np.ndarray matrix')
    
    if len(M.shape) != 2 or M.shape[1] != M.shape[0] :
        raise Exception('Matrix size incorrect. Input a np.ndarray matrix size NxN with N>1')

    if len(M) == 1 :
        return float(M)
    
    size = len(M)
    indexes_str = "".join(map(str,np.arange(1,size+1,1))) #create string : '1234..len(M) to be used in permutation function'
    permutations_str = permutations(indexes_str)          #compute all permutations of the string
    sum = 0

    for permutation in permutations_str :

        permutation_int = [int(i) for i in permutation] #convert the permutations as list of int
        sign = signature(permutation_int)               #compute the signature

        prod_permutation = sign

        for i in range(len(permutation_int)) :
            prod_permutation *= M[permutation_int[i]-1,i] #compute the determinant as sum of sign*permutations for each index
    
        sum+=prod_permutation
    
    return(sum)

def operation(operator : str,
              operand1 : Union[float,int],
              operand2 : Union[float,int]) -> float :
    
    """
    Return the operation with between the two operands & the operator.

    Args:
        - operator (str) : operator to use
        - operand1 (float) : first operand
        - operand2 (float) : second operand
    
    Return:
        - result (float) : result of the operation
    """
    if not all([isinstance(operator,str),isinstance(operand1,float),isinstance(operand2,float)]) : 
        raise(f'Incorrects inputs types. operator <{type(operator)}> operand1 <{type(operand1)}> operand2 <{type(operand2)}>') 

    # if current operator is '+', updating tmp variable by addition
    if(operator == '+'):
        result = operand1 + operand2 #chose close operands to make next operation        

    # if current operator is '*', updating tmp variable by multiplication
    elif(operator == '*'):
        result = operand1 * operand2 #chose close operands to make next operation        

    # if current operator is '-', updating tmp variable by substraction
    elif(operator == '-'):
        result = operand1 - operand2 #chose close operands to make next operation        

    # if current operator is '/', updating tmp variable by division
    elif(operator == '/' and operand2!=0):
        result = operand1 / operand2 #chose close operands to make next operation      

    else : #control division/0 & Operator type
        raise Exception(f'Invalid operator : {operator}. or division by 0')
  
    return result

def maxminexp(list_num : List[Union[int,float]],
              list_op : List[str]) -> Tuple[str, tuple] :
    """
    Compute the expression that gives the maximum & the difference between the max & the min expression for every possible parenthesis.

    Args:
        - list_num (list) : list of operands
        - list_op (list) : list of operators 
    
    Return:
        - result (tuple) : maximal expression & rounded difference betweeen max & min.
    """
    llen = len(list_num)
    list_numbers = [float(x) for x in list_num] #convert the list in float for easier type testing.

    minVal = [[0 for i in range(llen)] for i in range(llen)]
    maxVal = [[0 for i in range(llen)] for i in range(llen)]
    maxExpr = [[None for i in range(llen)] for i in range(llen)]
    # initializing minval and maxval 2D array

    for i in range(llen) :
        for j in range(llen) : #maximal / minimal unreachable value
            minVal[i][j] = float(10**9)
            maxVal[i][j] = float(-10**9)
            if (i==j): # initializing main diagonal by num values
                minVal[i][j] = maxVal[i][j] = list_numbers[i]
                maxExpr[i][j] = str(list_numbers[i])

    # looping similar to matrix chain multiplication
    # and updating both 2D arrays
    for L in range(2, llen + 1):
        for i in range(llen - L + 1):
            j = i + L - 1
            for k in range(i,j):
                minTmp = 0
                maxTmp = 0
                max_exprTmp = '('+maxExpr[i][k]+list_op[k]+maxExpr[k + 1][j]+')'
                minTmp = operation(operator=list_op[k],operand1=minVal[i][k],operand2=minVal[k+1][j])
                maxTmp = operation(operator=list_op[k],operand1=maxVal[i][k],operand2=maxVal[k+1][j])
            
                # updating array values by tmp variables
                if (minTmp < minVal[i][j]) :
                    minVal[i][j] = minTmp
                if (maxTmp > maxVal[i][j]) :
                    maxVal[i][j] = maxTmp
                    maxExpr[i][j] = max_exprTmp

    diff = int(round(maxVal[0][llen - 1]-minVal[0][llen - 1]))
    return (maxExpr[i][llen-1],diff)