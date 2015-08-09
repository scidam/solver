# -*- coding: utf-8 -*-
import re
import keyword
from jinja2 import Environment
from jinja2.exceptions import TemplateSyntaxError
from jinja2.meta import find_undeclared_variables
import six
import numpy as np

ALLOWED_VARIABLE_TYPES = ['ivvec', 'ivsca', 'ivmat', 'ivimg', 'ivstr']

VARTYPE_PAT = re.compile(r'(iv[a-z]{3,3})_.*$')


def is_python_variable(my_var):
    '''Returns True if `my_var` is a valid python variable name.'''

    return True if re.match("[_A-Za-z][_a-zA-Z0-9]*$", my_var) \
        and not keyword.iskeyword(my_var) else False


def check_variable_value(varname, varvalue):
    '''Because of part of a variable name declares 
    value type stored in the variable, we should ensure 
    assigned value to be desired type.
    
    Returns True if `varvalue` is allowed by the type declared in `varname` and 
    False otherwise.
    '''
    
    if VARTYPE_PAT.match(varname):
        vartype = VARTYPE_PAT.findall(varname)[0]

        if vartype == 'ivstr':
            if isinstance(varvalue, six.string_types):
                return True
            else:
                return False
        
        if vartype == 'ivvec':
            if isinstance(varvalue, (list, np.ndarray)):
                return True if (min(np.shape(varvalue))==1 and \
                    len(np.shape(varvalue))==2) or \
                        len(np.shape(varvalue))==1 else False
            else:
                return False
            
        if vartype == 'ivmat':
            if isinstance(varvalue, (list,np.ndarray)):
                return True if min(np.shape(varvalue))>1 else False
            else:
                return False
            
        if vartype == 'ivsca':
            if isinstance(varvalue, (float, np.floating, int, np.integer)):
                return True
            else:
                return False
            
        if vartype == 'ivimg':
            raise NotImplementedError
    else:
        return False
    

def is_valid_variable(x):
    '''Check for variable name `x` is valid.

    It is assumed that the variable name declared in a template is a valid
    variable name if (and only if):

        1) It is a valid python variable name
        2) A prefex of the `x` is in ALLOWED_VARIABLE_TYPES, e.g.
           x = 'ivvec_myname1' or x = 'ivmat_myvar10'

    '''

    if not VARTYPE_PAT.match(x):
        return False
    if VARTYPE_PAT.findall(x)[0] not in ALLOWED_VARIABLE_TYPES:
        return False
    elif is_python_variable(x):
        return True
    else:
        return False

class Task:
    '''Base class to handle a problem instance.'''

    def __init__(self, content, output='', default_vals=None):
#       public properties
        self.content = content
        self.output = output
        self.default_vals = default_vals

#       private properties
        self._env = Environment()
        self._templateerror = False
        try:
            self._allvars = find_undeclared_variables(self._env.parse(self.content))
        except TemplateSyntaxError:
            self._allvars = set([])
            self._templateerror = True
        if not bool(self._allvars):
            self._allvars = set([])
        
            
    def is_content_valid(self):
        '''Validate input template. '''
        
        if not self.content:
            return True

        if self._templateerror:
            return False

        if self._allvars:
            for item in self._allvars:
                if not is_valid_variable(item):
                    return False
        return True
    
    def is_state_correct(self):
        '''Validate correctness of a problem. 
        
        A problem treated as a correct problem, if:
            1) Content template for a problem is valid, see `is_content_valid` method;
            2) All variables has valid names; see `is_valid_variable` function;
            3) All variables defined in the content has default values;

        '''
        
        if not self.is_content_valid():
            return False

        if self._allvars:
            if self._allvars.issubset(set(self.default_vals.keys())):
                for varname in self._allvars:
                    if not check_variable_value(varname, self.default_vals.get(varname, None)):
                        return False
            else:
                return False
        else:
            return False
        return True
            
        
        