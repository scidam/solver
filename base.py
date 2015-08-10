# -*- coding: utf-8 -*-
import re
import keyword
from jinja2 import Environment, Template
from jinja2.exceptions import TemplateSyntaxError
from jinja2.meta import find_undeclared_variables
import six
import numpy as np
import ast
import uuid
import datetime
import pickle
from StringIO import StringIO
  


def is_python_variable(my_var):
    '''Returns True if `my_var` is a valid python variable name.'''

    return True if re.match("[_A-Za-z][_a-zA-Z0-9]*$", my_var) \
        and not keyword.iskeyword(my_var) else False


#--------------------------------Exceptions definition--------------------------------------
class AbstractSolverException(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return repr(self.msg)


class AbstractTaskExcpetion(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return repr(self.msg)

class AbstractRenderException(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return repr(self.msg)


class InappropriateSolverTypeError(AbstractSolverException):
    '''Should raised when we use not Solver instances for a problem solution.'''
    pass
    
class TemplateOutputSyntaxError(AbstractRenderException):
    '''Raised if output template includes syntax errors'''
    
    pass



class OutputValuesError(AbstractRenderException):
    '''Raised when not all values are defined for output rendering.'''
    
    pass
#--------------------------------End of exception definitions--------------------------------


class Task:
    '''Base class to handle a problem instance.'''

    def __init__(self, content, solution_template='', default_vals=None, code=None):
#       public properties
        self.content = content
        self.output = ''
        self.default_vals = default_vals
        self.code = code
        self.output_vals = {}
        
#       private properties
        self._env = Environment()
        self._templateerror = False
        self._solution_template = solution_template
        
        try:
            self._allvars = find_undeclared_variables(self._env.parse(self.content))
        except TemplateSyntaxError:
            self._allvars = set([])
            self._templateerror = True
        if not bool(self._allvars):
            self._allvars = set([])
        
        self._template_output_error = False
        try:
            self._all_output_vars = find_undeclared_variables(self._env.parse(self._solution_template))
        except TemplateSyntaxError:
            self._all_output_vars = {}
            self._template_output_error = True
    
    def render_outputs(self):
        if self._all_output_vars and self._all_output_vars.issubset(set(self.output_vals.keys())):
            temp = Template(self._solution_template)
            self.output = temp.render(**self.output_vals)
        elif self._template_output_error:
            raise TemplateOutputSyntaxError('Check output template for correctness.')
        elif not self._template_output_error and not self._all_output_vars:
            self.output = self._solution_template
        elif self._all_output_vars and not self._all_output_vars.issubset(set(self.output_vals.keys())):
            raise OutputValuesError('Not all variables defined in `output_vals`.')
        else:
            self.output = ''
            
    def is_content_valid(self):
        '''Validate input template. '''
        
        if not self.content:
            return True

        if self._templateerror:
            return False

        return True
    
    def is_state_correct(self):
        '''Validate correctness of a problem. 
        
        A problem treated as a correct problem, if:
            1) Content template for a problem is valid, see `is_content_valid` method;
            2) All variables defined in the content has default values;

        '''
        
        if not self.is_content_valid():
            return False

        if self._allvars:
            if self._allvars.issubset(set(self.default_vals.keys())):
                return True
            else:
                return False
        else:
            return True
    
    @property
    def is_solved(self):
        '''returns True if `output_vals` exists otherwise False'''
        
        return True if self.output_vals else False
    
    
class Solver:
    def_input_code = '''
import pickle
from StringIO import StringIO 
        
_raw_input = ''
_tmpvar = StringIO(_raw_input)
    
INPUTS = pickle.load(_tmpvar)
    
OUTPUTS = {}
    '''
    def __init__(self, task, preamble='', postamble=''):
        '''Create a solver instance.
        
        '''
        self.task = task
        self.preamble = preamble
        self.postamble = postamble
        self._code = '# -*- coding: utf-8 -*- \n\n' + self.preamble + '\n\n' + \
            Solver.def_input_code + '\n\n' + self.task.code + '\n\n' + self.postamble
        
        self.created = datetime.datetime.now()
        self.start = None
        self.end = None
        self.id = uuid.uuid4().hex
        
        self._async_obj = None
        
    def is_solvable(self, silent=True):
        '''Check task solvability.
        
        Solvable task should have either emptry or compilable code.
        '''
        
        if not self.task.code:
            return True
        
        retvalue = True
        if silent:
            try:
                pcode = ast.parse(self._code)
                retvalue = True
            except:
                retvalue = False
            finally:
                return retvalue
        else:
            pcode = ast.parse(self._code)
            return retvalue
            
    def solve(self):
        
        if not self.is_solvable():
            raise NotImplementedError
        
        a_task_serial = StringIO()
        pickle.dump(self.task.default_vals, a_task_serial)
        a_task_serial.seek(0)
        pcode = ast.parse(self._code, mode='exec')
        transformer = ast.NodeTransformer()
        newcode = transformer.visit(pcode)
        for item in newcode.body:
            if isinstance(item, ast.Assign):
                if any(map(lambda x: getattr(x, 'id', None) == '_raw_input', item.targets)):
                    item.value = ast.Str(a_task_serial.read())
        newcode = ast.fix_missing_locations(newcode)
        cobj = compile(newcode, '<string>', mode='exec')
        evalspace = {}
        try:
            self.start = datetime.datetime.now()
            exec(cobj) in evalspace
            self.end = datetime.datetime.now()
        finally:
            if not self.end:
                self.start = None
                self.end = None
        if evalspace.get('OUTPUTS'):
            self.task.output_vals = evalspace.get('OUTPUTS')
    
    def async_solve(self):
        from tasks import solve
        self._async_obj = solve.delay(self)
    
    @property
    def is_solved(self):
        '''Solution status. When a problem is solved returns true.'''
        return True if self.end else False
        
    @property        
    def total(self):
        '''Total execution time.'''
        
        if self.start and self.end:
            return (self.end - self.start).seconds
        else:
            return datetime.timedelta(0).seconds

        