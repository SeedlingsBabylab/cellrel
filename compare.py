import pyclan as pc
import sys
import os
import csv


def extract_annots(clan_file):

    # clan_file.flatten()
    clan_file.annotate()
    annots = clan_file._flat_annotations()

    return annots



def output_csv(annots, path):
    with open(path, "wb") as out:
        writer = csv.writer(out)
        writer.writerow(['file', "word", "orig_utt_type", "orig_present", "new_utt_type", "new_present", "onset", "offset"])
        writer.writerows(annots)


if __name__ == "__main__":

    orig_file = sys.argv[1]
    recode_file = sys.argv[2]

    orig_clan = pc.ClanFile(orig_file)
    orig_annots = extract_annots(orig_clan)

    recode_clan = pc.ClanFile(recode_file)
    recode_annots = extract_annots(recode_clan)

    key = os.path.basename(orig_file)[:5]

    if len(orig_annots) != len(recode_annots):
        raise Exception("\n\n\nannotation lengths do not match:\n\norig: {}\nrecode: {}\n\n".format(orig_annots, recode_annots))

    joined = zip(orig_annots, recode_annots)

    annots = []

    for pair in joined:
        old_entry = pair[0]
        new_entry = pair[1]
        annots.append([key, old_entry[0].word, old_entry[0].utt_type, old_entry[0].present,
                       new_entry[0].utt_type, new_entry[0].present, old_entry[0].onset,
                       old_entry[0].offset])


    output_csv(annots, "{}_audio_reliability_chi.csv".format(key))
