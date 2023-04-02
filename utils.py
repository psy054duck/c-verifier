import os
from subprocess import check_output
import z3
from z3.z3core import Z3_get_symbol_int
from rec_solver.sym_rec_solver import solve_individual_rec
import sympy as sp
from sympy.logic.boolalg import true, false
from functools import reduce

sim = z3.Then('ctx-simplify', 'unit-subsume-simplify')
def c2z3_preprocess(filename):
    TMP_PATH = 'temp/preprocessed.c'
    with open(filename) as fp:
        text = fp.read()
    text = '#define __attribute__(x)\n'\
         + '#define __extension__\n'\
         + '#include "assert.h"\n'\
         + text
    with open(TMP_PATH, 'w') as fp:
        fp.write(text)
    return os.path.abspath(TMP_PATH)

def query_z3(query, temp_file_postfix='', timeout=60):
    filename = 'temp/z3query%s.py' % temp_file_postfix
    with open(filename, 'w') as fp:
        fp.write(query)
    res = check_output(['python', filename], timeout=timeout).decode()
    return res

def solve_rec(recurrence_dict, variables, initial_values):
    conditions = {}
    simplified = {var: z3.simplify(value) for var, value in recurrence_dict.items()}
    variables_list = list(recurrence_dict.keys())
    addtional_variables = set(variables) - set(variables_list)
    variables = variables_list + list(addtional_variables)
    condition_list = []
    values_list = []
    for var in variables_list:
        translted_value = reverse_var_value_dict(simplified[var])
        values_list.append(list(translted_value.values()))
        condition_list.append(list(translted_value.keys()))
    index_list = _cartesion_product([list(range(len(l))) for l in condition_list])
    res_condition_list = []
    res_values_list = []
    for index in index_list:
        cond_list = []
        value_list = []
        for i, idx in enumerate(index):
            cond_list.append(condition_list[i][idx])
            value_list.append(values_list[i][idx])
        cond = z3.simplify(z3.And(*cond_list))
        res_condition_list.append(cond)
        res_values_list.append(value_list)
    translated = translate2rec_solver(res_condition_list, res_values_list, variables, initial_values)
    with open('temp/rec.txt', 'w') as fp:
        fp.write(translated)
    # rec_output = check_output(['python', 'rec_solver/sym_rec_solver.py', 'temp/rec.txt']).decode()
    closed = solve_individual_rec('temp/rec.txt')
    return closed

def reverse_var_value_dict(value):
    if _is_if(value):
        cond, left, right = value.children()
        left_cond_value_dict = reverse_var_value_dict(left)
        right_cond_value_dict = reverse_var_value_dict(right)
        new_left_cond_value_dict = {z3.simplify(z3.And(cond, c)): v for c, v in left_cond_value_dict.items()}
        new_right_cond_value_dict = {z3.simplify(z3.And(z3.Not(cond), c)): v for c, v in right_cond_value_dict.items()}
        new_left_cond_value_dict.update(new_right_cond_value_dict)
        return new_left_cond_value_dict
    else:
        return {True: value}

def translate2rec_solver(condition_list, var_value_list, var_list, initial_values):
    solver = z3.Solver()
    sim = z3.Then('ctx-simplify', 'ctx-solver-simplify')
    res_str = ''
    for var in var_list:
        if var in initial_values:
            res_str += '%s = %s;\n' % (var, initial_values[var])
        else:
            res_str += '%s = %s;\n' % (var, var)
    init_res_str = res_str
    acc = True
    for cond, value in zip(condition_list, var_value_list):
        simplified_cond = z3.simplify(z3.And(*sim(cond)[0]))
        if z3.is_false(simplified_cond): continue
        if solver.check(z3.And(acc, z3.Not(simplified_cond))) == z3.unsat:
            if acc is True:
                res_str += 'if (true) {\n'
            else:
                res_str += ' else {\n'
        elif res_str == init_res_str:
            res_str += 'if (%s) {\n' % simplified_cond
        else:
            res_str += ' else if (%s) {\n' % simplified_cond
        for i, var in enumerate(var_list):
            try:
                dummy = z3.Int('dummy_var')
                phi_list = sim(z3.And(cond, dummy == value[i]))[0]
                simplified_v = [phi for phi in phi_list if z3.is_eq(phi) and 'dummy_var' in str(phi)][0]
                children = simplified_v.children()
                assert(len(children) == 2)
                simplified_v = [d for d in children if str(d) != 'dummy_var' ][0]
                res_str += '\t%s = %s;\n' % (var, simplified_v)
            except:
                res_str += '\t%s = %s;\n' % (var, var)
        res_str += '}'
        acc = z3.And(acc, z3.Not(simplified_cond))
    return res_str.replace('Not', '!')

def _cartesion_product(l):
    if len(l) == 1:
        return [[e] for e in l[0]]
    first, remaining = l[0], l[1:]
    remaining_product = _cartesion_product(remaining)
    res = []
    for e in first:
        for r in remaining_product:
            res.append([e] + r)
    return res


def pull_ite(expr):
    expr = z3.simplify(expr, som=True)
    if z3.is_const(expr) or _is_if(expr):
        return expr
    if z3.is_add(expr):
        expr = sum(expr.children())
    elif z3.is_mul(expr):
        expr = reduce(lambda x, y: x*y, expr.children())
    children = expr.children()
    lhs, rhs = children
    op = lambda x, y: x + y if z3.is_add(expr) else x - y if z3.is_sub(expr) else x * y
    if z3.is_add(expr) or z3.is_sub(expr) or z3.is_mul(expr):
        lhs, rhs = pull_ite(children[0]), pull_ite(children[1])
        if _is_if(lhs) and not _is_if(rhs):
            cond, t, f = lhs.children()
            return z3.If(cond, op(t, rhs), op(f, rhs))
        elif _is_if(rhs) and not _is_if(lhs):
            cond, t, f = rhs.children()
            return z3.If(cond, op(lhs, t), op(lhs, f))
        elif not _is_if(lhs) and not _is_if(rhs):
            return op(lhs, rhs)
        else:
            raise Exception('both are If')
    else:
        raise Exception('not addition, subtraction, and mulplication')

