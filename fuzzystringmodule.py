
import numpy

_minimumstring = 2
_minimummatch = 4

#Exact local matching
_exactmatch = 2

#Approx. local matching
_localdiag = 2
_localoffdiag = -1
_localdash = -2

#Editing distance calculation using global alignments
_diag = 2
_offdiag = 0
_dash = 0




#=========== Main ratio functions 

def best_fuzzy_ratio(string1, string2):
    total_length = len(string1) + len(string2)
    functions = [approx_global_points, exact_points, approx_local_points]
    max_points = max([function(string1, string2) for function in functions])
    return max_points / total_length
    
def exact_ratio(string1, string2):
    total_length = len(string1) + len(string2)
    return exact_points(string1, string2) / total_length 

def approx_local_ratio(string1, string2):
    total_length = len(string1) + len(string2)
    return approx_local_points(string1, string2) / total_length
    
def approx_global_ratio(string1, string2):
    total_length = len(string1) + len(string2)
    return approx_global_points(string1, string2) / total_length

#================= Main point calculation functions
    
def best_points(string1, string2):
    return max(approx_global_points(string1, string2), 
               exact_points(string1, string2))
    
def worst_points(string1, string2):
    return min(approx_global_points(string1, string2),
               exact_points(string1, string2))
               
#================= Calculating the points 

def approx_local_points(string1, string2):
    length1 = len(string1)
    length2 = len(string2) 
    
    if length2 < _minimumstring and length1 < _minimumstring:
        return 0.0 
    
    alignment_matrix = approx_alignment_matrix(string1, string2, False)
    match = approx_local_traceback(alignment_matrix, string1, string2)
    if match[0] < _minimummatch:
        return 0.0
    
    clean_1 = match[1].replace('-','')
    clean_2 = match[2].replace('-','')
    
    string1 = string1.replace(clean_1, '')
    string2 = string2.replace(clean_2, '')
    
    length1 = len(string1)
    length2 = len(string2)
    
    if length1 < _minimumstring or length2 < _minimumstring:
        return match[0]
    else:
        return match[0] + approx_local_points(string1, string2)

def approx_local_traceback(alignment_matrix, string1, string2):
    row, col = numpy.unravel_index(alignment_matrix.argmax(), alignment_matrix.shape)
    highest_score =  alignment_matrix[row, col]
    indices = [[row, col]]
    
    
    string1_prime = ""
    string2_prime = ""        

    while row != 0 and col != 0:
        alignment_score = alignment_matrix[row, col]
        
        if alignment_score == 0:
            break
        
        elif alignment_score == alignment_matrix[row-1, col-1] + _localdiag:
            string1_prime = string1[row-1] + string1_prime
            string2_prime = string2[col-1] + string2_prime
            row -= 1
            col -= 1

        elif alignment_score == alignment_matrix[row-1,col] +  _localdash:
            string1_prime = string1[row-1] + string2_prime
            string2_prime = '-' + string2_prime
            row -= 1

            
        else:
            string1_prime = '-' + string1_prime
            string2_prime = string2[col-1] + string2_prime
            col -= 1      
            
    if alignment_matrix[row][col] != 0:  
        
        while row != 0:
            string1_prime = string1[row-1] + string1_prime
            string2_prime = '-' + string2_prime
            row -= 1

        while col != 0:
            string1_prime = '-' + string1_prime
            string2_prime = string2[col-1] + string2_prime
            col -= 1  
        
    indices.append([row,col])
    
    return (highest_score, string1_prime, string2_prime)  
	        

def exact_points(string1, string2):
    length1 = len(string1)
    length2 = len(string2)
    #Base case
    if length1 < _minimumstring or length2 < _minimumstring:
        return 0.0
    
    #Recursive case
    matrix = exact_alignment_matrix(string1, string2, length1, length2)
    match = exact_sequence(string1, string2, matrix)
    
    if match[0] < _minimummatch:
        return 0.0
    
    string_1 = string1.replace(match[2], '')
    string_2 = string2.replace(match[3], '')
    length_1, length_2 = len(string_1), len(string_2)
    
    if length_1 == 0 or length_2 == 0:
        return match[0]
    else:
        return exact_points(string_1, string_2) + match[0]
        
    
