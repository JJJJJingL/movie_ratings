
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
# print(id_dict)

with open(id_to_attr, 'r') as attr:
    next(attr)
    for line in attr:
        fields = line.strip().split('\t')
        if fields[3] == 'US':
            if fields[0] in id_dict.keys(): # check if the rating exists
                title = fields[2].lower()
                title = "".join(title.split())
                id_dict[fields[0]].append(title) # append title

print(id_dict)

movie_name_list = '15minutes'
dialog_filename = '15minutes_dialog.txt'
scene_filename = f'{movie_name_list}_scene.txt'
dialog_list = []

dialog_file = f'/Users/ivywang/PycharmProjects/movie_final/dialogs/Action/{dialog_filename}'
scene_file = f'/Users/ivywang/PycharmProjects/movie_final/scenes/Action/{scene_filename}'


# extract the dialog in the file
with open(dialog_file, 'r') as dialog_file:
    for line in dialog_file:
        dialog_list.append(line)
        dialog_list = [d for d in dialog_list if d is not '\n']
        # dialog_list = [d for d in sublist for sublist in dialog_list]
print(len(dialog_list))
for d in dialog_list[:5]:
    print(d)
