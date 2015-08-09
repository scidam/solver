
import unittest
from base import is_python_variable, is_valid_variable, check_variable_value,\
                 Task
import numpy as np



class TestBaseSolverClasses(unittest.TestCase):

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
            default_vals={'ivstr_name1': 'Dmitry', 'ivsca_myage': '10.0', 'ivvec_vec1': np.random.rand(10), 
                          'ivvec_addval' : None, 'ivmat_mat1':np.random.rand(3,3)})
        
        self.incorrect_problem2 = Task('''My name is {{ivstr_name1}}. I am {{ivsca_myage}} y.o.
            Currently, I like the following sequence {{ivvec_vec1}}. Also, I like magic squares {{ivmat_mat1}}''', 
            default_vals={'ivstr_name1': 7, 'ivsca_myage': 10, 'ivvec_vec1': np.random.rand(10), 
                          'ivvec_addval' : None, 'ivmat_mat1':np.random.rand(3,3)})

        self.incorrect_problem3 = Task('''My name is {{ivstr_name1}}. I am {{ivsca_myage}} y.o.
            Currently, I like the following sequence {{ivvec_vec1}}. Also, I like magic squares {{ivmat_mat1}}''', 
            default_vals={'ivstr_name1': 'Dmitry', 'ivsca_myage': 30.0, 'ivvec_vec1': np.random.rand(10), 
                          'ivvec_addval' : None, 'ivmat_mat1':np.random.rand(1,3)})
            
        self.incorrect_problem4 = Task('''My name is {{ivstr_name1}}. I am {{ivsca_myage}} y.o.
            Currently, I like the following sequence {{ivvec_vec1}}. Also, I like magic squares {{ivmat_mat1}}''', 
            default_vals={'ivstr_name1': 'Dmitry', 'ivsca_myage': 30.0, 'ivvec_vec1': np.random.rand(10,10), 
                          'ivvec_addval' : None, 'ivmat_mat1':np.random.rand(3,3)})            

        self.incorrect_problem5 = Task('''My name is {{ivstr_name1}}. I am {{ivsca_myage}} y.o.
            Currently, I like the following sequence {{ivvec_vec1}}. Also, I like magic squares {{ivmat_mat1}}''', 
            default_vals={'ivstr_name1': ['Dmitry'], 'ivsca_myage': 30.0, 'ivvec_vec1': range(10), 
                          'ivvec_addval' : None, 'ivmat_mat1':np.random.rand(3,3)})
        
        self.incorrect_problem6 = Task('''My name is {{ivstr_name1}}. I am {{ivsca_myage}} y.o.
            Currently, I like the following sequence {{ivvec_vec1}}. Also, I like magic squares {{ivmat_mat1}}''', 
            default_vals={'ivsca_myage': 30.0, 'ivvec_vec1': range(10), 
                          'ivvec_addval' : None, 'ivmat_mat1':np.random.rand(3,3)})

#               Problem content validation
        self.invalid_content_problem1 = Task('''My name is {{ivstr_name1}. I am {{ivsca_myage}} y.o.
            Currently, I like the following sequence {{ivvec_vec1}}. Also, I like magic squares {{ivmat_mat1}}''')

        self.invalid_content_problem2 = Task('''My name is {{ifvstr_name1}}. I am {{ivsca_myage}} y.o.
            Currently, I like the following sequence {{ivvec_vec1}}. Also, I like magic squares {{ivmat_mat1}}''')
        
    def test_allowed_variable_names(self):
        self.assertTrue(is_valid_variable(self.valid_solver_variable_name))
        self.assertFalse(is_valid_variable(self.bad_solver_variable_name))
        self.assertFalse(is_valid_variable(self.bad_python_variable_name))
        self.assertFalse(is_valid_variable(self.valid_python_name))
        self.assertTrue(is_python_variable(self.valid_python_name))
        self.assertTrue(is_python_variable(self.valid_solver_variable_name))
        self.assertTrue(is_python_variable(self.bad_solver_variable_name))
        self.assertFalse(is_python_variable(self.bad_python_variable_name))
        
    def test_check_variable_values(self):
        self.assertTrue(check_variable_value('ivvec_vector1', range(10)))
        self.assertTrue(check_variable_value('ivvec_vector2', np.array(range(10))))
        self.assertFalse(check_variable_value('ivvec_vector3', np.random.rand(10,10)))
        self.assertTrue(check_variable_value('ivvec_vector4', np.random.rand(10,1)))
        self.assertTrue(check_variable_value('ivmat_array1', np.random.rand(10,10)))
        self.assertTrue(check_variable_value('ivsca_ups1', 10))
        self.assertTrue(check_variable_value('ivsca_ups1', 10.0))
        self.assertTrue(check_variable_value('ivsca_ups1', np.int32(10)))
        self.assertTrue(check_variable_value('ivsca_ups1', np.float128(10)))
        
    def test_check_content_valid(self):
        self.assertTrue(self.correct_problem1.is_content_valid())
        self.assertFalse(self.invalid_content_problem1.is_content_valid())
        self.assertFalse(self.invalid_content_problem2.is_content_valid())
        
    def test_state_correctness(self):
        self.assertTrue(self.correct_problem1.is_state_correct())
        self.assertFalse(self.incorrect_problem1.is_state_correct())
        self.assertFalse(self.incorrect_problem2.is_state_correct())
        self.assertFalse(self.incorrect_problem3.is_state_correct())
        self.assertFalse(self.incorrect_problem4.is_state_correct())
        self.assertFalse(self.incorrect_problem5.is_state_correct())
        self.assertFalse(self.incorrect_problem6.is_state_correct())
        
        
if __name__ == '__main__':
    unittest.main()