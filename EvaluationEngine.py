# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 07:52:43 2016

@author: OffermanTW1
"""

from pandas import Series, DataFrame 

#Import regular operators and comparisons
from operator import lt, le, eq, ne, gt, ge
from operator import add, sub, truediv, mul

#Import custom operators and comparison



from operator import or_
from functools import reduce


from collections import Counter

def approx_local_ratio():
    #dummy
    pass




class EvaluationEngine():
    comparisons = {'<': lt,
                   '<=': le,
                   '==': eq,
                   '!=': ne,
                   '>': gt,
                   '>=': ge,
                   'zit in': None,
                   'zit niet in': None}
                   
    operators =   {'+': add,
                   '-': sub,
                   '/': truediv,
                   '*': mul,
                   'fuzzymatch met': approx_local_ratio}
                   
    precedence = {'**': 0,
                  '*': 1, '/': 1, 
                  '+': 2, '-': 2, 'fuzzymatch met': 2, 
                  '<=': 3, '<': 3, '>': 3, '>=': 3,
                  '==':4, '!=': 4,
                  'in': 5, 'not in': 5}

    connectors = {'from', 'van'}
    
    possible_frames = {'eerste regel', 'tweede regel', 'alle regels'}
    
    known_elements = reduce(or_, [{n for n in operators}, #
                                  {n for n in comparisons}, 
                                  connectors, 
                                  possible_frames])
        

                
    
    @classmethod
    def isoperator(cls, operator):
        return operator in cls.operators
    
    @classmethod    
    def iscomparison(cls, comparison):
        return comparison in cls.comparisons
       
    @classmethod
    def getcomparison(cls, comparison):
        try:
            return cls.comparisons[comparison]
        except:
            raise NameError("This comparison is not supported by the engine: " + str(comparison))
            
    @classmethod        
    def getoperator(cls, operator):
        try:
            return cls.operators[operator]
        except:
            raise NameError("This operator is not supported by the engine: " + str(operator))
            
    @classmethod
    def getprecedence(cls, symbol):
        try: 
            return cls.precedence[symbol]
        except:
            raise NameError("This operator/comparison is not supported by the engine: " + str(symbol))


class StatementElement():
    def __init__(self, element1, element2):
        self.element1 = element1
        self.element2 = element2
        
    def eval_op(self, operand, from_obj):
        return operand.evaluate_statement(from_obj)

    def evaluate_statement(self, from_obj):
        elements = [self.element1, self.element2]
        op1, op2 = [self.eval_op(n, from_obj) for n in elements]
        
        op1_pandas_struct = isinstance(op1, Series) or isinstance(op1, DataFrame) 
        op2_pandas_struct = isinstance(op2, Series) or isinstance(op2, DataFrame) 
        
        
        #It is important to change the syntax if one of the ops is a single value
        #It should then be: Pandas Structure -operator- single value
        
        if op1_pandas_struct and op2_pandas_struct: #Both are pandas struct
            return self.action(op1, op2)
            
        elif op1_pandas_struct:
            return self.action(op1, op2)
            
        elif op2_pandas_struct: 
            return self.action(op2, op1)
            
        else: #None are a pandas struct
            return self.action(op1, op2)
            
    def return_variables(self):
        def get_var_from_operand(operand):
            variables = set([])
            if isinstance(operand, StatementElement):
                variables = operand.return_variables()
            elif isinstance(operand, Variable):
                variables = {operand.return_description()}
                
                
            return variables
    
        var1 = get_var_from_operand(self.element1)
        var2 = get_var_from_operand(self.element2)
        
        variables = var1.union(var2)
        
        return variables
        
    def return_frames(self):
        def get_frames_from_operand(operand):
            frames = set([])
            if isinstance(operand, FrameWithColumn):
                frames = {operand.return_description()}

            elif isinstance(operand, StatementElement):
                frames =  operand.return_frames()
                
            return frames
            
        frame1 = get_frames_from_operand(self.element1)
        frame2 = get_frames_from_operand(self.element2)
        
        frames = frame1.union(frame2)
        
        return frames

    def return_abstract_repr(self):

        return self.action_obj.return_abstract_repr()

        
class OperatorStatement(StatementElement):
    def __init__(self, operator, operand1, operand2):
        self.action_obj = operator
        self.action = EvaluationEngine.getoperator(str(operator))
        super(OperatorStatement, self).__init__(operand1, operand2)

class ComparisonStatement(StatementElement):
    def __init__(self, operator,operand1, operand2):
        self.action_obj = operator
        self.action = EvaluationEngine.getcomparison(str(operator))
        super(ComparisonStatement, self).__init__(operand1, operand2)


class FrameWithColumn():
    def __init__(self, framename, column):
        self.frame = framename.replace(' ', '')
        self.column = column
        
    def evaluate_statement(self, from_obj):
        try:
            frame = getattr(from_obj, self.frame)
        except:
            raise NameError("Could not retrieve this frame: " + str(self.frame))
        try:           
            return frame[self.column]
        except: 
            raise NameError("This column is not in the frame: " + str(self.column))
            
    def return_description(self):
        return self.frame
		
    def return_abstract_repr(self):
        return '{0} Frame'.format(self.column)
        
class Variable:
    def __init__(self, description):
        self.description = description
        
    def evaluate_statement(self, from_obj):
        try:
            return getattr(from_obj, self.description)
        except:
            raise NameError("This variable is not defined")
            
    def return_description(self):
        return self.description
	
    def return_abstract_repr(self):
	    return self.return_description()
 
class OperCompar():
    def __init__(self, symbol):
        self.symbol = symbol
        
    def __str__(self):
        return self.symbol

    def getprecedence(self):
        return EvaluationEngine.getprecedence(self.symbol)
        
    def return_description(self):
        return self.symbol
    
    def return_abstract_repr(self):
        return self.return_description()
		
class Operator(OperCompar):
    pass
class Comparison(OperCompar):
    pass

        
    
        
class Expression():
    def __init__(self, string):
        self.object_elements = self.parse_expression(string)
        if len(self.object_elements) == 0:
            raise NameError('No object elements found')
        expression = self.construct_expression(self.object_elements)
        
        self.raw_expression = string
        self.expression = expression[0] 


    def parse_expression(self, string):

        for known_ in EvaluationEngine.known_elements:
            string = string.replace(" {0} ".format(known_), " # {0} #  ".format(known_))

        parsed_elements = []
        string = " " + string + " "

        elements = [n.strip() for n in string.split(" # ")]
        elements = [n for n in elements if n != '']                
        last_index = len(elements) - 1   

        for index, element in enumerate(elements):

            if element in EvaluationEngine.connectors:
                assert 0 < index < last_index
                column, frame = elements[index-1], elements[index+1]
                parsed_elements.append(FrameWithColumn(frame, column))
                
            elif element in EvaluationEngine.comparisons:
                parsed_elements.append(Comparison(element))
                
            elif element in EvaluationEngine.operators:
                parsed_elements.append(Operator(element))
                
            elif element in EvaluationEngine.possible_frames:
                error_string = "{0} not found in connectors, check hashtags".format(elements[index-1])
                assert elements[index-1] in EvaluationEngine.connectors, error_string
                
            elif index != last_index and elements[index+1] in EvaluationEngine.connectors:
                continue
            
            else:
                parsed_elements.append(Variable(element))
                
        return parsed_elements

    def construct_expression(self, object_elements):
        object_elements = list(object_elements) #So original stays the same
        
        precedences = []
        for index, obj in enumerate(object_elements):
            if isinstance(obj, OperCompar):
                precedences.append(index)
                
        indices = sorted(precedences, key = lambda x: object_elements[x].getprecedence())

        for i in range(len(indices)):
            index = indices[i]

            operand1, opcompar, operand2 = object_elements[index-1:index+2]

            if isinstance(opcompar, Comparison):
                obj = ComparisonStatement(opcompar, operand1, operand2)
                
            elif isinstance(opcompar, Operator):
                obj = OperatorStatement(opcompar, operand1, operand2)

            object_elements[index] = obj
            object_elements.pop(index+1)
            object_elements.pop(index-1)

 
            for remaining_index in range(i, len(indices[i:]) + i):
                if indices[remaining_index] > index:
                    indices[remaining_index] -= 2
        
        return object_elements
         
    def evaluate(self, from_obj):
        return self.expression.evaluate_statement(from_obj)
        
    def return_frames(self):
        e = 'return_frames only works on statements, not frames or variables'
        assert isinstance(self.expression, StatementElement), e
        return self.expression.return_frames()
        
    def return_variables(self):
        e = 'return_variables only works on statements, not frames or variables'
        assert isinstance(self.expression, StatementElement), e
        return self.expression.return_variables()
		
    def return_abstract_representation(self):
        abstr_string = ""
        from collections import defaultdict
        
        abstr_dict = defaultdict(set)
        #We use set because it will make it easier to determine whether
        #the same variable/column is mentioned in the frames 
        
        for obj in self.object_elements:
            abstr_repr = obj.return_abstract_repr()
            abstr_string += '{0} '.format(abstr_repr)
            abstr_dict[type(obj)].add(abstr_repr)

        return abstr_string.strip(), abstr_dict
        
    def compare_with_other_expression(self, other):
        self_str, self_dict = self.return_abstract_expression()
        other_str, other_dict = self.return_abstract_representation()
        #TO DO: make this 
        raise NameError('This function is still under construction')
        
   


