# import argparse
#
# parser = argparse.ArgumentParser()
# parser.add_argument("--", type=str,
#                         default="/Users/ivywang/PycharmProjects/emerging_entities_17/emerging.dev.conll",
#                         help="wnut tsv file including annotations")
# parser.add_argument("--output_file", type=str, default="my_predictions.tsv",
#                         help="file to write results")
#
# args = parser.parse_args()
from collections import defaultdict
id_dict = defaultdict(list)
id_to_rating = "/Users/ivywang/PycharmProjects/movie_final/title.ratings.tsv"
id_to_attr = '/Users/ivywang/PycharmProjects/movie_final/title.akas.tsv'
with open(id_to_rating, 'r') as rating:
    next(rating)
    for line in rating:
        fields = line.strip().split('\t')
        id_dict[fields[0]].append(fields[1])
        id_dict[fields[0]].append(fields[2])
print(id_dict)



movie_name_list = '15minutes'
dialog_filename = '15minutes_dialog.txt'
scene_filename = f'{movie_name_list}_scene.txt'
dialog_list = []

dialog_file = f'/Users/ivywang/PycharmProjects/movie_final/dialogs/Action/{dialog_filename}'
scene_file = f'/Users/ivywang/PycharmProjects/movie_final/scenes/Action/{scene_filename}'

with open(dialog_file, 'r') as dialog_file:
    for line in dialog_file:
        dialog_list.append(line)
        dialog_list = [d for d in dialog_list if d is not '\n']
        # dialog_list = [d for d in sublist for sublist in dialog_list]
print(len(dialog_list))
for d in dialog_list[:5]:
    print(d)
