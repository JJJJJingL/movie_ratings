import os
import argparse
import re
import pandas as pd
from collections import defaultdict
from nltk import sent_tokenize
import statistics
import numpy as np


def get_filenames(folder_name):
    """
    Args:
        folder_name (str): path of the folder that contains the dialogue files

    Yields:
        List[str]: list of paths for script files
    """
    fis = []
    n = 0
    rootdir = os.walk(folder_name)
    for root, subdir, files in rootdir:
        for name in files:
            if name.endswith('.txt'):
                n += 1
                fis.append(os.path.join(root, name))
    return fis

def get_script_frame(folder):
    """
    Args:
        folder (str): path of the folder that contains the dialogue files

    Yields:
        DataFrame: data frame of title, genre and text
    """
    the_ending = r'(.*)(the)\b'
    files_name = get_filenames(folder)
    dialogue_text = []
    dialogue_pathname = []
    dialogue_genre = []
    dialogue_name = []
    for dir in files_name:
        genre = dir.split('/')[-2]
        name = os.path.splitext(os.path.basename(dir))[0]
        name = name.split("_")[0]
        if name not in dialogue_pathname:
            dialogue_genre.append(genre)
            dialogue_pathname.append(name)
            with open(dir, "r") as file:
                text = file.read()
                dialogue_text.append(text)
        else:
            ind = dialogue_pathname.index(name)
            dialogue_genre[ind] += f' {genre}'

    for name in dialogue_pathname:
        match_the = re.search(the_ending, name)
        if match_the is not None:
            name = re.sub(the_ending, r'\2\1', name)
        dialogue_name.append(name)

    script_frame = pd.DataFrame({'title': dialogue_name, 'genre': dialogue_genre, 'text': dialogue_text})

    return script_frame

def get_data_frame(script_frame, movie_att_file):
    """
    Args:
        script_frame (str): data frame of title, genre and text
        movie_att_file (str): path of movie attributes file

    Yields:
        DataFrame: data frame of all attributes
    """
    pd_list =[]
    with open(movie_att_file, "r") as movie_att:
        for line in movie_att:
            line = [field for field in line.strip().split('\t')]
            pd_list.append(line)
        imdb_frame = pd.DataFrame(pd_list)
        imdb_frame.columns = ['id','title','year', 'imdb_genre','rating','vote_num']
        imdb_frame['rating'] = pd.to_numeric(imdb_frame['rating'])
        imdb_frame.groupby(['title'])['rating'].mean()
    nou_frame = imdb_frame.sort_values('vote_num', ascending=False).drop_duplicates(['title'])
    data_frame = pd.merge(script_frame, nou_frame)
    return data_frame

def output_data_frame(data_frame, script_file):
    """
    Args:
        data_frame (DataFrame): data frame of all attributes
        script_file (str): path of output file of script names, ratings and texts

    Yields:
        tsv: a tsv output file of script names, ratings and texts
    """
    with open(script_file, 'w') as out_script:
        rate_list = []
        for i, row in data_frame.iterrows():
            text = row['text']
            movie_name = row['title']
            rating = row['rating']
            rate_list.append(rating)
            text = re.sub(r'[A-Z]+\n', ' ', text)
            text = re.sub(r'--+', ' ', text)
            text = text.replace('\n',' ')
            text = text.replace('\t', ' ')
            out_script.write(f'{movie_name}\t{rating}\t{text}\n')


def output_movie_attributes(id_to_rating, id_to_attr, output_file):
    """
    Args:
        id_to_rating (str): path of tsv file containing ids and ratings
        id_to_attr (str): path of tsv file containing ids and their attributes
        output_file (str): path of output file of movie attributes

    Yields:
        tsv: a tsv output file of movie attributes
    """
    id_dict = defaultdict(list)
    # append those that: type is either short or movie, append title, append start/end year if there is any; append year
    # that is more than 1950; append genre, lowered. Title is also lowered and stripped of spaces
    with open(id_to_attr, 'r') as attr:
        next(attr)
        for line in attr:
            fields = line.strip().split('\t')
            if fields[1] == 'movie' or fields[1] == 'short':
                title = fields[2].lower()
                title = "".join(title.split())
                title = re.sub(r'[^\w\s]', '', title)
                id_dict[fields[0]].append(title) # append title
                # try to append year, if no year then do 0000
                if len(fields[5]) > 3:
                    year = int(fields[5])
                elif len(fields[6]) > 3:
                    year = int(fields[6])
                elif fields[5] == "\\N" and fields[6] == "\\N":
                    year = 1000
                id_dict[fields[0]].append(year)
                if fields[8] is not None:
                    id_dict[fields[0]].append(fields[8].lower()) # genre

    # append raitng and numVotes
    with open(id_to_rating, 'r') as rating:
        next(rating)
        for line in rating:
            r_fields = line.strip().split('\t')
            if r_fields[0] in id_dict.keys():
                id_dict[r_fields[0]].append(float(r_fields[1])) # rating
                id_dict[r_fields[0]].append(int(r_fields[2])) # number of votes

    # remove from the ones that do not have ratings
    for i, j in list(id_dict.items()):
        if len(j) < 4:
            del id_dict[i]
    with open(output_file, 'w') as output:
        for i, j in id_dict.items():
            output.write(i)
            output.write('\t')
            for attr in j:
                output.write(str(attr))
                output.write('\t')
            output.write('\n')

def main(dialogues_folder, id_to_rating_file, id_to_attr_file, movie_attr_output, data_frame_output):

    output_movie_attributes(id_to_rating_file, id_to_attr_file, movie_attr_output)
    script_frame = get_script_frame(dialogues_folder)
    data_frame = get_data_frame(script_frame, movie_attr_output)
    output_data_frame(data_frame, data_frame_output)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dialogues_file", type=str,
                        default="../imsdb_scenes_dialogs_nov_2015/dialogs",
                        help="wnut tsv file including annotations")
    parser.add_argument("-r", "--id_to_rating_file", type=str,
                        default="../title.ratings.tsv",
                        help="tsv file of id and rating")
    parser.add_argument("-a", "--id_to_attr_file", type=str,
                        default="../title.basics.tsv",
                        help="tsv file of id and attributes")
    parser.add_argument("-ao", "--attributes_output", type=str,
                        default="movie_attributes.tsv",
                        help="output file of all attributes")
    parser.add_argument("-dfo", "--data_frame_output", type=str,
                        default="script_file.txt",
                        help="output file of data frame")

    args = parser.parse_args()

    main(args.dialogues_file, args.id_to_rating_file, args.id_to_attr_file,
         args.attributes_output, args.data_frame_output)
