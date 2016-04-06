# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 14:02:23 2016

@author: OffermanTW1
"""

from .Constraints.Factory.RBC_ConstraintFactory import RBC_ConstraintFactory
from ...Common.BaseBusinessRule import BaseBusinessRule
from pandas import DataFrame 


class RBC_BusinessRule(BaseBusinessRule):
    def __init__(self, exception):
        self.both_constraints = []
        self.base_constraints = []
        self.comp_constraints = []
        self.real_constraints = []
        self.split_constraints = []
        
        super().__init__(exception)
        
    def add_split(self, splitstring):
        self.split_constraints.append(splitstring)
        
    def isempty(self):
        if self.both_constraints:
            return False
        elif self.base_constraints:
            return False
        elif self.comp_constraints:
            return False
        elif self.real_constraints:
            return False
        elif self.split_constraints:
            return False
        else:
            return True

        
    def add_global_constraint(self, constrainttuple):
        settype = constrainttuple[0]
        new_constraint = constrainttuple[1]
        
        self.choose_constraint_location(settype, new_constraint)

    def add_constraint(self, settype, expression, expected_outcome = True, mode = 'default', **kwargs):
        
        
        new_constraint = RBC_ConstraintFactory.create_constraint(expression,
                                                                 expected_outcome,
                                                                 mode,
                                                                 **kwargs)
        self.choose_constraint_location(settype, new_constraint) 
             
    def choose_constraint_location(self, settype, new_constraint):
        if settype == 'both':
            self.both_constraints.append(new_constraint) 
            
        elif settype == 'base':
            self.base_constraints.append(new_constraint)
            
        elif settype == 'comp':
            self.comp_constraints.append(new_constraint)
            
        elif settype == 'real':
            self.real_constraints.append(new_constraint)
        
        else:
             raise NameError()
        
        
    def assert_rule(self, data, firstcall = True, split_index = 0):
        #We don't use no exceptions because we can't show no exceptions 
        #in comparative analysis. It would be a combinatorial explosion.
        if self.isempty():
            return None
            
        if data.empty:
            return None
            
        if firstcall:
            for constraint in self.both_constraints:
                data = data[constraint.evaluate(data, data)]


        

        split_index = split_index
        if self.split_constraints and split_index < len(self.split_constraints):
            splitstring = self.split_constraints[split_index]
            split_index += 1            
            
            groups = data.groupby(splitstring).groups
            groups = [groups[key] for key in groups if len(groups[key]) > 1]
            datasets = [data.loc[group] for group in groups]

            
            for dataset in datasets:
                self.assert_rule(dataset, False, split_index)

        else:
            base_data = data
            comp_data = data 


            for constraint in self.base_constraints:
                base_data = base_data[constraint.evaluate(base_data, base_data)]
                
            


            for constraint in self.comp_constraints:
                comp_data = comp_data[constraint.evaluate(comp_data, comp_data)]
                 
                 

            
            if base_data.empty or comp_data.empty:
                return None 
                
            for index, base in base_data.iterrows():

                candidates = comp_data.drop(index)
                

                indexo = 0 
                for constraint in self.real_constraints:
                    candidates = candidates[constraint.evaluate(base, candidates)]
                    indexo += 1


                    if candidates.empty:
                        break 
                    

                if not(candidates.empty):
                    for exception in candidates.index:

                        self.process_exception(base, candidates.loc[exception])
                    


                    
  
                    
                    