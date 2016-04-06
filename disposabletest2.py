# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 12:42:27 2016

@author: OffermanTW1
"""

import fuzzystringmodule


"""
class FuzzyStringMatcher():
    pass

fsm = FuzzyStringMatcher(a=str1, b= str2)

result1 = fsm.ratio()

fsm.set_a(str3)
fsm.set_b(str4)

result2 = fsm.ratio()

"""


from fuzzystringmodule import best_fuzzy_ratio, approx_local_ratio, exact_ratio, approx_global_ratio
str1 = 'Test22FlapAppels'
str2 = 'Test2OAppelsFlap'


#result = best_fuzzy_ratio(str1, str2)
result1 = approx_local_ratio(str1, str2)
result2 = approx_global_ratio(str1, str2)
result3 = exact_ratio(str1, str2)


print(result, result1, result2, result3)