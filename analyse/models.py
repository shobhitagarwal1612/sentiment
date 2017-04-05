from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import unicode_literals

import collections
import json
import os
import os.path
import pickle

from django.db import models
from nltk.corpus import movie_reviews as reviews

from analyse.build import build_and_evaluate


class Amazon_Analyse(models.Model):
    def analyse_class(self):

        global emotion
        X = [reviews.raw(fileid) for fileid in reviews.fileids()]
        y = [reviews.categories(fileid)[0] for fileid in reviews.fileids()]

        filename = 'dump.pkl'

        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                model = pickle.load(f)
        else:
            model = build_and_evaluate(X, y, outpath=filename)

        # print(show_most_informative_features(model,'this is a nice day',n=50))
        # print(show_most_informative_features(model,'this is a worst day',n=50))

        path = os.getcwd()

        with open('amazon_data.json') as data_file:
            data = json.load(data_file)

        comments = [data["reviews"][i]["review_text"] for i in range(len(data["reviews"]))]
        ratings = [data["reviews"][i]["review_rating"] for i in range(len(data["reviews"]))]

        prediction = model.predict(comments)

        print(prediction)

        positive_review = []
        negative_review = []

        for i, emotion in enumerate(prediction):
            if emotion == 1:
                positive_review.append(i)
            else:
                negative_review.append(i)

        specs = ['camera', 'performance', 'battery', 'look', 'feel', 'money', 'sound', 'network', 'storage', 'software']

        save_path = path + '/analyse/data/'

        total_score = []
        data = []
        comments_list = collections.defaultdict(lambda: [])
        for spec in specs:
            spec_comments = []

            for i, comment in enumerate(comments):
                if spec in comment.split():
                    if i in positive_review:
                        emotion = 1
                    else:
                        emotion = 0

                    spec_comments.append([comment,
                                          ratings[i],
                                          emotion])
                    comments_list[spec].append((emotion, comment))
            comments_list[spec].sort()

            if len(spec_comments) > 0:
                sentiment_value = sum(i[2] for i in spec_comments) * 1.0 / len(spec_comments)
                sentiment_value = round(sentiment_value, 3) * 10

                total_score.append(sentiment_value)
                sentiment_value = round(sentiment_value, 3)
                print(spec, sentiment_value)
                data.append((spec, sentiment_value))

            completeFileName = os.path.join(save_path, spec + ".txt")

            with open(completeFileName, 'wb') as fp:
                pickle.dump(spec_comments, fp)

        net_score = round(sum(total_score) / len(total_score), 2)
        print("total score", net_score)

        return len(comments), net_score, data, comments_list

    def Amazon_spec(self, tokenn):

        path = os.getcwd()

        with open('amazon_data.json') as data_file:
            data = json.load(data_file)

        comments = [data["reviews"][i]["review_text"] for i in range(len(data["reviews"]))]
        ratings = [data["reviews"][i]["review_rating"] for i in range(len(data["reviews"]))]

        global emotion
        X = [reviews.raw(fileid) for fileid in reviews.fileids()]
        y = [reviews.categories(fileid)[0] for fileid in reviews.fileids()]

        filename = 'dump.pkl'

        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                model = pickle.load(f)
        else:
            model = build_and_evaluate(X, y, outpath=filename)

        prediction = model.predict(comments)

        specs = [tokenn]
        positive_review = []
        negative_review = []

        total_score = []
        data = []
        comments_list = collections.defaultdict(lambda: [])

        for i, emotion in enumerate(prediction):
            if emotion == 1:
                positive_review.append(i)
            else:
                negative_review.append(i)

        save_path = path + '/analyse/data/'
        for spec in specs:
            spec_comments = []

            for i, comment in enumerate(comments):
                if spec in comment.split():
                    if i in positive_review:
                        emotion = 1
                    else:
                        emotion = 0

                    spec_comments.append([comment,
                                          ratings[i],
                                          emotion])

                    comments_list[spec].append((comment, emotion))
            comments_list[spec].sort()

            if len(spec_comments) > 0:
                sentiment_value = sum(i[2] for i in spec_comments) * 1.0 / len(spec_comments)
                sentiment_value = round(sentiment_value, 3) * 10

                total_score.append(sentiment_value)
                sentiment_value = round(sentiment_value, 3)
                print(spec, sentiment_value)
                data.append((spec, sentiment_value))

            completeFileName = os.path.join(save_path, spec + ".txt")

            with open(completeFileName, 'wb') as fp:
                pickle.dump(spec_comments, fp)
        return data[0][1], comments_list
