import unittest 
from pandas import DataFrame, Series 
from EvaluationEngine import Expression

        
                
class TestObj():
    def __init__(self, eersteregel = None,tweederegel = None, alleregels = None, 
                 var1 = None, var2 = None):
        self.eersteregel = eersteregel
        self.tweederegel = tweederegel
        self.alleregels = alleregels
        self.var1 = var1
        self.var2 = var2
    


import unittest 
from pandas import DataFrame, Series 

class ExpressionTester():
    def evaluate_expression(self, expression_text):
        expr = Expression(expression_text)
        return expr.evaluate(self.testobj).tolist()

        
class ExpressionIntegerDFTest(unittest.TestCase, ExpressionTester):
    list1 = [[1,2,3],[2,2,2],[3,3,3]]
    list2 = [[1,2,3],[4,4,4],[9,9,9]]   
    
    df1 = DataFrame(list1, columns = ['A','B','C'])
    df2 = DataFrame(list2, columns = ['A','B','C']) 
    var1 = 9
    var2 = 40
    
    testobj = TestObj(df1, df2, df1, var1, var2) 
    
    
    def evaluate_expression(self, expression_text):
        expr = Expression(expression_text)
        return expr.evaluate(self.testobj).tolist()
    
#   Basic comparisons
    def test_dataframe_eq_dataframe1(self):
        expr = Expression('A van eerste regel == B van tweede regel ')
        result = expr.evaluate(self.testobj)

        assert result.tolist() == [False, False, False]
        
    def test_dataframe_ge_dataframe1(self):
        expr = Expression('A van eerste regel >=  A van tweede regel ')
        result = expr.evaluate(self.testobj)
        
        assert result.tolist() == [True, False, False]
        

    def test_dataframe_gt_dataframe1(self):
        expr = Expression('A van tweede regel > B van eerste regel ')
        result = expr.evaluate(self.testobj)
        
        assert result.tolist() == [False, True, True]

    def test_dataframe_lt_dataframe1(self):
        expr = Expression('A van tweede regel < B van eerste regel ')
        result = expr.evaluate(self.testobj)
        
        self.assertEqual(result.tolist(),[True, False, False])
    
    def test_dataframe_le_dataframe1(self):
        expr = Expression('A van eerste regel <= B van eerste regel ')
        result = expr.evaluate(self.testobj)
        
        self.assertEqual(result.tolist(),[True, True, True])
    
    def test_dataframe_ne_dataframe1(self):
        expr = Expression('A van tweede regel != A van eerste regel ' )
        result = expr.evaluate(self.testobj)
        
        self.assertEqual(result.tolist(), [False, True, True])
        
#   Some operations
    
    def test_dataframe_plus_dataframe(self):
        expr = Expression('A van tweede regel + A van eerste regel ')
        result = expr.evaluate(self.testobj)
        
        self.assertEqual(result.tolist(), [2, 6, 12])
        
    def test_dataframe_minus_dataframe(self):
        result = self.evaluate_expression('A van tweede regel - A van eerste regel ')
        
        self.assertEqual(result, [0, 2, 6])
        
 
class ExpressionIntegerSeriesTest(unittest.TestCase, ExpressionTester):
    list1 = [1,2,3]
    list2 = [[1,2,3],[4,4,4],[9,9,9]]   
    series1 = Series(list1, index = ['A','B', 'C'])
    df2 = DataFrame(list2, columns = ['A','B','C']) 
    

    var1 = 8
    var2 = 40
    
    testobj = TestObj(series1, df2, series1, var1, var2) 
    
    def evaluate_expression(self, expression_text):
        expr = Expression(expression_text)
        return expr.evaluate(self.testobj).tolist()
        
    def test_series_eq_dataframe(self):
        result = self.evaluate_expression('A van eerste regel == A van tweede regel ')
        self.assertEqual(result, [True, False, False])
        
    def test_series_ne_dataframe(self):
        result = self.evaluate_expression('A van eerste regel != A van tweede regel ')
        self.assertEqual(result, [False, True, True])
        
    def test_series_plus_dataframe(self):
        result = self.evaluate_expression('A van eerste regel + A van tweede regel ')
        self.assertEqual(result, [2,5,10])
        
    def test_series_minus_dataframe(self):
        result = self.evaluate_expression('A van eerste regel - A van tweede regel ')
        self.assertEqual(result, [0, 3, 8])
        
    def test_series_operation_and_comparison(self):
        result = self.evaluate_expression('A van eerste regel - A van tweede regel == var1 ')
        self.assertEqual(result, [False, False, True])
        
    def test_series_operation_and_comparison1(self):
        result = self.evaluate_expression('A van eerste regel - A van tweede regel <= var2 ')
        self.assertEqual(result, [True, True, True])
        

    def test_dataframe_eq_variable1d_(self):
        expr = Expression('A van tweede regel  == var1')
        result = expr.evaluate(self.testobj)

        assert result.tolist() == [False, False, False]

