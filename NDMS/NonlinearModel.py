import sympy as sp, numpy as np
from .utils import process_vector_args, lambdify_with_vector_args

class NonlinearSystem(object):
    def __init__(self, state_equations, states, inputs, constants_values, dt=None):
        """
        state_equations is a vector valued expression, the derivative of each state.        

        states is a sympy matrix (vector) of the states, in desired order, matching 
        state_equations.
        """
        n_states, one_test = states.shape
        n_inputs, one_test = inputs.shape 
        n_states_test = len(state_equations)
        
        self.state_equations = state_equations
        self.states = states
        self.inputs = inputs
        self.constants_values = constants_values
        
        self.n_states = n_states
        self.n_inputs = n_inputs
        self.dt = dt
            
        self.callable_function = lambdify_with_vector_args(sp.flatten(states) + sp.flatten(inputs), \
            state_equations.subs(constants_values), modules="numpy")
    
    def copy(self):
        return NonlinearSystem(self.state_equations, self.states, self.inputs, self.constants_values, self.dt)

    def __call__(self,x,u):
        return self.callable_function(x,u)

def grad(f, basis):
    n = len(basis)
    return sp.Matrix([ 
        [ sp.diff(f[x],basis[y]) for y in range(len(basis)) ] \
            for x in range(len(f)) ])