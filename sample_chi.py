import sys
import random
import math
import csv

import pyclan as pc


def extract(path, percent=0.10):
    clan_file = pc.ClanFile(path)
    clan_file.flatten()
    clan_file.annotate()
    clan_file.assign_pho()
    annotations = clan_file.annotations()
    len_all = len(annotations)
    clan_file.clear_annotations()
    clan_file.delete_pho_comments()

    chi = [x for x in annotations if x.speaker == "CHI"]
    n = int(math.ceil(len(chi) * percent))
    start = random.randint(0, len(chi)-n)

    selected = chi[start:start+n]

    print "#annot: {}    #chi: {}    #non_chi: {}    #selected: {}\n".format(len_all, len(chi), len_all -len(chi), n)

    return clan_file, selected


def insert_annot(line, annot, orig=False):
    tab_i = line.line.find("\t")
    if orig:
        blank_annot = annot.annot_string() + " "
    else:
        blank_annot = annot.annot_string(utt_type=False, present=False) + " "
    line.line = line.line[:tab_i+1] + blank_annot + line.line[tab_i+1:]


def fill_blank_cha(clan_file, annots):
    # first empty out all the old annotations
    for line in clan_file.line_map:
        line.annotations = []

    # make a list of all the lines that have annotations on them
    annot_lines = set([x.line_num for x in annots])


    for annot in annots:
        line = clan_file.line_map[annot.line_num]
        line.annotations.append(annot)
        insert_annot(line, annot)

    lines = sorted(annot_lines, reverse=True)
    for line_num in lines:
        clan_line = clan_file.line_map[line_num]
        pho_string = "%pho:\t\r\n"
        clan_file.line_map.insert(line_num+1, pc.ClanLine(line_num, pho_string))

    return clan_file, annots


def fill_orig_cha(clan_file, annots):
    # for annot in annots:
    #     line = clan_file.line_map[annot.line_num]
    #     insert_annot(line, annot, orig=True)

    # first empty out all the old annotations
    for line in clan_file.line_map:
        line.annotations = []

    # make a list of all the lines that have annotations on them
    annot_lines = set([x.line_num for x in annots])


    for annot in annots:
        line = clan_file.line_map[annot.line_num]
        line.annotations.append(annot)
        insert_annot(line, annot, orig=True)

    lines = sorted(annot_lines, reverse=True)
    for line_num in lines:
        clan_line = clan_file.line_map[line_num]
        pho_string = "%pho:\t{}\r\n".format(" ".join([x.pho_annot for x in clan_line.annotations]))
        clan_file.line_map.insert(line_num+1, pc.ClanLine(line_num, pho_string))

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
    # output_annot_csv(annots, "output.csv")



    output_annot_csv(annots, "output_pho_withcodes.csv", with_codes=True)
