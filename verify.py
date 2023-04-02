from visitor import C2Z3Visitor
from preprocessor import preprocess
from rec_solver.PRS.mathematica_manipulation import session
from pycparser import parse_file
import time
import fire
import atexit
import os
import signal
import psutil

def exit_handler():
    session.terminate()
    print('exit successfully')

atexit.register(exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

def verify(filename):
    if not os.path.exists('temp'):
        os.mkdir('temp')
    preprocessed = preprocess(filename, 'temp/preprocessed.c')
    visitor = C2Z3Visitor()
    ast = parse_file(preprocessed)
    visitor.visit(ast)
    # to_preprossed_path = utils.c2z3_preprocess('/home/wangchenglin/Downloads/icra-master/WALi-OpenNWA/Examples/cprover/tests/frankenstein/HOLA/34.c')
    # ast = parse_file(to_preprossed_path, use_cpp=True)
    # visitor = C2Z3Visitor()
    # visitor.visit(ast)
    session.terminate()

def except_verify(filename):
    try:
        verify(filename)
        session.terminate()
    finally:
        session.terminate()
    # time.sleep(0.5)


if __name__ == '__main__':
    fire.Fire(except_verify)
    # verify('./benchmarks/pldi22/branching_loops_modified/leapfrog_safe.c')
    # verify('./benchmarks/pldi22/branching_loops/bobble.c')
    # verify('./benchmarks/pldi22/sv-comp/loops-crafted-1/iftelse.c')
    # verify('benchmarks/pldi22/branching_loops_modified/simple_bl_unbound_safe.c')
    # verify('benchmarks/sv-comp/loops-crafted-1/mono-crafted_6.c')
    # verify('/home/wangchenglin/pldi22/sv-comp/loop-lit/css2003.c')
    # verify('benchmarks/literature/5.c')
    # verify('benchmarks/pldi22/branching_loops/bobble2_unbound.c')
    # verify('examples/main_with_args.c')
    # verify('test6.c')
    # verify('benchmarks/literature/4.c')
    # verify('/Users/wangchenglin/OneDrive - HKUST Connect/WCL/submission-popl22/code/benchmarks/experiment/loop-acceleration/simple_1-2.c')
    # verify('examples/test_while_loop.c')
    # verify('examples/fsa.c')
    # verify('examples/test_nested_if.c')
    # verify('examples/loop_splitting_test_safe.c')
    # verify('examples/top-level-if-add-const_product.c')
    # verify('examples/AGHKTW2017_foo.c')
    # verify('examples/inter1.c')
    # verify('examples/01.c')
    # verify('benchmarks/HOLA/46.c')
