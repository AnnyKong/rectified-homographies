import cv2
import numpy as np

def run_ppl(pipeline, names, args, start_index=0, force_run = False):
    foreach(names, pipeline, num_threads = args.threads, debug = args.debug,
            start_index = start_index,
            index_list=None)

def compose(color_fn, disp_fn, out_fn):
    color = cv2.imread(color_fn)
    disp = cv2.imread(disp_fn)
    composed = np.hstack((color, disp))
    cv2.imwrite(out_fn, composed)

if __name__ == '__main__':
    import argparse
    import os
    from shutil import copyfile
    from os.path import join as pjoin
    import json
    import cv2
    from utils.pipeline.list_foreach import *
    from utils.pipeline.pipeline import *
    from utils.argparse_ext import coords_list
    import glob

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('names_list', help='names list')
    parser.add_argument('in_dir', help='input directory')
    parser.add_argument('out_dir', help='output directory')
    parser.add_argument('--start', type=int, help='start index', default=0)
    parser.add_argument('--end', type=int, help='end index', default=None)
    parser.add_argument('--threads', type=int, help='#threads', default=20)
    parser.add_argument('--debug', help='debug mode', default=False, action='store_true')

    args = parser.parse_args()


    with open(args.names_list, 'r') as f:
        names = json.load(f)
    names = sorted(names)

    end = len(names)-1 if args.end is None else args.end
    if args.start != 0 or args.end is not None:
        names = sorted(names)
        names = names[args.start:end+1]

    for i in range(len(names)):
        names[i] = str(int(names[i])).zfill(5) + ".jpg"

    ppl = [
            ParallelStep(copyfile,
                [pjoin(args.in_dir, kFormatKey, 'imL_(512,512).png'),
                 pjoin(args.in_dir, kFormatKey, 'imL_disp_(512,512).png')],
                [pjoin(args.out_dir, kFormatKey + 'imL_(512,512).png'),
                 pjoin(args.out_dir, kFormatKey + 'imL_disp_(512,512).png')],
            ),
    ]
    ppl = [
            Step(compose,
                {'color_fn': pjoin(args.in_dir, kFormatKey, 'imL_(512,512).png'),
                 'disp_fn': pjoin(args.in_dir, kFormatKey, 'imL_disp_(512,512).png')},
                {'out_fn': pjoin(args.out_dir, kFormatKey)},
            ),
    ]
    run_ppl(ppl, names, args)





