import json

import librosa
from  librosa import display
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay

from predictions_system.model.genres import genres as labels_mapping

from song_collection.database_connection import DatabaseConnection


def load_data(path):
    ids = []
    predictions = []
    genres = []
    albums = []
    with open(path, "r") as file:
        line = file.readline()
        while line:
            row = json.loads(line)
            ids.append(row["song_id"])
            predictions.append(row["prediction_result"])
            genres.append(row["genre"])
            albums.append(row["album_id"])
            line = file.readline()
    return ids, predictions, genres, albums


def plot_albums(ids, predictions, albums):
    connection = DatabaseConnection()
    counts = {}
    for i in range(len(ids)):
        print(albums[i])
        similar = [connection.get_song_by_id(song.split("/")[-1])["album_id"] for song in
                   predictions[i]["similar_songs_ids"]]
        if similar.count(albums[i]) in counts:
            counts[similar.count(albums[i])] += 1
        else:
            counts[similar.count(albums[i])] = 1
    x = list(counts.keys())
    y = list(counts.values())

    fig = plt.figure(figsize=(10, 5))
    bar1 = plt.bar(x, y, color='maroon', width=0.4)
    for rect in bar1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

    plt.title("Number of songs from the same album")
    plt.show()
    plt.savefig("albums.png", dpi=200)


def plot_confusion_matrix(ids, predictions, genres):
    labels_mapping.append("others")
    mat = np.zeros((len(labels_mapping), len(labels_mapping)))
    for i in range(len(ids)):
        for genre in predictions[i]["genre_predictions"]:
            genres_predicted = genre.split(" - ")[0]
            percent = float(genre.split(" - ")[1].replace("%", "")) / 100
            mat[labels_mapping.index(genres[i])][labels_mapping.index(genres_predicted)] += percent
    disp = ConfusionMatrixDisplay(confusion_matrix=mat,
                                  display_labels=labels_mapping)
    ig, ax = plt.subplots()
    plt.rc('font', size="5")
    disp.plot(include_values=True,
              cmap='viridis', ax=ax, xticks_rotation=30)
    disp.ax_.set()
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right', fontsize="8")
    plt.savefig("confusion_full_songs_without_kids.png", dpi=200)


if __name__ == '__main__':
    # ids, predictions, genres, albums = load_data("statistics_data_without_kids")
    # # plot_albums(ids, predictions, albums)
    # for i in range(len(ids)):
    #     print(genres[i], predictions[i]["genre_predictions"])
    # plot_confusion_matrix(ids, predictions, genres)
    waveform, sr = librosa.load(r"D:\LICENTA\app\server\temporary_uploads\split\6Jyleq8XY0cETDUzqvo5PU\vocals.wav")
    fig, ax = plt.subplots(ncols=2, sharey=True)
    librosa.display.waveplot(waveform, sr=sr, ax=ax[0])
    ax[0].set(title='Vocals')
    ax[0].label_outer()
    waveform1, sr = librosa.load(r"D:\LICENTA\app\server\temporary_uploads\split\6Jyleq8XY0cETDUzqvo5PU\clean_vocals.wav")
    librosa.display.waveplot(waveform1, sr=sr, ax=ax[1])
    ax[1].set(title='Vocals without silence')
    ax[1].label_outer()
    plt.savefig("./cleaned_vocals.png", dpi=200)
