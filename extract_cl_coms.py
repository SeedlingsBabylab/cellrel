import csv
import os
import sys


if __name__ == "__main__":

    in_dir = sys.argv[1]

    for root, dirs, files in os.walk(in_dir):
        with open("output_cl_coms.csv", "wb") as out:
            writer = csv.writer(out)
            writer.writerow(["file", "labeled_object.ordinal", "labeled_object.onset", "labeled_object.offset",
                             "labeled_object.object","labeled_object.utterance_type","labeled_object.object_present",
                             "labeled_object.speaker","basic_level"])
            for file in files:
                if file.endswith(".csv"):
                    print file
                    with open(os.path.join(root, file), "rU") as filein:
                        reader = csv.reader(filein)
                        header = reader.next()
                        for row in reader:
                            if "???" in row[3]:
                                writer.writerow([file[0:5]] + row)
