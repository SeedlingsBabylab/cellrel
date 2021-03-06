import os
import sys


def walk():
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith(".cha"):
                with open(os.path.join(root, file), "rb") as input:
                    with open(os.path.join(out_dir, file), "wb") as out:
                        for line in input:
                            if not line.startswith("%pho:"):
                                out.write(line)
                            else:
                                if "??? NOT A WORD" in line:
                                    line = line.replace("??? NOT A WORD", "???")
                                elif "NOT A WORD ???" in line:
                                    line = line.replace("NOT A WORD ???", "???")
                                elif "???NOT A WORD" in line:
                                    line = line.replace("???NOT A WORD", "???")
                                elif "??? can't hear" in line:
                                    line = line.replace("??? can't hear", "???")
                                elif "??? NOT HEARD" in line:
                                    line = line.replace("??? NOT HEARD", "???")
                                elif "NOT HEARD ???" in line:
                                    line = line.replace("NOT HEARD ???", "???")
                                elif "NOT A WORD???" in line:
                                    line = line.replace("NOT A WORD???", "???")
                                elif "??? Not Heard" in line:
                                    line = line.replace("??? Not Heard", "???")
                                elif "??? UNCLEAR" in line:
                                    line = line.replace("??? UNCLEAR", "???")
                                elif "??? Questionable" in line:
                                    line = line.replace("??? Questionable", "???")
                                elif "???" in line:
                                    print "file: {}\nline:\n{}\n\n".format(file, line)

                                content = " ".join(line.split('\t')[1:])
                                out.write("%pho:\t{}".format(content))



if __name__ == "__main__":

    start_dir = sys.argv[1]
    out_dir = sys.argv[2]

    walk()