def exact_sequence(string1, string2, alignment_matrix):
    row, col = numpy.unravel_index(alignment_matrix.argmax(), alignment_matrix.shape)
    highest_score =  alignment_matrix[row, col]
    indices = [[row, col]]
    
    string1_prime = ""
    string2_prime = ""
    while row != 0 and col != 0:
        alignment_score = alignment_matrix[row, col]
        
        if alignment_score == 0:
            break
        
        if alignment_score == alignment_matrix[row-1, col-1] + _exactmatch:
            string1_prime = string1[row-1] + string1_prime
            string2_prime = string2[col-1] + string2_prime
            row -= 1
            col -= 1
            
    indices.append([row,col])
    return (highest_score, indices, string1_prime, string2_prime)
        

def approx_global_points(string1, string2):
    alignment_matrix = approx_alignment_matrix(string1, string2, True)
    
    row = len(string1)
    col = len(string2)
    
    highest_score = alignment_matrix[row][col]

    string1_prime = ""
    string2_prime = ""
    while row != 0 and col != 0:
        
        alignment_score = alignment_matrix[row][col]
        
        if alignment_score == alignment_matrix[row-1][col-1] + \
        _diag if string1[row-1] == string2[col-1] else _offdiag:
            string1_prime = string1[row-1] + string1_prime
            string2_prime = string2[col-1] + string2_prime
            row -= 1
            col -= 1
            
        elif alignment_score == alignment_matrix[row-1][col] + _dash:
            string1_prime = string1[row-1] + string2_prime
            string2_prime = '-' + string2_prime
            row -= 1
            
        else:
            string1_prime = '-' + string1_prime
            string2_prime = string2[col-1] + string2_prime
            col -= 1      
            
    while row != 0:
        string1_prime = string1[row-1] + string1_prime
        string2_prime = '-' + string2_prime
        row -= 1
        
    while col != 0:
        string1_prime = '-' + string1_prime
        string2_prime = string2[col-1] + string2_prime
        col -= 1  
        
            
    return highest_score #, string1_prime, string2_prime)    

#============ Calculating the matrices

    
def exact_alignment_matrix(string_1, string_2, length_1, length_2):
    #The rows are the first string, columns are the second string. 
    row_range, col_range = range(length_1+1), range(length_2+1)
    
    alignment_matrix = [[0 for col in col_range] for row in row_range]
    
    for row in range(1, length_1+1):
        for col in range(1, length_2+1):

            if string_1[row-1] == string_2[col-1]:
                alignment_matrix[row][col] = alignment_matrix[row-1][col-1] + _exactmatch
            else:
                alignment_matrix[row][col] = 0
                
    alignment_matrix = numpy.array(alignment_matrix)
    return alignment_matrix
    
def approx_alignment_matrix(string1, string2, global_flag):
    length1 = len(string1)
    length2 = len(string2)

    #Global and local alignments have different scoring settings
    #We first assign the correct score to our variables, depending on the flag
    offdiag_score = _offdiag if global_flag else _localoffdiag
    diag_score = _diag if global_flag else _localdiag
    dash_score = _dash if global_flag else _localdash
    
    #Initialize the matrix to be a length1+1-by-length2+1 matrix full of 0s.
    #I know the +1 in length+1 was because we sometimes initialized the matrix to -2
    #But I have no idea why we still use it. Maybe look into it.
    #I think it might be because we look at the pos above/left of the current pos
    #If the matrix was not a little larger, we would get index errors.
    
    alignment_matrix = [[0 for dummy_col in range(length2 + 1)]
                        for dummy_row in range(length1 + 1)]
    
  
    for row in range(1, length1+1):
        for col in range(1, length2+1):
            matrix_score = diag_score if string1[row-1] == string2[col-1] else offdiag_score

            score = max(alignment_matrix[row-1][col-1] + matrix_score,
                        alignment_matrix[row-1][col] + dash_score,
                        alignment_matrix[row][col-1] + dash_score
                        )

            if global_flag == False and score < 0:
                score = 0
                
            alignment_matrix[row][col] = score
            
    alignment_matrix = numpy.array(alignment_matrix)
    
    return alignment_matrix