def _is_if(expr):
    children = expr.children()
    return len(children) == 3 and z3.is_bool(children[0])

def all_z3_symbols(expr):
    if len(expr.children()) == 0:
        if z3.is_int_value(expr) or z3.is_rational_value(expr):
            return set()
        else:
            return {expr} - {z3.BoolVal(True), z3.BoolVal(False)}
    res = set()
    for c in expr.children():
        ret = all_z3_symbols(c)
        res = res.union(ret)
    return res

def my_substitute(expr, mapping):
    import re
    from z3 import And, Or, Not, If, Implies
    try:
        return z3.substitute(expr, mapping)
    except:
        for var in all_z3_symbols(expr):
            exec('%s = z3.Int("%s")' % (var, var))
        for _, mapped in mapping:
            for var in all_z3_symbols(mapped):
                exec('%s = z3.Int("%s")' % (var, var))
        for var, mapped in mapping:
            exec('%s = mapped' % var)
        new_expr = eval(str(z3.simplify(expr)).replace('\n', ''))
        return new_expr

def to_z3(sp_expr):
    self = sp.factor(sp_expr)
    self = pow_to_mul(self)
    if isinstance(self, sp.Add):
        res = sum([to_z3(arg) for arg in self.args])
    elif isinstance(self, sp.Mul):
        res = 1
        for arg in reversed(self.args):
            if arg.is_number and not arg.is_Integer:
                try:
                    res = (res*arg.numerator())/arg.denominator()
                except:
                    res = (res*arg.numerator)/arg.denominator
            else:
                res = res * to_z3(arg)
        return z3.simplify(res)
        # return reduce(lambda x, y: x*y, [to_z3(arg) for arg in reversed(self.args)])
    elif isinstance(self, sp.Piecewise):
        if len(self.args) == 1:
            res = to_z3(self.args[0][0])
        else:
            cond  = to_z3(self.args[0][1])
            res = z3.If(cond, to_z3(self.args[0][0]), to_z3(self.args[1][0]))
    elif isinstance(self, sp.And):
        res = z3.And(*[to_z3(arg) for arg in self.args])
    elif isinstance(self, sp.Or):
        res = z3.Or(*[to_z3(arg) for arg in self.args])
    elif isinstance(self, sp.Not):
        res = z3.Not(*[to_z3(arg) for arg in self.args])
    elif isinstance(self, sp.Gt):
        res = to_z3(self.lhs) > to_z3(self.rhs)
    elif isinstance(self, sp.Ge):
        res = to_z3(self.lhs) >= to_z3(self.rhs)
    elif isinstance(self, sp.Lt):
        res = to_z3(self.lhs) < to_z3(self.rhs)
    elif isinstance(self, sp.Le):
        res = to_z3(self.lhs) <= to_z3(self.rhs)
    elif isinstance(self, sp.Eq):
        res = to_z3(self.lhs) == to_z3(self.rhs)
    elif isinstance(self, sp.Ne):
        res = to_z3(self.lhs) != to_z3(self.rhs)
    elif isinstance(self, sp.Integer) or isinstance(self, int):
        res = z3.IntVal(int(self))
    elif isinstance(self, sp.Symbol):
        res = z3.Int(str(self))
    elif isinstance(self, sp.Rational):
        # return z3.RatVal(self.numerator, self.denominator)
        res = z3.IntVal(self.numerator) / z3.IntVal(self.denominator)
    elif isinstance(self, sp.Pow):
        if self.base == 0: res = z3.IntVal(0)
        else: raise Exception('%s' % self)
    elif isinstance(self, sp.Mod):
        res = to_z3(self.args[0]) % to_z3(self.args[1])
    elif isinstance(self, sp.Abs):
        res = z3.Abs(to_z3(self.args[0]))
    elif isinstance(self, sp.Sum):
        s = z3.Function('Sum', z3.IntSort(), z3.IntSort(), z3.IntSort(), z3.IntSort(), z3.IntSort())
        # expr, (idx, start, end) = self.args
        expr, *l = self.args
        res = to_z3(expr)
        for idx, start, end in l:
            res = s(res, to_z3(idx), to_z3(start), to_z3(end))
    elif self is true:
        res = z3.BoolVal(True)
    elif self is false:
        res = z3.BoolVal(False)
    elif self.is_Function:
        func = self.func
        args = self.args
        z3_func = z3.Function(func.name, *([z3.IntSort()]*(len(args) + 1)))
        res = z3_func(*[to_z3(arg) for arg in args])
    else:
        raise Exception('Conversion for "%s" has not been implemented yet: %s' % (type(self), self))
    return z3.simplify(res)

def pow_to_mul(expr):
    """
    Convert integer powers in an expression to Muls, like a**2 => a*a.
    """
    pows = list(expr.atoms(sp.Pow))
    if any(not e.is_Integer for b, e in (i.as_base_exp() for i in pows)):

        raise ValueError("A power contains a non-integer exponent")
    repl = zip(pows, (sp.Mul(*[b]*e,evaluate=False) for b,e in (i.as_base_exp() for i in pows)))
    return expr.subs(repl)

if __name__ == '__main__':
    n = z3.Int('n')
    s = z3.Int('s')
    print(all_z3_symbols(2**n + s*2 + 3))
