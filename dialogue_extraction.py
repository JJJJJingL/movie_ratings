import os
import argparse
import re
import pandas as pd

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
    dialogues = []
    the_ending = r'(.*)(the)\b'
    files_name = get_filenames(dialogues_folder)
    #print(files_name)
    dialogue_text = []
    dialogue_name = []
    dialogue_genre = []
    for dir in files_name:
        genre = dir.split('/')[-2]
        with open(dir, "r") as file:
            text = file.read()
            name = os.path.splitext(os.path.basename(dir))[0]
            name = name.split("_")[0]
            if name not in dialogue_name:
                match_the = re.search(the_ending, name)
                if match_the is not None:
                    name = re.sub(the_ending, r'\2\1', name)
                dialogue_genre.append(genre)
                dialogue_name.append(name)
                dialogue_text.append(text)
    script_frame = pd.DataFrame({'title': dialogue_name, 'genre': dialogue_genre, 'text': dialogue_text})
    print(script_frame.iloc[[1]])
    #print(len(dialogue_text))
    #print(file_content[0])
    #print(dialogue_name[10])

    k = 0
    movie_att_file = "movie_attributes.tsv"
    pd_list =[]
    with open(movie_att_file, "r") as movie_att:
        for line in movie_att:
            line = [field for field in line.strip().split('\t')]
            pd_list.append(line)
        print(pd_list[341298])
        imdb_frame = pd.DataFrame(pd_list)
        imdb_frame.columns = ['id','title','year', 'imdb_genre','rating','vote_num']
        imdb_frame['rating'] = pd.to_numeric(imdb_frame['rating'])
        print(imdb_frame)
        imdb_frame.groupby(['title'])['rating'].mean()
        #
        # new_frame = imdb_frame.groupby(['title'])['rating'].mean()
        # print(new_frame)
    data_frame = pd.merge(script_frame, imdb_frame)
    print(data_frame)

        # for line in movie_att:
        #     fields = line.strip().split('\t')
        #     movie_name = fields[1]
        #     movie_names.append(movie_name)
        #
        # for name in dialogue_name:
        #     if name in movie_names:
        #         match.append(name)
        #     else:
        #         k += 1
        #         #print(name)
        # print(f'{k} movies not found')

        #match = [name for name in dialogue_name if name in movie_names]
        #print(len(match))
        #print(match)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--dialogues_file", type=str,
                        default="../imsdb_scenes_dialogs_nov_2015/dialogs",
                        help="wnut tsv file including annotations")


    args = parser.parse_args()

    main(args.dialogues_file)
