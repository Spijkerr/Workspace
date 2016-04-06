# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 18:14:57 2016

@author: Thomas
"""

from operator import or_, and_
from functools import reduce
import re
from EvaluationEngine import Expression
from EvaluationEngine import FrameWithColumn, Operator, Comparison, Variable 
class Constraint():
    def __init__(self, raw_expression, **kwargs):
        known_boolean_operators = ' and | or '
        
        #First we see whether there are boolean operators present in the expr.
        self.boolean_ops_txt = re.findall(known_boolean_operators, raw_expression)
        self.boolean_ops = [or_ if n == ' or ' else and_ for n in self.boolean_ops_txt]
        
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
        frame_to_mode = {'eersteregel': 'base',
                         'tweederegel': 'comp',
                         'alleregels': 'total'}
                      
        frames_per_expression = [n.return_frames() for n in self.expressions]
        set_of_frames = reduce(or_, frames_per_expression)
        
        if len(set_of_frames) == 1:
            frame = list(set_of_frames)[0]
            return frame_to_mode[frame], 'irrelevant'
            
            
        elif len(set_of_frames) > 1:
            #This means we have a base and a comp frame.
            kwargs = {'frame_to_mode': frame_to_mode,
                      'frames_per_expression': frames_per_expression, 
                      'set_of_frames': set_of_frames}
                      
            return self.specify_constraint_mode_on_multiple_frames(**kwargs)
            
            
            
    def specify_constraint_mode_on_multiple_frames(self, frame_to_mode,
                                                   frames_per_expression,
                                                   set_of_frames):         
        e = 'Alle regels is not allowed in combination with other frames'
        assert 'alleregels' not in set_of_frames, e

        mode = 'real'
        
        if len(self.expressions) == 1:
            expr = self.expressions[0]
            abstr_str, abstr_dict = expr.return_abstract_representation()
            
            if len(abstr_dict[FrameWithColumn]) == 1: #Only one column dropped
                #Because only one column is named, we might be able to split on it.
                return mode, 'parallel single comparison'
                
            elif len(abstr_dict([FrameWithColumn])) > 1:
                #Two columns are mentioned, so it is non-parallel.
                return mode, 'non-parallel single comparison'
                
                
                
        elif len(self.expressions) > 1:
            from statistics import mean
            from statistics import stdev
            
            num_of_frames_per_expr = [len(n) for n in frames_per_expression] 
            avg_frame = mean(num_of_frames_per_expr)
            stdev_frame = stdev(num_of_frames_per_expr)
            
            abstr_reprs = [n.return_abstract_representation() for n in self.expressions]
            abstr_strings = []
            abstr_dicts = []
            for abstr_str, abstr_dict in abstr_reprs:
                abstr_strings.append(abstr_str)
                abstr_dicts.append(abstr_dict)
                
            
                
            if stdev_frame == 0.0:                
                if avg_frame == 1:
                    if all([n == ' or ' for n in self.boolean_ops_txt]):
                        return mode, 'external disjunction'
                        
                    elif all([n == ' and ' for n in self.boolean_ops_txt]):
                        return mode, 'external conjunction'
        
                    else: #A mix of ors and ands. 
                        return mode, 'unclassifiable'
                    
                elif avg_frame == 2:
                    return mode, 'juncted comparison'

            else: #This means that not all expresions have the same num of frames
                return mode, 'unclassifiable'
                

    def evaluate_constraint(self):        
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
                
                    
            parallel = are the same columns being compared throughout?
            single/disjunc/conjunc = only on       
            
            'parallel single comparison' -> possible splittable
            'non-parallel single comparison' -> just goes in 
            
            'disjunction' -> split into base and comp
            'disjunction' -> just goes in.
            
            
            'parallel conjunction' #-> make this a total statement 
            'non-parallel conjunction'
            
            
            
            'disjuncted comparison' #We are not going into these as much. Just put them in. 
            'conjuncted comparison' #-> Just make two constraints, this is clearer.
            
            'unclassifiable' #-> goes straight into real_constraints
            
            

A van eerste == var1 or  A van tweede == var1 -> Mixed parallel disjunction
A van eerste == var1 or  B van tweede == var1 -> Mixed non-parallel disjunction

A van eerste == var1 and A van tweede == var1 -> Mixed parallel conjunction (this could be alleregels)

A van eerste == var1 and B van tweede == var1 -> Mixed non-parallel conjunction (this should be split into base - comp)
A van eerste == var1 and A van tweede == var2 -> Mixed non-parallel conjunction (this should be split into base - comp)
A van eerste == var1 and B van tweede == var2 -> Mixed non-parallel conjunction (this should be split into base - comp)

#Intertrans constraints are constraints that directly compare values in the same frame
A van eerste == A van eerste -> The fuck you doing mate.
A van eerste == B van eerste -> Single intertrans constraint
A van eerste == B van eerste or A van eerste == C van eerste -> Mixed intertrans disjunction
A van eerste == B van eerste and A van eerste == C van eerste -> Mixed intertrans conjunction

#Real constraints are constraints that directly compare two different frames.
A van eerste == B van tweede or A van eerste == C van tweede -> Mixed real disjunction 
A van eerste == B van tweede -> non-parallel real constraint
A van eerste == A van tweede -> parallel real constraint (splittable/groupable)
"""

