from compare import *
import csv

class Group:
    def __init__(self, orig=None, recode=None):
        self.orig = orig
        self.recode = recode


def output_bl_csv(annots, path):
    with open(path, "wb") as out:
        writer = csv.writer(out)
        writer.writerow(["word", "onset", "offset", "utt_type", "present", "speaker", "annotid"])
        for x in annots:
            writer.writerow([x.word, x.onset, x.offset, x.utt_type, x.present, x.speaker, x.annotation_id])



if __name__ == "__main__":

    start_dir = sys.argv[1]

    blank_dir = os.path.join(start_dir, "reliability_checks")
    orign_dir = os.path.join(start_dir, "orig_10_percent")
    compare_csv_dir = os.path.join(start_dir, "debug", "compare_csvs")
    blank_files = [os.path.join(blank_dir, x) for x in os.listdir(blank_dir) if x.endswith(".cha")]
    orign_files = [os.path.join(orign_dir, x) for x in os.listdir(orign_dir) if x.endswith(".cha")]

    groups = {}
    for f in blank_files:
        key = os.path.basename(f)[:5]
        groups[key] = Group(recode=f)
    for f in orign_files:
        key = os.path.basename(f)[:5]
        groups[key].orig=f

    annots = []

    for key, group in groups.items():
        print key
        orig_clan = pc.ClanFile(group.orig)
        orig_annots = extract_annots(orig_clan)

        recode_clan = pc.ClanFile(group.recode)
        recode_annots = extract_annots(recode_clan)

        output_bl_csv(orig_annots, os.path.join(compare_csv_dir, "{}_orig.csv".format(key)))
        output_bl_csv(recode_annots, os.path.join(compare_csv_dir, "{}_recode.csv".format(key)))

        if len(orig_annots) != len(recode_annots):
            raise Exception("annotation lengths do not match: {}".format(key))

        joined = zip(orig_annots, recode_annots)

        for pair in joined:
            old_entry = pair[0]
            new_entry = pair[1]
            annots.append([key, old_entry.word, old_entry.utt_type, old_entry.present,
                           new_entry.utt_type, new_entry.present, old_entry.onset,
                           old_entry.offset])


    output_csv(annots, os.path.join(start_dir, "spreadsheets", "audio_reliability.csv"))

    print
