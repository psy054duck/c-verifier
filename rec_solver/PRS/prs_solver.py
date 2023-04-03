import sympy as sp
from sympy.core import symbol
from .condition import And, PolyCondition, ModCondition
from .closed_form import closed_form, symbolic_closed_form_linear, solve_rec_expr
# from .old_parser import parse
from .parser import parse
import os
import time

def is_linear_transition(transition):
    variables = transition.keys()
    for _, exp in transition.items():
        for v in variables:
            diff_v = sp.diff(exp, v, 2)
            if sp.simplify(diff_v) != 0:
                return False
    return True

def trans2matrix(transition, var_order):
    matrix = sp.eye(len(var_order))
    for i, v in enumerate(var_order):
        matrix[i, :] = exp2vec(transition[v], var_order)
    return matrix

def exp2vec(exp, var_order):
    cur_exp = exp
    vec = sp.zeros(1, len(var_order))
    for i, v in enumerate(var_order[:-1]):
        coeff = cur_exp.coeff(v)
        vec[i] = coeff
        cur_exp = cur_exp - coeff*v
    const_dummy = sp.Symbol('constant')
    vec[-1] = cur_exp if cur_exp != const_dummy else 1
    return vec

def solve(filename):
    with open(filename) as fp:
        recurrence = fp.read()
        res = solve_str(recurrence)
        return res


def solve_str(recurrence: str):
    cond, x0, A, variables, index = parse(recurrence)
    start = time.time()
    res = closed_form(A, x0, cond, variables, index, bnd=999999999999)
    # print(sp.expand(res[1][0].subs(index, 5)))
    # for i in range(6, 12):
    #     print(sp.expand(res[1][1].subs(index, i)))
    end = time.time()
    if res is None:
        return None
    return res, variables, index, end - start

def solve_sym_str(recurrence: str):
    cond, x0, str_transitions, variables, index = parse(recurrence)
    sp_transitions = [{sp.Symbol(v): e for v, e in trans.items()} for trans in str_transitions]
    initial_symbols = []
    for i, v in enumerate(x0):
        if v.is_symbol and v.name != 'constant':
            initial_symbols.append(v)
    if all(is_linear_transition(trans) for trans in sp_transitions):
        A = [trans2matrix(tran, variables) for tran in sp_transitions]
        res = symbolic_closed_form_linear(A, x0, cond, variables, index, bnd=99999999)
    else:
        #TODO non-linear case
        raise Exception('Non-linear Case Not Yet Implemented')
    return res, variables, initial_symbols

def solve_recurrence_expr(recurrence):
    conds, x0, str_transitions, variables, index = parse(recurrence)
    sp_transitions = [{sp.Symbol(v): e for v, e in trans.items()} for trans in str_transitions]
    if all(is_linear_transition(trans) for trans in sp_transitions):
        A = [trans2matrix(tran, variables) for tran in sp_transitions]
    else:
        raise Exception('Non-linear Case Not Yet Implemented')
    return solve_rec_expr(A, x0, conds, variables, index)

def solve_sym(filename):
    with open(filename) as fp:
        recurrence = fp.read()
        try:
            res = solve_sym_str(recurrence)
        except:
            res = solve_recurrence_expr(recurrence)
            print(res)
        return res