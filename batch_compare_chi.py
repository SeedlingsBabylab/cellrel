from compare_chi import *

class Group:
    def __init__(self, orig=None, recode=None):
        self.orig = orig
        self.recode = recode


if __name__ == "__main__":

    start_dir = sys.argv[1]

    blank_dir = os.path.join(start_dir, "reliability_checks")
    orign_dir = os.path.join(start_dir, "orig_10_percent")
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
        orig_annots = extract_chi(orig_clan)

        recode_clan = pc.ClanFile(group.recode)
        recode_annots = extract_chi(recode_clan)

        if len(orig_annots) != len(recode_annots):
            raise Exception("annotation lengths do not match: {}".format(key))

        joined = zip(orig_annots, recode_annots)

        for pair in joined:
            old_entry = pair[0]
            new_entry = pair[1]
            annots.append([key, old_entry[0].word, old_entry[0].utt_type, old_entry[0].present, old_entry[1],
                           new_entry[1], new_entry[0].utt_type, new_entry[0].present,
                           old_entry[0].onset, old_entry[0].offset])


    output_csv(annots, os.path.join(start_dir, "spreadsheets", "audio_reliability_chi.csv"))

    print