import os
from subprocess import check_output, STDOUT, CalledProcessError
import csv
import time

# bench_path = '/home/wangchenglin/branching_loops_modified'
# bench_path = '/home/wangchenglin//icra/WALi-OpenNWA/Examples/cprover/tests/frankenstein/HOLA'
# bench_path = '/home/wangchenglin/c2z3/benchmarks/pldi22/sv-comp'
# bench_path = '/home/wangchenglin/c2z3/benchmarks/literature'
# bench_path = '/home/wangchenglin/function91'
# bench_path = './benchmarks/pldi22/branching_loops'
# bench_path = './benchmarks/pldi22/function91'
# bench_path = './benchmarks/pldi22/literature'
# bench_path = './benchmarks/pldi22/branching_loops_modified'
# bench_path = './benchmarks/pldi22/sv-comp-branch'
bench_path = './benchmarks/pldi22/sv-comp-simple'
tot = 0
success = 0
fails = 0
csv_file = open('stat.csv', 'w', newline='')
ground_truth_csv = open('./ground_truth.csv', newline='')
csv_writer = csv.writer(csv_file)
csv_reader = csv.DictReader(ground_truth_csv)
bench_prefix = './benchmarks'
benchmarks = os.listdir('benchmarks')
csv_writer.writerow(['program', 'predicted', 'ground truth', 'time'])

res_map = {}

for dir_name in benchmarks:
    for prefix, _, files in os.walk(os.path.join(bench_prefix, dir_name)):
        for c_file in files:
            if not c_file.endswith('.c'): continue
            # if not c_file == 'Mono1_1-1.c': continue
            tot += 1
            full_c_path = os.path.join(prefix, c_file)
            print("Verifying " + full_c_path)
            end = 0
            try:
                s = time.time()
                out = check_output(['python', 'verify.py', full_c_path], stderr=STDOUT, timeout=60).decode()
                # end = time.time()
            except CalledProcessError as e:
                out = e.output.decode()
            except:
                out = ''
            predicted = 'Correct'
            if 'Correct' in out or 'Wrong' in out:
                success += 1
                t = time.time() - s
                if 'Correct' in out:
                    predicted = 'Correct'
                    print('correct')
                else:
                    predicted = 'Wrong'
                    print('wrong')
            else:
                fails += 1
                t = 'None'
                predicted = 'Unknown'
                print('fail')
            short_path = os.path.join(dir_name, c_file)
            ground = 'Correct'
            for row in csv_reader:
                if row['program'] == short_path:
                    ground = row['ground']
                    break
            csv_writer.writerow([short_path, predicted, ground, t])
            if 'exit successfully' in out:
                print('exit successfully')
            print('%d/%d' % (success, tot))
            print('*'*20)
            res_map.setdefault(dir_name, [0, 0, 0, 0])
            if ground == 'Wrong':
                res_map[dir_name][1] += 1
            else:
                res_map[dir_name][0] += 1
            if ground == 'Wrong' and ground == predicted:
                res_map[dir_name][3] += 1
            elif ground == 'Correct' and ground == predicted:
                res_map[dir_name][2] += 1
        
print('%d/%d' % (success, tot))
csv_writer.writerow(['benchmark name', '# of safe / # of unsafe', 'predict # of safe', 'predict # of unsafe'])
for dir_name in res_map:
    csv_writer.writerow([dir_name, '"'+str(res_map[dir_name][0]) + '/' + str(res_map[dir_name][1])+'"', res_map[dir_name][2], res_map[dir_name][3]])
csv_file.close()
ground_truth_csv.close()
