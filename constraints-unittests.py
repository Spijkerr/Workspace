# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 09:40:26 2016

@author: OffermanTW1
"""


import unittest
from pandas import Series, DataFrame
from Constraints import Constraint 

class TestConstraint1(unittest.TestCase):
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
      
      
class TestExpressionClassifier(unittest.TestCase):
    #Single expressions
    def test5(self):
        
        constraint = Constraint('A van eerste regel - A van tweede regel <= var2', var2 = 10)
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('real', 'parallel single comparison'))
        
    def test6(self):
        
        constraint = Constraint('B van alle regels == A van alle regels')
        modes = constraint.specify_constraint_mode()

        self.assertEqual(modes, ('total', 'irrelevant'))
        
    def test7(self):
        
        constraint = Constraint('B van eerste regel == A van eerste regel')
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('base', 'irrelevant'))
        
    def test8(self):
        
        constraint = Constraint('B van tweede regel == C van tweede regel')
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('comp', 'irrelevant'))
    
    def test9(self):
        
        constraint = Constraint('B van tweede regel == var2', var2 = 10)
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('comp', 'irrelevant'))
        
    def test10(self):

        constraint = Constraint('B van alle regels == var2', var2 = 10)
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('total', 'irrelevant'))       
        
    def test11(self):
        
        constraint = Constraint('B van eerste regel == var1', var1 = 10)
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('base', 'irrelevant'))     
  

    #Mixed Parallel disjunctions   
    def test12(self):
        
        constraint = Constraint('B van eerste regel == var1 or B van tweede regel == var1', var1 = 10)
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('real', 'external disjunction'))
        
    def test13(self):
        
        constraint = Constraint('B van tweede regel == var1 or B van tweede regel == var1', var1 = 10)
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('comp', 'irrelevant')) 

    def test14(self):
        
        constraint = Constraint('B van eerste regel == var1 or B van eerste regel == var1', var1 = 10)
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('base', 'irrelevant'))

    def test15(self):
        
        constraint = Constraint('B van alle regels == var1 or B van alle regels == var1', var1 = 10)
        modes = constraint.specify_constraint_mode()      
        
        self.assertEqual(modes, ('total', 'irrelevant'))
        

    #Mixed Non-parallel disjunctions 
    def test16(self):
        
        constraint = Constraint('A van eerste regel == var1 or B van tweede regel == var1', var1 = 10)
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('real', 'external disjunction'))
        
    def test17(self):
        
        constraint = Constraint('A van tweede regel == var1 or B van tweede regel == var1', var1 = 10)
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('comp', 'irrelevant'))

    def test18(self):
        
        constraint = Constraint('A van eerste regel == var1 or B van eerste regel == var1', var1 = 10)
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('base', 'irrelevant'))

    def test19(self):
        
        constraint = Constraint('A van alle regels == var1 or B van alle regels == var1', var1 = 10)
        modes = constraint.specify_constraint_mode() 
        
        self.assertEqual(modes, ('total', 'irrelevant'))
        
        

    #Mixed parallel conjunctions 
    def test20(self):
        
        constraint = Constraint('B van eerste regel == var1 and B van tweede regel == var1', var1 = 10)
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('real', 'external conjunction'))
        
    def test21(self):
        
        constraint = Constraint('B van tweede regel == var1 and B van tweede regel == var1', var1 = 10)
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('comp', 'irrelevant'))

    def test22(self):
        
        constraint = Constraint('B van eerste regel == var1 and B van eerste regel == var1', var1 = 10)
        modes = constraint.specify_constraint_mode()

        self.assertEqual(modes, ('base', 'irrelevant'))
        
    def test23(self):
        
        constraint = Constraint('B van alle regels == var1 and B van alle regels == var1', var1 = 10)
        modes = constraint.specify_constraint_mode() 
        
        self.assertEqual(modes, ('total', 'irrelevant'))

    #Mixed non-parallel conjunctions 
    def test24(self):
        
        constraint = Constraint('A van eerste regel == var1 and B van tweede regel == var1', var1 = 10)
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('real', 'external conjunction'))
    def test25(self):
        
        constraint = Constraint('A van tweede regel == var1 and B van tweede regel == var1', var1 = 10)
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('comp', 'irrelevant'))

    def test26(self):
        
        constraint = Constraint('A van eerste regel == var1 and B van eerste regel == var1', var1 = 10)
        modes = constraint.specify_constraint_mode()
        
        self.assertEqual(modes, ('base', 'irrelevant'))

    def test27(self):
        
        constraint = Constraint('A van alle regels == var1 and B van alle regels == var1', var1 = 10)
        modes = constraint.specify_constraint_mode() 
        
        self.assertEqual(modes, ('total', 'irrelevant'))

             
        
if __name__ == '__main__':
    test_classes_to_run = [TestConstraint1, TestExpressionClassifier]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
