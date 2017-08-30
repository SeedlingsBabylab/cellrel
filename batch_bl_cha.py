import sys
import os
import pandas as pd
import filegrouper as fg
import extract_cha as extract
import pyclan as pc

import compare


def annot_to_df(annots):
    x = [[a.word, a.utt_type, a.present, a.speaker, a.onset, a.offset] for a in annots]
    df = pd.DataFrame(x, columns=['word', 'utt_type', 'present', 'speaker', 'onset', 'offset'])
    return df


if __name__ == "__main__":

    start = sys.argv[1]

    grouper = fg.FileGrouper(start, types=[
                                            fg.audio_blank_recode_cha,
                                            fg.audio_orig_recode_cha
                                          ])


    frames = []
    for prefix, group in grouper.groups():
        print "\n\n{}".format(prefix)

        new_clan_file = pc.ClanFile(group.audio_recode_cha)
        new_annots = annot_to_df(new_clan_file.annotations())

        orig_clan_file = pc.ClanFile(group.audio_orig_recode_cha)
        orig_annots = annot_to_df(orig_clan_file.annotations())

        df = pd.DataFrame(columns=["file","onset","offset","word","orig_utt_type","orig_present","new_utt_type","new_present"])
        df.file = pd.Series([prefix]*new_annots.shape[0])
        df.onset = new_annots.onset
        df.offset = new_annots.offset
        df.word = new_annots.word
        df.orig_utt_type = orig_annots.utt_type
        df.orig_present = orig_annots.present
        df.new_utt_type = new_annots.utt_type
        df.new_present = new_annots.present

        frames.append(df)

    bl = pd.concat(frames)

    bl.to_csv("audio_reliability.csv", index=False)

        # not_equal = compare.compare2(orig_annots, new_annots)
        # not_eekwal = not_equal.query('(utt_type == True) | (present == True)')



        #
        # mismatched = new_annots.iloc[not_eekwal.index]
        #
        # total_num += not_equal.shape[0]
        # mismatch_num += mismatched.shape[0]
        #
        # out_path = os.path.join(output, "{}_mismatches.csv".format(prefix))
        # mismatched.to_csv(out_path, index=False)
        #
        # print "total:     {}".format(total_num)
        # print "mismatch:  {}".format(mismatch_num)
        # print "% matched: {}".format(float(total_num-mismatch_num)/total_num)
        #

        # print (prefix)
