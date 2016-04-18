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
    
class OperatorStatement(StatementElement):
    def __init__(self, operator, operand1, operand2):
        self.action = EvaluationEngine.getdub_operator(str(operator))
        super(OperatorStatement, self).__init__(operand1, operand2)

class ComparisonStatement(StatementElement):
    def __init__(self, operator,operand1, operand2):
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
 
class OperCompar():
    def __init__(self, symbol):
        self.symbol = symbol
        
    def __str__(self):
        return self.symbol

    def getprecedence(self):
        return EvaluationEngine.getprecedence(self.symbol)
        
    def return_description(self):
        return self.symbol
    
class Operator(OperCompar):
    pass
class Comparison(OperCompar):
    pass

class LsideOperator():
    def __init__(symbol, operand):
        pass
    
class RsideOperator():
    def __init__(symbol, operand):
        pass
        