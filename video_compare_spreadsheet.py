import os
import sys
import csv

import pandas as pd

import filegrouper as fg



def compare(orig, recode):
    df1 = pd.read_csv(orig)
    df2 = pd.read_csv(recode)

    if df1.shape[0] != df2.shape[0]:
        raise Exception("row count mismatch: \n\n{}:  {}\n{}:  {}".format(orig,
                                                                          df1.shape[0],
                                                                          recode,
                                                                          df2.shape[0]))
    else:
        ne = df1 != df2
        filename = os.path.basename(recode)
        ne['file'] = filename
        ne = ne.drop(
                 ["labeled_object.ordinal",
                  "labeled_object.onset",
                  "labeled_object.offset",
                  "labeled_object.object",
                  "labeled_object.speaker",
                  "labeled_object.id",
                  "basic_level"],
                  1
                )
        ne = ne.rename(index=str, columns={"labeled_object.utterance_type": "utt_type_mismatch",
                        "labeled_object.object_present": "obj_present_mismatch"})
        return ne


def compare2(orig, recode):
    if orig.shape[0] != recode.shape[0]:
        raise Exception("row count mismatch: \n\n{}:  {}\n{}:  {}".format(orig,
                                                                          orig.shape[0],
                                                                          recode,
                                                                          recode.shape[0]))
    else:
        ne = orig != recode
        return ne


def join(orig, recode):
    with open(orig, "rU") as orig_csv:
        with open(recode, "rU") as recode_csv:
            original = csv.reader(orig_csv)
            recoded = csv.reader(recode_csv)

            original.next()
            recoded.next()

            joined = []


            file_prefix = os.path.basename(orig)[:5]

            for line in original:
                reco_line = recoded.next()
                # new_line = []
                new_line = [file_prefix] + [line[7]] + line[0:6] + reco_line[4:6]
                # new_line.append(line == reco_line)
                joined.append(new_line)

    return joined




def output_joined(input_dir, joined):
    with open(input_dir+"/video_reliability_comparison.csv", "wb") as out:
        writer = csv.writer(out)
        writer.writerow(["file", "id", "ordinal", "onset", "offset", "word", "orig_utt_type", "orig_present", "new_utt_type", "new_present"])
        writer.writerows(joined)


if __name__ == "__main__":

    input_dir = sys.argv[1]
    print(input_dir)

    grouper = fg.FileGrouper(dir=input_dir,
                             types=[fg.video_orig_recode_csv,
                                    fg.video_recode_csv])

    final_ne = None
    final_joined = []

    for prefix, group in grouper.groups():
        print("prefix, ", prefix)
        print("video recode", group.video_recode_csv)
        print("video orig", group.orig_video_recode_csv)

        joined = join(group.orig_video_recode_csv,
                      group.video_recode_csv)

        final_joined += joined


    output_joined(input_dir, final_joined)
