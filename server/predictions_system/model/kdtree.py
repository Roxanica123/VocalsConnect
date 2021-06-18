import json
import sklearn
from sklearn.utils import shuffle
from sortedcontainers import SortedSet


class KDTree:
    def __init__(self, number_of_neighbours_for_segment, number_of_neighbours, predictions_path):
        self.number_of_neighbours_for_segment = number_of_neighbours_for_segment
        self.predictions_path = predictions_path
        self.number_of_neighbours = number_of_neighbours
        self.filenames, self.predictions, self.genres_list = self.load_data()
        self.filenames, self.predictions = shuffle(self.filenames, self.predictions)
        self.tree = sklearn.neighbors.KDTree(self.predictions)

    def get_neighbours(self, predictions):
        distances, indexes_lists = self.tree.query(predictions, k=self.number_of_neighbours_for_segment)
        flat_distances = [item for sublist in distances for item in sublist]
        flat_indexes_lists = [item for sublist in indexes_lists for item in sublist]
        zipped = zip(flat_indexes_lists, flat_distances)
        zipped = sorted(zipped, key=lambda elem: elem[1])
        ids_lists = []
        for element in zipped:
            current_id = self.filenames[element[0]].split("_")[1]
            if current_id not in ids_lists:
                ids_lists.append(current_id)
            if len(ids_lists) == self.number_of_neighbours:
                break
        return list(ids_lists)

    def load_data(self):
        filenames = []
        predictions = []
        with open(self.predictions_path, "r") as file:
            line = file.readline()
            while line:
                row = json.loads(line)
                filenames.append(row["filename"])
                predictions.append(row["prediction"][0])
                line = file.readline()
        genres = sorted(list(set([filename.split("_")[0] for filename in filenames])))
        return filenames, predictions, genres
