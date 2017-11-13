import pyclan as pc
import sys
import os
import csv


def extract_chi(clan_file):

    clan_file.annotate()
    annots = clan_file._flat_annotations()
    chis = [x for x in annots if x.speaker == "CHI"]
    chis.sort(key=lambda x: x.line_num)

    orig_phos = []

    for chi in chis:
        orig_phos.extend(find_phos(chi, clan_file))

    # get unique set of phos
    orig_phos = sorted(list(set(orig_phos)), key=lambda x: x.index)
    phos = []

    for pho in orig_phos:
        results = pho.content.translate(None, '\r\n').split()
        phos += results

    pairs = []
    if len(chis) != len(phos):
        raise Exception("\n\n\nmismatch in chi/pho count ({}):\nchis: {}\nphos: {}".format(clan_file.filename, chis, phos))
    else:
        pairs = zip(chis, phos)

    return pairs


def find_phos(annot, cf):
    init_tier = cf.line_map[annot.line_num].tier
    # curr_tier = cf.line_map[annot.line_num.tier]
    phos = []
    lines = cf.line_map[annot.line_num:]
    for line in lines:
        if line.is_tier_line and init_tier != line.tier:
            return phos
        elif line.line.startswith("%pho:"):
            phos.append(line)


def output_csv(annots, path):
    with open(path, "wb") as out:
        writer = csv.writer(out)
        writer.writerow(['file', "word", "orig_utt_type", "orig_present", "orig_pho", "recode_pho", "new_utt_type", "new_present", "onset", "offset"])
        writer.writerows(annots)


if __name__ == "__main__":

    orig_file = sys.argv[1]
    recode_file = sys.argv[2]

    orig_clan = pc.ClanFile(orig_file)
    orig_annots = extract_chi(orig_clan)

    recode_clan = pc.ClanFile(recode_file)
    recode_annots = extract_chi(recode_clan)

    key = os.path.basename(orig_file)[:5]

    if len(orig_annots) != len(recode_annots):
        raise Exception("\n\n\nannotation lengths do not match:\n\norig: {}\nrecode: {}\n\n".format(orig_annots, recode_annots))

    joined = zip(orig_annots, recode_annots)

    annots = []

    for pair in joined:
        old_entry = pair[0]
        new_entry = pair[1]
        annots.append([key, old_entry[0].word, old_entry[0].utt_type, old_entry[0].present, old_entry[1],
                       new_entry[1], new_entry[0].utt_type, new_entry[0].present,
                       old_entry[0].onset, old_entry[0].offset])


    output_csv(annots, "{}_audio_reliability_chi.csv".format(key))
