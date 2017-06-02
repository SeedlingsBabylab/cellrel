import os
import sys

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


if __name__ == "__main__":

    input_dir = sys.argv[1]

    grouper = fg.FileGrouper(dir=input_dir,
                             types=[fg.orig_video_recode_csv,
                                    fg.video_recode_csv])

    final_ne = None

    for prefix, group in grouper.groups():
        print prefix
        print group.video_recode_csv
        print group.orig_video_recode_csv

        ne = compare(group.video_recode_csv,
                     group.orig_video_recode_csv)
        if final_ne is None:
            final_ne = ne
        else:
            final_ne = final_ne.append(ne, ignore_index=True)

        print ne.shape

    final_ne.to_csv("output.csv")
