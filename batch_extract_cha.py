import extract_cha as extract
import os
import json
import sys
from copy import deepcopy

import cPickle

def walk():
    for root, dirs, files in os.walk(start):
        for file in files:
            print file
            clan_file, selected = extract.extract(os.path.join(root, file))
            clan_file_orig = cPickle.loads(cPickle.dumps(clan_file)) # cPickle is way faster than deepcopy....ugh

            new_clan, new_annots = extract.fill_blank_cha(clan_file, selected)
            orig_clan, orig_annots = extract.fill_orig_cha(clan_file_orig, selected)



            # new_clan, annots = extract.extract(os.path.join(root, file))
            newname = file[:5]+ "_blank_rel_10"



            new_clan.write_to_cha(os.path.join(blank_cha_out, newname + ".cha"))
            orig_clan.write_to_cha(os.path.join(orig_cha_out, newname + "_orig.cha"))




            # extract.output_annot_csv(new_annots, os.path.join(blank_csv_output, newname + ".csv"))
            # extract.output_annot_csv(annots, os.path.join(orig_csv_output, newname+"_orig" + ".csv"), with_codes=True)



if __name__ == "__main__":

    start = sys.argv[1]
    blank_cha_out = sys.argv[2]
    orig_cha_out = sys.argv[3]
    # blank_csv_output = sys.argv[4]

    walk()
