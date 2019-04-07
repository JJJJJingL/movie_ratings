import os
import argparse

def main(dialogues_foler):
    fis = []
    n = 0
    print(dialogues_foler)
    rootdir = os.walk(dialogues_foler)
    for root, subdir, files in rootdir:
        for name in files:
            if name.endswith('.txt'):
                n += 1
                fis.append(os.path.join(root, name))

    print(fis)
    print(len(fis))
    # for dir in os.path.listdir(main_dir):
    #     print(dir)
        # for file in os.path.listdir(dir):
        #     with open(os.path.join(dir, file), "r") as fd:
        #         file_content.append(fd.read)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--dialogues_file", type=str,
                        default="../imsdb_scenes_dialogs_nov_2015/dialogs",
                        help="wnut tsv file including annotations")

    args = parser.parse_args()

    main(args.dialogues_file)
