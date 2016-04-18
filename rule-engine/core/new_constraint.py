# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 18:14:57 2016

@author: Thomas
"""

from operator import or_, and_
from functools import reduce
import re
from EvaluationEngine import Expression

class Constraint():
    def __init__(self, raw_expression, **kwargs):
        known_boolean_operators = ' and | or '
        
        #First we see whether there are boolean operators present in the expr.
        boolean_ops = re.findall(known_boolean_operators, raw_expression)
        self.boolean_ops = [or_ if n == ' or ' else and_ for n in boolean_ops]
        
        #Split the expression on those operators, if present.
        expressions = re.split(known_boolean_operators, raw_expression)
        self.expressions = [Expression(n) for n in expressions]
        
        #Little assertion here and there never hurt nobody.
        assert len(self.expressions) == len(self.boolean_ops) + 1

        #Kwargs is used to declare the values that are used in the expression(s)
        
        #First get all the used variables
        sets_of_variables = [n.return_variables() for n in self.expressions]
        used_variables = reduce(or_, sets_of_variables)
        
        #Now assert that all the variables that are used in expressions;
        #are also actually defined in the kwargs. 
        for used_variable in used_variables:
            e = "Variable {0} is used, but not defined".format(used_variable)
            assert used_variable in kwargs, e  
            
        for defined_variable in kwargs:
            value = kwargs[defined_variable]
            setattr(self, defined_variable, value)
            
        
    def specify_constraint_mode(self):
        pass
        

    def evaluate_constraint(self, **kwargs):
        #self.set_attributes(**kwargs) activeer deze en pas set_attribute aan
        
        if len(self.expressions) == 1:
            return self.expressions[0].evaluate(self)
            
        #If we got here it means there are more than one expressions
        #So we have to string together some expressions with their bool operators
            
        bool_ops_iter = iter(self.boolean_ops)
        def evaluate_expressions(*args):
            #The args contain two expressions.
            #Get the next boolean operator, evaluate expressions
        
            boolean_operator = next(bool_ops_iter)
            results = [n if isinstance(n, bool) else n.evaluate(self) for n in args]
            return boolean_operator(*results)
        
        return reduce(evaluate_expressions, self.expressions)
        
    def set_attributes(self, *args):
        keys = iter(['eersteregel', 'tweederegel', 'alleregels'])
        for value in args:
            key = next(keys)
            setattr(self, key, value)
            

   
"""
t = Constraint('A van eerste regel + A van tweede regel ')
n = Constraint('A van eerste regel - A van tweede regel ')
k = Constraint(, var2 = 10)
l = Constraint('A van eerste regel - A van tweede regel == var1 or A van eerste regel - A van tweede regel <= var2', var1 = 20, var2 = 30)
"""

import unittest
from pandas import Series, DataFrame

class TestDisjunctedExpressionsinConstraint(unittest.TestCase):
    list1 = [1,2,3]
    list2 = [[1,2,3],[4,4,4],[9,9,9]]   
    eersteregel = Series(list1, index = ['A','B', 'C'])
    tweederegel = totaleregels = DataFrame(list2, columns = ['A','B','C']) 

    
    def eval_shortcut(self, raw_expression, **kwargs):
        constraint = Constraint(raw_expression, **kwargs)
        constraint.set_attributes(self.eersteregel, self.tweederegel, self.totaleregels)
        
        return constraint.evaluate_constraint().tolist()
        
        
        
    def test1(self):
        n = self.eval_shortcut('A van eerste regel - A van tweede regel <= var2', var2 = 10)
        
        self.assertEqual(n, [True, True, True])
        
    def test2(self):
        #Baby's first or statement test.
        
        n = self.eval_shortcut('B van eerste regel == var1 or A van tweede regel == var2', var1 = 3, var2 = 9)
        
        self.assertEqual(n, [False, False, True])
      
    def test3(self):
         #Baby's first and statement test.
         
         n = self.eval_shortcut('B van eerste regel == var1 and A van tweede regel == var2', var1 = 2, var2 = 4)
         
         self.assertEqual(n, [False, True, False])
         
    def test4(self):
        
        n = self.eval_shortcut('B van eerste regel == var1 and A van tweede regel > var2', var1 = 2, var2 = 3)
        
        self.assertEqual(n, [False, True, True])
        
if __name__ == '__main__':
    unittest.main()
