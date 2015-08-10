
import unittest
from base import Task, Solver, OutputValuesError, TemplateOutputSyntaxError
import numpy as np

class TestBaseTaskClass(unittest.TestCase):

    def setUp(self):
        self.bad_solver_variable_name = 'turipov'
        self.bad_python_variable_name = '1cot'
        self.valid_python_name = 'acat'
        self.valid_solver_variable_name = 'ivvec_matrix1'
        
#       Test problem definitions
#               Problem correctness
        self.correct_problem1 = Task('''My name is {{ivstr_name1}}. I am {{ivsca_myage}} y.o.
            Currently, I like the following sequence {{ivvec_vec1}}. Also, I like magic squares {{ivmat_mat1}}''', 
            default_vals={'ivstr_name1': 'Dmitry', 'ivsca_myage': 30.0, 'ivvec_vec1': np.random.rand(10), 
                          'ivvec_addval' : None, 'ivmat_mat1':np.random.rand(3,3)})
     
        self.incorrect_problem1 = Task('''My name is {{ivstr_name1}}. I am {{ivsca_myage}} y.o.
            Currently, I like the following sequence {{ivvec_vec1}}. Also, I like magic squares {{ivmat_mat1}}''', 
            default_vals={'ivvec_vec1': range(10), 'ivvec_addval' : None, 'ivmat_mat1':np.random.rand(3,3)})

#               Problem content validation
        self.invalid_content_problem1 = Task('''My name is {{ivstr_name1}. I am {{ivsca_myage}} y.o.
            Currently, I like the following sequence {{ivvec_vec1}}. Also, I like magic squares {{ivmat_mat1}}''')
       
    def test_check_content_valid(self):
        self.assertTrue(self.correct_problem1.is_content_valid())
        self.assertFalse(self.invalid_content_problem1.is_content_valid())
        
    def test_state_correctness(self):
        self.assertTrue(self.correct_problem1.is_state_correct())
        self.assertFalse(self.incorrect_problem1.is_state_correct())





class TestBaseSolverClass(unittest.TestCase):
    
    def setUp(self):
        
        self.validcodeproblem = Task('''My name is {{username}}. I have {{total}} $. I want to buy several papers. 
            Each paper worth is {{paper_cost}}$. How much papers can I buy?''',
            default_vals={'username':'Dmitry', 'total': 100, 'paper_cost': 20},
            code='''OUTPUTS['result']=INPUTS['total']/INPUTS['paper_cost']''')
        
        self.notsolvableproblem = Task('''My name is {{username}}. I have {{total}} $. I want to buy several papers. 
            Each paper worth is {{paper_cost}}$. How much papers can I buy?''',
            default_vals={'username':'Dmitry', 'total': 100, 'paper_cost': 20},
            code='''OUTPUTS['result']=INPUTS['total']-/INPUTS['paper_cost']''')
        
        self.solver = Solver(self.validcodeproblem)
        self.answer = {'result' : 5}
        
    def test_solver_creation(self):
        solver = Solver(self.validcodeproblem)
        unsolver = Solver(self.notsolvableproblem)
        self.assertEqual(solver.total, 0)
        self.assertTrue(solver.is_solvable(silent=False))
        self.assertFalse(unsolver.is_solvable())
        
    def test_solver(self):
        self.solver.solve()
        self.assertEqual(self.validcodeproblem.output_vals, self.answer)
        self.assertIsNotNone(self.solver.start)
        self.assertIsNotNone(self.solver.created)
        self.assertIsNotNone(self.solver.end)
        

    def test_async_solver(self):
        self.solver.async_solve()
        self.assertEqual(self.validcodeproblem.output_vals, self.answer)
        self.assertTrue(self.solver.is_solved)
        
        


class TestTaskRendererClass(unittest.TestCase):
    
    def setUp(self):
        
        self.validcodeproblem = Task('''My name is {{username}}. I have ${{total}}. I want to buy several papers. 
            Each paper worth is ${{paper_cost}}. How much papers can I buy?''',
            default_vals={'username':'Dmitry', 'total': 100, 'paper_cost': 20},
            code='''OUTPUTS['result']=INPUTS['total']/INPUTS['paper_cost']''', 
            solution_template='''Your answer is ${{result}}.''')
        self.invalidcodeproblem = Task('''My name is {{username}}. I have {{total}} $. I want to buy several papers. 
            Each paper worth is ${{paper_cost}}. How much papers can I buy?''',
            default_vals={'username':'Dmitry', 'total': 100, 'paper_cost': 20},
            code='''OUTPUTS['result']=INPUTS['total']/INPUTS['paper_cost']''', 
            solution_template='''My name is {{name}} and answer is {{result}}.''')
        
        self.invalidtemplateproblem = Task('''My name is {{username}}. I have ${{total}}. I want to buy several papers. 
            Each paper worth is $ {{paper_cost}}. How much papers can I buy?''',
            default_vals={'username':'Dmitry', 'total': 100, 'paper_cost': 20},
            code='''OUTPUTS['result']=INPUTS['total']/INPUTS['paper_cost']''', 
            solution_template='''My answer is ${{result}.''')
        
        
        self.solver = Solver(self.validcodeproblem)
        self.inv_solver = Solver(self.invalidcodeproblem)
        self.inv_temp =  Solver(self.invalidtemplateproblem)
       
    def test_output_renderer(self):
        self.solver.solve()
        self.inv_solver.solve()
        self.inv_temp.solve()
        self.validcodeproblem.render_outputs()
        self.assertEqual(self.validcodeproblem.output, 'Your answer is $5.')
        try:    
            self.invalidcodeproblem.render_outputs()
        except OutputValuesError:
            self.assertTrue(True)
        try:
            self.invalidtemplateproblem.render_outputs()
        except TemplateOutputSyntaxError:
            self.assertTrue(True)
            

        
if __name__ == '__main__':
    unittest.main()