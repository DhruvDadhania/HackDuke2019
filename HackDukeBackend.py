from __future__ import print_function
import re
import string
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Sentiment:

    def __init__(self):
        self.positive = set(line.strip() for line in open('positive-words.txt'))
        self.negative = set(line.strip() for line in open('negative-words.txt'))

    def analyze_sentiment(self, instr):
        exclude = set(string.punctuation)
        instr = ''.join(ch for ch in instr if ch not in exclude)
        words = re.findall(r"\w+", instr)
        count = 0
        for word in words:
            word = string.lower(word)
            if word in self.positive:
                count = count + 1
            elif word in self.negative:
                count = count - 1
        if count > 0:
            return 1
        if count < 0:
            return -1
        return count


class Group:

    def __init__(self, groups, data, debug):
        self.debug = debug
        self.groups = groups

        def similarity(x, y):
            count = 0
            for i in range(len(x)):
                if x[i] != y[i]:
                    count = count + 1
            return count

        def aff(X):
            if self.debug:
                print(pairwise_distances(X, metric=similarity))
            return pairwise_distances(X, metric=similarity)

        self.labels = AgglomerativeClustering(n_clusters=groups, affinity=aff, linkage="single").fit(data).labels_

        if self.debug:
            print(self.labels)

    def get_labels(self):
        mapping = {}
        for group in range(self.groups):
            mapping[group] = []
        for i in range(len(self.labels)):
            mapping[self.labels[i]].append(i)

        result = []
        for elem in range(self.groups):
            result.append([])
        counter = 0;

        for key in mapping:
            for elem in mapping[key]:
                result[counter % self.groups].append(elem)
                counter = counter + 1

        if self.debug:
            print(result)

        return result


class Sheet:

    def __init__(self, spreadsheet_id, debug):
        self.debug = debug
        self.scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.spreadsheet_id = spreadsheet_id
        self.sample_range_num = 'Form Responses 1!A:YY'
        self.nameMap = {}

    def get_data(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scope)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                    range=self.sample_range_num).execute()
        values = result.get('values', [])
        sentim = Sentiment()
        for row in values:
            row.append(sentim.analyze_sentiment(row.pop(len(row) - 1)))

        ansMap = {}
        result = []
        counter = 0
        nameCounter = 0
        values = values[1:]
        for row in values:
            temp = []
            first = True
            second = True
            for elem in row:
                if first:
                    first = False
                    continue
                if second:
                    second = False
                    self.nameMap[nameCounter] = elem
                    nameCounter = nameCounter + 1
                    continue
                if elem in ansMap:
                    temp.append(ansMap[elem])
                else:
                    ansMap[elem] = counter
                    temp.append(counter)
                    counter = counter + 1
            result.append(temp)

        if self.debug:
            print(result)

        return result

    def get_namedict(self):
        return self.nameMap


def make_groups(spreadsheet_id, groups, debug=False):
    sheet = Sheet(spreadsheet_id, debug)
    group = Group(groups, sheet.get_data(), debug)
    labels = group.get_labels()
    nameDict = sheet.get_namedict()

    return [[nameDict[x] for x in team]for team in labels]


#print(make_groups('1PXfV_bU_JpD6ARuBLQaOERINxv30odhBveYeVgWFdBM', 2, True))
