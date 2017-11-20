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
                new_line = [file_prefix] + line[0:6] + reco_line[4:6]
                # new_line.append(line == reco_line)
                joined.append(new_line)

    return joined

def join_chi(orig, recode):
    with open(orig, "rU") as orig_csv:
        with open(recode, "rU") as recode_csv:
            original = csv.reader(orig_csv)
            recoded = csv.reader(recode_csv)

            original.next()
            recoded.next()

            orign = []
            for x in original:
                if x[9]:
                    x[9] = int(x[9])
                    orign.append(x)
            reco = []
            for x in recoded:
                if x[9]:
                    x[9] = int(x[9])
                    reco.append(x)

            orign.sort(key=lambda x: x[9])
            reco.sort(key=lambda x: x[9])
            joined = []

            file_prefix = os.path.basename(orig)[:5]

            if len(reco) != len(orign):
                raise Exception("\n\ncount mismatch: {}  ---- recode: {}  original: {}\n\n".format(file_prefix, len(reco), len(orign)))

            for idx, line in enumerate(orign):
                reco_line = reco[idx]
                if reco_line[9] != line[9]:
                    raise Exception("original_ordinal mismatch: \n\n{}\n{}".format(line, reco_line))
                # new_line = []
                new_line = [file_prefix] + [line[9]] + line[0:9] + reco_line[2:9]
                # new_line.append(line == reco_line)

                joined.append(new_line)

    return joined


def output_joined_chi(joined):
    with open("chi_cv_checks.csv", "wb") as out:
        writer = csv.writer(out)
        # "onset", "offset", "type", "ctype",
        # "voctype", "notes", "object", "cgprompt",
        # "cgresponse", "orig_ordinal"
        writer.writerow(["file", "orig_ordinal", "onset", "offset", "orig_type", "orig_ctype","orig_voctype", "orig_notes", "orig_object", "orig_cgprompt", "orig_cgresponse", "new_type", "new_ctype","new_voctype", "new_notes", "new_object", "new_cgprompt", "new_cgresponse"])
        writer.writerows(joined)



if __name__ == "__main__":

    input_dir = sys.argv[1]

    grouper = fg.FileGrouper(dir=input_dir,
                             types=[fg.video_orig_recode_csv,
                                    fg.video_recode_csv])

    final_ne = None
    final_joined = []

    for prefix, group in grouper.groups():
        print prefix
        print group.video_recode_csv
        print group.orig_video_recode_csv

        # joined = join(group.orig_video_recode_csv,
        #               group.video_recode_csv)
        joined = join_chi(group.orig_video_recode_csv,
                      group.video_recode_csv)

        final_joined += joined


    # output_joined(final_joined)
    output_joined_chi(final_joined)


