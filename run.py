import os, shutil, subprocess, time

if 'PDC_EVAL_DATA_PATH' in os.environ:
    data_path = os.environ['PDC_EVAL_DATA_PATH']
else:
    data_path = 'data'

results_path = 'results'
if not os.path.isdir(results_path):
    os.mkdir(results_path)


# Generated by 
# rng = random.Random(60127)
# (rng.randint(0, 30), rng.randint(0, 30))
pairs = [
    ('a05', 'a29'),
    ('a23', 'a18'),
    ('a13', 'a14'),
    ('a03', 'a10'),
    ('a27', 'a11'),
    ('a30', 'a19'),
    ('a06', 'a10'),
    ('a27', 'a03'),
    ('a15', 'a26'),
    ('a09', 'a15')
]

def image_path(id, scale_id):
    return os.path.join(data_path, 'resampled', '{}_{}.vtk'.format(id, scale_id))

def register(f, m, gpu, log):
    args = [
        'bin/deform',
        'registration',
        '-p', 'config.yml',
        '-f0', f,
        '-m0', m
    ]
    if gpu:
        args.append('--gpu')

    subprocess.check_call(args, stderr=log)

for gpu in [True, False]:
    print('GPU: {}'.format(gpu))
    for s in range(0, 5):
        print('scale: {}'.format(s))
        for p in pairs:
            print(p)
            f = image_path(p[0], s)
            m = image_path(p[1], s)

            log_file = os.path.join(results_path, '{}_{}_scale{}_gpu{}.txt'.format(p[0], p[1], s, 1 if gpu else 0))
            with open(log_file, 'w') as l:
                start = time.time()
                register(f, m, gpu, l)
                stop = time.time()
                l.write('\nTime elapsed: {}\n'.format(stop-start))



