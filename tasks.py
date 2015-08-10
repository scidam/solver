
from base import Solver, InappropriateSolverTypeError

try:
    from celery import Celery
    celery_installed = True
except:
    celery_installed = False

if celery_installed:
    app = Celery('tasks', broker='amqp://guest@localhost//')
else:
    class app:
        '''Implements identity decorator.'''
        
        @staticmethod
        def task(func):
            '''Just identity decorator. Do nothing.'''
            func.delay = func
            return func
    
@app.task
def solve(x):
    if isinstance(x, Solver):
        x.solve()
    else:
        raise exceptions.InappropriateSolverTypeError('Use the instances of class `Solver` instead.')