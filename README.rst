
.. image:: https://travis-ci.org/scidam/solver.svg?branch=master
    :target: https://travis-ci.org/scidam/solver

About
=====

*A simple problem solver written in pure Python*

Module provides an easy way to solve various problems that require
calculations. Lets imagine a problem formulated in
a text file using a some template language. Some places
within the problem formulation text correspond to variables
that have default values. What does `to solve a problem` mean in this context?
To solve the problem is to 1) define output template (used to render solution), 2) write code
that exploits input variables, 3) set up output variables in the code and, finally, 4) 
render the solution template.
With help of solver classes these steps of getting a problem solution
can be made easily.

Solver features:
    * arbitrary and independent input and output markups
      used in problem formulation and solution templates.
    * ability of asynchronous problem solving (Celery is required).
    * heuristic testing of problem solvability.
    * using all of Python computational power (with third party libraries) to solve your problems.
    * using jinja2 template language to produce dynamic parts of a problem
      formulation/solution.


Requirements
============

The solver works under Python 2.7.x and Python 3.3 and higher. 
The only requirements:

- ``jinja2``
- ``six``


Installation
============

::

$ pip install python-solver

Testing
=======

To run tests run the command:

::

python -m solver.tests



Usage example
=============

**A simple test problem.** My name is John. I have 100 $.
I want to buy several papers. Each paper worth is 5 $. 
How many papers can I buy?


Test problem  (abstraction level) ::

    test_problem_template_formulation = """
    My name is {{username}}. I have {{total}} $.
    I want to buy several papers. Each paper worth is {{paper_cost}}$.
    How many papers can I buy?
    """

    test_problem_solution_code = """
    OUTPUTS['result']=INPUTS['total']/INPUTS['paper_cost']
    OUTPUTS['name'] = INPUTS['username']
    """
    test_problem_output_template="""
    My name is {{name}} and answer is {{result}}.
    """

    from solver import Task, Solver
    task = Task(test_problem_template_formulation,
                default_vals={'username': 'Dmitry',
                'total': 100, 'paper_cost': 20},
                solution_template=test_problem_output_template,
                code = test_problem_solution_code
                )
    psolver = Solver(task)

    # solve the problem
    psolver.solve()

    # or you can try to solve the problem asynchronously instead.
    # if error occur in async_solve, 
    # the solve() method will be invoked by default.
    psolver.async_solve()

    # Before getting the results check problem for solution is ready
    # (This step is required, when getting the solution asynchronously)
    if psolver.is_solved:
    	# Render output template
        task.render_outputs() 
        # Print rendered template or do something else
        print(task.output) 