class TestRealisticcolumnsTest(unittest.TestCase, ExpressionTester):
    list1 = [1,2,3]
    list2 = [[1,2,3],[4,4,4],[9,9,9]]   
    series1 = Series(list1, index = ['Boekingsdatum.','Doc.nr.', 'Doc nr2'])
    df2 = DataFrame(list2, columns = ['Bedrag in EV','B','C']) 
    

    var1 = 8
    var2 = 40
    
    testobj = TestObj(series1, df2, series1, var1, var2) 
    
    def test_compare_with_spaces1(self):
        result = self.evaluate_expression('Boekingsdatum. van eerste regel == Bedrag in EV van tweede regel')
        self.assertEqual(result, [True, False, False])
        
    def test_compare_with_spaces2(self):
        result = self.evaluate_expression('Bedrag in EV van tweede regel == var1')
        self.assertEqual(result, [False, False, False])
    
    def test_compare_with_spaces3(self):
        result = self.evaluate_expression('Doc nr2 van eerste regel == var1')
        self.assertEqual(result, False)
        
        
class TestVariableandFramereturning(unittest.TestCase):
    
    def test1(self):
        expr = Expression('Boekingdatum van eerste regel + Boekingsdatum van tweede regel == vandaag')
        frames = expr.return_frames()
        variables = expr.return_variables()
        
        self.assertEqual(frames,{'eersteregel', 'tweederegel'})
        self.assertEqual(variables,{'vandaag'})
        
    def test2(self):
        expr = Expression('var1 == var2 + var3 == var4')
        frames = expr.return_frames()
        variables = expr.return_variables()
        
        self.assertEqual(frames, set())
        self.assertEqual(variables, {'var1', 'var2', 'var3', 'var4'})
        
    def test3(self):
        expr = Expression('Boekingsdatum van eerste regel == Boekingsdatum van eerste regel')
        frames = expr.return_frames()
        variables = expr.return_variables()
        
        self.assertEqual(frames, {'eersteregel'})
        self.assertEqual(variables, set())


import EvaluationEngine        
class TestAbstractExprRepresentation(unittest.TestCase):
    frames = EvaluationEngine.FrameWithColumn
    variables = EvaluationEngine.Variable
    comparison = EvaluationEngine.Comparison
    operator = EvaluationEngine.Operator

    def testabstr_string1(self): 
        expr = Expression('Boekingsdatum van eerste regel + Boekingsdatum van tweede regel == var1')
        result, ddict = expr.return_abstract_representation()
        
        self.assertEqual(result, 'Boekingsdatum Frame + Boekingsdatum Frame == var1')

    def testabstr_string2(self):
        expr = Expression('Boekingsdatum van eerste regel == Boekingsdatum van eerste regel')
        result, ddict = expr.return_abstract_representation()
        
        self.assertEqual(result, 'Boekingsdatum Frame == Boekingsdatum Frame')
    
    def testabstr_string3(self):
        expr = Expression('Boekingsdatum van alle regels == var1')
        result, ddict = expr.return_abstract_representation()
        
        self.assertEqual(result, 'Boekingsdatum Frame == var1')
        
        
    def testabstr_dict1(self): 
        expr = Expression('Boekingsdatum van eerste regel + Boekingsdatum van tweede regel == var1')
        result, ddict = expr.return_abstract_representation()
        
        self.assertEqual(ddict[self.frames], ['Boekingsdatum Frame', 'Boekingsdatum Frame'])
        self.assertEqual(ddict[self.variables], ['var1'])
        self.assertEqual(ddict[self.comparison], ['=='])
        self.assertEqual(ddict[self.operator], ['+'])


    def testabstr_dict2(self):
        expr = Expression('Boekingsdatum van eerste regel == Boekingsdatum van eerste regel')
        result, ddict = expr.return_abstract_representation()
        

        self.assertEqual(ddict[self.frames], ['Boekingsdatum Frame', 'Boekingsdatum Frame'])
        self.assertEqual(ddict[self.variables], [])
        self.assertEqual(ddict[self.comparison], ['=='])
        self.assertEqual(ddict[self.operator], [])


    def testabstr_dict3(self):
        expr = Expression('Boekingsdatum van alle regels == var1')
        result, ddict = expr.return_abstract_representation()
        
        self.assertEqual(ddict[self.frames], ['Boekingsdatum Frame'])
        self.assertEqual(ddict[self.variables], ['var1'])
        self.assertEqual(ddict[self.comparison], ['=='])
        self.assertEqual(ddict[self.operator], [])
        
        
    
if __name__ == '__main__':
    test_classes_to_run = [TestVariableandFramereturning, TestRealisticcolumnsTest, 
                           ExpressionIntegerSeriesTest, ExpressionIntegerDFTest,
                           TestAbstractExprRepresentation]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
