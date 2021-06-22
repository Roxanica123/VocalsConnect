import json
import random
from random import sample
from os import walk

from predictions_system.feature_extraction.feature_function import FeatureFunction
from predictions_system.feature_extraction.used_feature_function import get_mel_spec
from predictions_system.prediction_system import PredictionSystem
from song_collection.database_connection import DatabaseConnection
from song_collection.spotify_uri_collector import SpotifyURICollector
from predictions_system.model.genres import genres as labels_mapping

if __name__ == '__main__':
    _dir_path, _dir_names, filenames = next(walk("./../../full songs"))
    samples = [filename.split(".")[0] for filename in filenames]

    # with open("./predictions_system/model/predictions", "r") as file:
    #     line = file.readline()
    #     while line:
    #         row = json.loads(line)
    #         filenames.append(row["filename"])
    #         line = file.readline()
    # filenames = [filename.split("_")[1] for filename in filenames]
    # filenames = list(set(filenames))
    # samples = ['5j7yurYTbYeQNXUYt7HMIh', '5XAaKR6aeWwG7ZDi37kWyZ', '1W0vl7sF9FIJye2HLWMkuG', '0sXvjZV7p4uvyPN4uQo3FH',
    #            '6OfTbviA1R1Exmf1oLjhT3', '4AsspdUMxLgji9Xl9ZWtJ6', '7pqhXViYrIK8Icpquar0fi', '5JwuHzmJCmHuHGjP9W6KtK',
    #            '33oBsOdKwm3bwMmlLYOZM4', '3t1hWG8EmCAIjMhEeEHoHj', '4OBEZpgbognrQ2I1OulYfu', '378ZUpNm2u2vsxNrTg5k7K',
    #            '4MOm00IOdFIuECOWfDhDoO', '4eLVBUT44CI83vOCO00RtW', '5BOsDwvahEezm6caqevGaR', '2fPlA2m2B0yecH8bVhUb1U',
    #            '3tdMuXpalBL7MEmeybOhpr', '4Im33JWLEobPtMTTAw7GUF', '717M9o5bZedADKa66AxqOg', '4QcYPg7jfKSnhiroHd51hC',
    #            '7Hay4E1OA8mOOukKBywusF', '5CFQcCHj09yfHqXeUJ7NAK', '7zRObPOHA0tWMYTAxLudmA', '72tAU6b10AgYfEFKrykp8J',
    #            '1XrZSqNIKJSLOgGqWikGC6', '6hrevxNtP5khJJjJ94DRz1', '5ddVuq7ud1LhazGXtxDbth', '0gdLTqxAY4DDUQxXzmwj1z',
    #            '63mjdS4drkgGHgUGJr7JYV', '5cMmtGotk1fEFpbaYrulZL', '1e8cnQVrv1vij7b2oDRUL1', '5qcWmwM2wZNLuBbBJDeI8d',
    #            '3Tb6RlqXPldaQVasxc68cP', '4T8YH4SJjLFwKeuUz8uVY7', '5F6rwEF15hN1jnhNk2YQHn', '2TAQ9YGehOKWDqDak5DuXc',
    #            '3el5n0AZ9NVCKi1rQfrxN6', '67HhfyfRBOnF2VELqBGmUG', '4ST3eFnbYuFMMlDJdgeqb7', '4eC8kxde5otdG8EyoMQXhG',
    #            '0jdny0dhgjUwoIp5GkqEaA', '1duotZCHiJkwZ6Ywx3xXVI', '7D5apefC8cTn93lIW60mHY', '7shx34SWmPiSw6QIPegmZB',
    #            '4hryAskv7zqhUIPDvF4N22', '0qbouIdcN4lrj49jem7TEz', '7Ljvi6JSrvNbfDhgSpUnvP', '4MIvorotwZEdzX9Rpy8nR6',
    #            '4cVWWg3mDfvIp8ZnxT0qfA', '0cMnwk12QE2GIvKEkgTfpF', '130dKZhza6XRe8WSBl1nsu', '7HFY3g2EuNTjZIk3Ooe0c5',
    #            '0J9VwZNdbi8lEyzzFyRvEE', '3LLS5a080K8drqinwbnHoT', '6UU25ijVOuDCFKvL0z5fyL', '6hpDd7qckQt4R8eUknR4rE',
    #            '4QbvsW2LSjNlpZSeMlOTI4', '2UKDqvTrKmFuT2OLuKK9Sp', '286xVza5jkTHO049lBwGtn', '2dYbi3CYZL2wp3CoQ9i1II',
    #            '5yoVSXmUC4a4jVcGuhzDev', '0DfouRnLomAdVvERdKuOkF', '7MEHTWzEi3z7P2jEWAcdHZ', '5sfLp8kRxeOxfMZI2s3W29',
    #            '3kvoYxCDpH4ZVPsFXQNlRc', '4l7lRKayuqTFT5tbYxQAZg', '1O9z6LLQPWuoiam2VwKh3x', '52d35Deejayu18L7EPCIjU',
    #            '4QaAvfxK0053pkYg16plDw', '3HMewTWHRtb7GY1hjG2kIw', '6XT9boebO9ntiDEbt0yPYh', '1SW3gUtT3xgDiypSrpHCHd',
    #            '7w7S6uEa6vO4xpvHeyA4wV', '61jwJO6zE0HeecQFZXLkNf', '318EGw5ZZB8U5MdMWQwxZQ', '5u4SWlDH9fATiXfMzV8fvD',
    #            '0t5zXzcJjRZMpBPAqkbjdW', '6eLLK01Jj06Pue3QAOtpWZ', '1BTXcdO8S1NrtGVIwGeuSw', '6oL0ib27diOV7aoNFTrVLq',
    #            '7APJGWX711cNV3BPeZodFN', '0NL4bgJMzs46bfUWg5tNcd', '5ChkMS8OtdzJeqyybCc9R5', '5nVMN88wJhC0uCVDzBHLru',
    #            '4nSCXiPMaXcQ79c6ahAiKv', '5GseQckHgP7uWyaiCd5ZW3', '5gdyrDO1ZYCKt9fx2hETYc', '3pmW6vR582UnUiH7BdXvRA',
    #            '1FoqENv4aSyGOtYwvgp7NG', '1xDOo45wHecFdLlDftyskk', '58HwS21miL7EmTcq3gpEYJ', '1j6Mdc3eML1f7FtQeRaW8J',
    #            '1PlsQaVfXOXPjx3XdUVSR3', '1iDK6TAwvcoGyEvr714xOw', '0ZBUoSnETToZmj90HmoPZO', '15EPc80XuFrb2LmOzGjuRg',
    #            '440qPj0wic2vJsfOTJ8b2E', '1pUrFkSi1ZN21538qCn3m8', '04lFaIg61J2gKoJa1Isk4L', '0Tys2Xz1d6GH4hSOdnYy68',
    #            '4KEYicVF0YsMFvUcCPaJyD', '49colNVoLFcMszng9O8w4h', '2hJWZvTw4QVBwC14ZNs1Ib', '6tBtLGv5vi39CEvKOqExYX',
    #            '3KVH8dkLQTKEsueo6ZhoBP', '5WbbuVzsAOunKbxOAt5m2b', '6twW4ma6w0mOeejejPK0nY', '4CfjFhJbL6GaTV3qBDO3jW',
    #            '6qIVsW535kQL85yVT8Cw7h', '1SgAraqPcfMwo1F3W9koEw', '1G9KctNOyAM8wMkCFhR3EZ', '2vNrk30RwEo2YExlmkoZmn',
    #            '3It1OL5RYsw68lLQJ986SH', '4LUNPeYGpcSyV2caXJBHH0', '5vsOTX7fKg0lObLeGX596w', '7wwifI9ROGvrmy2SDeLGhq',
    #            '4Cbl8pPeqone9olhLSzfgr', '12jeGtVC92AWtZP4bvTtFe', '5x2ET8r8R2gLdblpuB7uyF', '7K5bsDqIw6U6iASn0YN2wQ',
    #            '4z54rlBhOwB6NGJD1wgM7C', '4UBuBd6EkSFj8Y7o9nC0vz', '44yWVBdbAeNwGB5AWMsee1', '1NrhZWxjZef6PryMR9RLVP',
    #            '26AuyrZGzWWiYZPSd3XBIg', '23e29alilKhIYF88ifp7We', '3hXXaIOaXzw2Gd6pjzRd7b', '4um6ZMnib1I7VuG3c6jGm5',
    #            '6Jyleq8XY0cETDUzqvo5PU', '4fVDiH2VJR44CZ01mpr5Gu', '2wplW8iXXsklWeVaSHoNvX', '2jNA09bzVQOuNBAovxDR7f',
    #            '4VA95RMfqI85sx6hlzzToy', '1hrZkgqeMV45AzgGEw1NFE', '6Pe05uWRL9BfuGqF4ohOEz', '2WgxShhRLxD0QNTt3aEPIo',
    #            '0TqsqohsZgQ4LuWH2hHSfN', '24nv8Zg4zQz8yDwAORL6kQ', '1iH1OlDbKuhnqGRV9XsKPW', '0LvDivRKsoDDp7z8sAEWCe',
    #            '4Bs9NcSkWJ1uuV7lHnTXxd', '1WUt8SY17zIL49TxENehP5', '0dqXvhXUdiazbQ4JptjclJ', '4obajiv07fk15cJ9dQiFsy',
    #            '0ZoWRdF0aj5nigXXJZFrNb', '3y7JxyQzcfuMMTcvDSAjGk', '1vmYWShdyIhVDlEbArlBRC', '3dOAXUx7I1qnzWzxdnsyB8',
    #            '3KATY6VMXbu3u38J5YEbl3', '3u1dxH8Hqu8jQYzW06vRb6']
    connection = DatabaseConnection()
    urls = []
    albums = []
    genres = []
    new_samples = []
    for i in range(len(samples)):
        song = connection.get_song_by_id(samples[i])
        if song["genre"] != "kids":
            urls.append(song["preview_url"])
            albums.append(song["album_id"])
            genres.append(song["genre"])
            new_samples.append(samples[i])

    # SpotifyURICollector().download_songs("./temporary_uploads", urls, samples)
    samples = new_samples
    UPLOADS_PATH = '../temporary_uploads/'
    prediction_system = PredictionSystem(input_shape=(646, 128, 1), output_size=24,
                                         load_path_weights="./predictions_system/model/model_weights/model",
                                         out_folder=UPLOADS_PATH + "split",
                                         genres_mapping=labels_mapping,
                                         predictions_path="../predictions_system/model/predictions_without_kids",
                                         feature_function=FeatureFunction(get_mel_spec, {"add_dimension": True}, "mel",
                                                                          requires_to_list=False),
                                         seconds_per_segment=15,
                                         additional_segments_seconds_delay=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                                                                            14])

    paths = [UPLOADS_PATH + sample + ".mp3" for sample in samples]
    print(paths)
    with open("statistics_data_full_songs_without_kids_better", "w") as file:
        for i in range(len(samples)):
            print(i)
            print(samples[i])
            print(genres[i])
            try:
                prediction_result = prediction_system.predict(paths[i], samples[i] + ".mp3")
                print(prediction_result)
                json.dump({"song_id": samples[i], "prediction_result": prediction_result, "genre": genres[i],
                           "album_id": albums[i]}, file)
                file.write("\n")
            except Exception as e:
                print(e)

