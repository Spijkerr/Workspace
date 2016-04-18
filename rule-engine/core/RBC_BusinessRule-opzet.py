# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 10:43:10 2016

@author: Thomas
"""

class BusinessRule():
    def __init__(self):
        self.totalconstraints = []
        self.baseconstraints = []
        self.compconstraints = [] 
        self.groupbyconstraints = [] #Beide regels - gelijk
        self.slidingconstraints = [] #Beide regels - met offset
        self.inversedisjunctions = [] #Precies een
        self.complimentarydisjunctions = [] #Minstens eens 
        self.realconstraints = [] #Misc
        
        
    def evaluate_rule(self, data):
        analyzed_data = data.copy()
        for constraint in self.totalconstraints:
            analyzed_data = analyzed_data[constraint.assertself(alleregels = analyzed_data)]
            

        def analyze_constraints(data, column, list_of_constraints):
            for constraint in list_of_constraints:
                if column == 'Base':
                    result = constraint.assertself(eersteregel = data)
                elif column == 'Comp':
                    result = constraint.assertself(tweederegel = data)
                data[column] = data[column] && result
                
        analyzed_data['Base'] = True #set whole column to True
        analyzed_data['Comp'] = True #set whole column to True
        analyze_constraints(analyzed_data, 'Base', self.baseconstraints)
        analyze_constraints(analyzed_data. 'Comp', self.compconstraints)
        
        for conindex, constraint in enumerate(self.complimentaryconstraints):
            col = '_compl {0}'.format((conindex))
            analyzed_data[col] = constraint.assertself(minstenseenvanderegels = analyzed_data)
            
        
        candidates = [analyzed_data]
        for constraint in self.groupbyconstraints:
            candidates = [constraint.assertself(beideregels = n) for n in candidates]
            candidates = [n for n in candidates if len(n) > 1)]

        #Now we have a list of frames (all bigger than 1)
       
        #Now we will split them on complimentary constraints:
        candidates = [split_on_compl_constraint(n) for n in candidates]
        
        for constraint in slidingconstraints:
            candidates = [constraint.assertself(beideregels = n) for n in candidates]
            candidates = [n for n in candidates if n[1] > 0]
            
        candidates = [(b[b['Base']],c[c['Comp']] for b,c, in candidates]
        #TO DO : Write the real constraint evaluations
            
        
        
            
            
        
        
        
            
            
            
            