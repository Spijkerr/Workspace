class Expression():
    def __init__(self, string):
        object_elements = self.parse_expression(string)
        expression = self.construct_expression(object_elements)
        
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
                
            elif element in EvaluationEngine.double_operators:
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
        
    def construct_expression2(self, object_elements):
        """
        Make functionality for the creation of rside and lside operators
        """
        precedences = []
        for index, obj in enumerate(object_elements):
            if isinstance(obj, OperCompar):
                precedences.append(index)
                
                
        for i in range(len(indices)):
            index = indices[i]
            
            opcompar = object_elements[index]
            
            if isinstance(opcompar, (Comparison, Operator)):
                operand1 =  object_elements[index-1]
                operand2 =  object_elements[index+1]
                    
                if isinstance(opcompar, Comparison):
                    obj = ComparisonStatement(opcompar, operand1, operand2)
                    
                elif isinstance(opcompar, Operator):
                    obj = OperatorStatement(opcompar, operand1, operand2)
                    
                object_elements[index] = obj
                object_elements.pop(index+1)
                object_elements.pop(index-1)
    
                decrement_indices_by = 2

                        
            else:
                if isinstance(opcompar, LsideOperator):
                    operand_index = index - 1
                    obj = LsideOperator
                    
                
                elif isinstance(opcompar, RsideOperator):
                    operand_index = index + 1
                    obj = RsideOperator
                    
                operand = object_elements[operand_index]
                
                obj = obj(opcompar, operand)
                object_elements[index] = obj
                object_elements.pop(operand_index)

            for remaining_index in range(i, len(indices[i:]) + i):
                if indices[remaining_index] > index:
                    indices[remaining_index] -= decrement_indices_by            
         
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
        
        