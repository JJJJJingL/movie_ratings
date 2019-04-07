import os
import argparse
import re

def get_filenames(folder_name):
    fis = []
    n = 0
    rootdir = os.walk(folder_name)
    for root, subdir, files in rootdir:
        for name in files:
            if name.endswith('.txt'):
                n += 1
                fis.append(os.path.join(root, name))
    return fis

def main(dialogues_folder):

    the_ending = r'(.*)(the)\b'
    files_name = get_filenames(dialogues_folder)
    #print(files_name)
    dialogue_text = []
    dialogue_name = []
    for dir in files_name:
        with open(dir, "r") as file:
            text = file.read()
            name = os.path.splitext(os.path.basename(dir))[0]
            name = name.split("_")[0]
            match_the = re.search(the_ending, name)
            if match_the is not None:
                name = re.sub(the_ending, r'\2\1', name)
            dialogue_name.append(name)
            dialogue_text.append(text)
    print(len(dialogue_text))
    #print(file_content[0])
    print(dialogue_name[0])

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--dialogues_file", type=str,
                        default="../imsdb_scenes_dialogs_nov_2015/dialogs",
                        help="wnut tsv file including annotations")

    args = parser.parse_args()

    main(args.dialogues_file)
