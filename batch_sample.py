import sample as extract
import os
import sys

import cPickle

def walk():
    for root, dirs, files in os.walk(full_files_dir):
        for file in files:
            if file.endswith(".cha"):
                print file
                clan_file, selected = extract.extract(os.path.join(root, file))
                clan_file_orig = cPickle.loads(cPickle.dumps(clan_file)) # cPickle is way faster than deepcopy....ugh

                new_clan, new_annots = extract.fill_blank_cha(clan_file, selected)
                orig_clan, orig_annots = extract.fill_orig_cha(clan_file_orig, selected)

                newname = file[:5]+ "_blank_rel_10"

                new_clan.write_to_cha(os.path.join(blank_out_dir, newname + ".cha"))
                orig_clan.write_to_cha(os.path.join(orig10_out_dir, newname + "_orig.cha"))

                # extract.output_annot_csv(new_annots, os.path.join(blank_csv_output, newname + ".csv"))
                # extract.output_annot_csv(annots, os.path.join(orig_csv_output, newname+"_orig" + ".csv"), with_codes=True)



if __name__ == "__main__":

    full_files_dir = sys.argv[1]

    blank_out_dir = os.path.join(os.path.dirname(full_files_dir), "reliability_checks")
    orig10_out_dir = os.path.join(os.path.dirname(full_files_dir), "orig_10_percent")

    walk()
