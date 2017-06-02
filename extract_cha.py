import sys
import random
import math
import csv

import pyclan as pc
import pandas as pd


def extract(path, percent=0.10):
    clan_file = pc.ClanFile(path)
    annotations = clan_file.annotations()
    len_all = len(annotations)
    clan_file.clear_annotations()

    non_chi = [x for x in annotations if x.speaker != "CHI"]
    n = int(math.ceil(len(non_chi) * percent))
    start = random.randint(0, len(annotations)-n)

    selected = non_chi[start:start+n+1]

    print "#annot: {}    #chi: {}    #non_chi: {}    #selected: {}\n".format(len_all, len_all-len(non_chi), len(non_chi), n)

    return clan_file, selected
    # return fill_blank_cha(clan_file, selected)


def insert_annot(line, annot, orig=False):
    tab_i = line.line.find("\t")
    if orig:
        blank_annot = annot.annot_string() + " "
    else:
        blank_annot = annot.annot_string(utt_type=False, present=False) + " "
    line.line = line.line[:tab_i+1] + blank_annot + line.line[tab_i+1:]


def fill_blank_cha(clan_file, annots):
    for annot in annots:
        line = clan_file.line_map[annot.line_num]
        insert_annot(line, annot)
    return clan_file, annots


def fill_orig_cha(clan_file, annots):
    for annot in annots:
        line = clan_file.line_map[annot.line_num]
        insert_annot(line, annot, orig=True)
    return clan_file, annots


def output_annot_csv(annots, path, with_codes=False):
    with open(path, "wb") as out:
        writer = csv.writer(out)
        if with_codes:
            writer.writerow(['word', 'utt_type', 'present', 'speaker', 'onset', 'offset'])
            x = [[a.word, a.utt_type, a.present, a.speaker, a.onset, a.offset] for a in annots]
            writer.writerows(x)
        else:
            writer.writerow(['word', 'onset', 'offset'])
            x = [[a.word, a.onset, a.offset] for a in annots]
            writer.writerows(x)

if __name__ == "__main__":

    coded_cha = sys.argv[1]

    new_clanfile, annots = extract(coded_cha)

    new_clanfile.write_to_cha("blank_rel_10.cha")
    output_annot_csv(annots, "output.csv")
