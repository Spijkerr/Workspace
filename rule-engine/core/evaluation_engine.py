# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 21:48:47 2016

@author: Thomas
"""

"""
The engine consists of a couple of things.
-A mapping from natural language to operators/comparisons in several dicts
-A collections of sets for the definition of frames
-Certain sets/maps which encompass all the operators/known_elements
-A definition for fetch_action, which will be partialed up for all the dicts
-A couple standard error_messages that will be used in the partial functions
-A function that returns a classification for the operators.

But first, some imports.
"""

#Some useful functions
from functools import partial, reduce 
from operator import or_

#Import operator for the standard operator library
import operator

#Import custom functions 

#fuzzymatch etc 
def approx_local_ratio(): pass

#Import Series because sometimes we need to partial the Series.apply

from pandas import Series




#Dictionaries for operators 

#These operators are in the center of two operands
double_operators =   {'+': operator.add,
                      '-': operator.sub,
                      '/': operator.truediv,
                      '*': operator.mul,
               
                      #Custom functions we defined
                      'fuzzymatch met': approx_local_ratio,
                      'verschillen niet meer dan': None, #discrete/cont chunks percentagewise
                      'wijken niet meer af dan': None, #discrete/cont chunks amountwise
                      'zijn gelijk aan elkaar': 'simple groupby',
                      }

#The operand is on the left side of these operators
lside_operators = {}

#The operand is on the right side of these operators
rside_operators = {'de lengte van': None,
                   'de frequentie van': None,
                   'bevat het patroon': None,
                   }

comparisons = {'<': operator.lt,
               '<=': operator.le,
               '==': operator.eq,
               '!=': operator.ne,
               '>': operator.gt,
               '>=': operator.ge,
               'zit in': None,
               'zit niet in': None
               }
                   

precedence = {'**': 0,
              '*': 1, '/': 1, 
              '+': 2, '-': 2, 'fuzzymatch met': 2, 
              '<=': 3, '<': 3, '>': 3, '>=': 3,
              '==':4, '!=': 4,
              'in': 5, 'not in': 5
              }

#Sets for frames

connectors = {'van'}

possible_frames = {'beide regels': 'vergelijk met elkaar',
                  'alle regels': 'vergelijk alle transacties',
                  'eerste regel': None,
                  'tweede regel': None,
                  'minstens een van de regels': None,
                  'precies een van de regels': None
                  }


#Mapping of all operators and elements
all_operator_dicts = [double_operators, 
                      lside_operators, 
                      rside_operators,
                      comparisons]
                             
all_elements_dicts = [double_operators,
                      lside_operators,
                      rside_operators,
                      comparisons,
                      connectors,
                      possible_frames]
                             
all_operators = reduce(or_, [{n for n in seq} for seq in all_operator_dicts])
all_operators = sorted(list(all_operators), key = len, reverse = True)

all_elements = reduce(or_, [{n for n in seq} for seq in all_elements_dicts]) 
known_elements = sorted(list(all_elements), key = len, reverse = True)

type_of_operators = {'double': double_operators,
                     'rside': rside_operators,
                     'lside': lside_operators,
                     'cmp': comparisons}


#Fetch action, error_messages and partial functions
def fetch_action(action, lookup, err):
    try:
        return lookup[action]
    except:
        raise NameError(err.format((action)))
        
        
unkwn_op = "This operator {0} is not available in the engine."
unkwn_cmp = "This comparison {0} is not available in the engine."
unkwn_prc = "There is no known precedence for this action {0}."

getdub_operator = partial(fetch_action, lookup = double_operators, err=unkwn_op)
getlsd_operator = partial(fetch_action, lookup = lside_operators, err=unkwn_op)
getrsd_operator = partial(fetch_action, lookup = rside_operators, err=unkwn_op)
getcomparison = partial(fetch_action, lookup = comparisons, err = unkwn_cmp)
getprecedence = partial(fetch_action, lookup = precedence, err = unkwn_prc)


#Function for classifying an operator

                     
def classify_operator(input_operator, err = unkwn_op):
    for operator_type, operator_dict in type_of_operators.items():
        if input_operator in operator_dict:
            return operator_type
            
    raise NameError(err.format((operator)))
    






