import pandas as pd
import datetime
import numpy as np
import re
from string import punctuation


class DataParser:
    """

    This class implements a parser that cleans the variables of the NFL dataset
    for the 2019 NFL data competition held on Kaggle.

    Parameters
    ----------
    data: the nfl data in pandas DataFrame format

    Notes
    -----
    Might not work if some of the columns have been edited since initial
    import. In that case, either implement additional feature engineering
    methods or reload the data.

    References
    ----------
    The methods were implemented based from the one found at:
    https://www.kaggle.com/prashantkikani/nfl-starter-lgb-feature-engg
    https://www.kaggle.com/bgmello/neural-networks-feature-engineering-for-the-win

    """

    def __init__(self, data):
        self.data = data

    def cleanWindSpeed(self, x):
        x = str(x)
        x = x.lower()
        if '-' in x:
            x = (int(x.split('-')[0]) + int(x.split('-')[1])) / 2
        elif ' gusts up to 25 ' in x:
            x = (int(x.split(' gusts up tp 25 ')))
        try:
            return float(x)
        except:
            return -1

    def cleanGameWeather(self, x):
        x = str(x).lower()
        if 'sunny' in x or 'clear' in x or 'fair' in x:
            return 'sunny'
        elif 'cloud' in x or 'coudy' in x or 'clouidy' in x or 'hazy' in x or 'sun & clouds' in x or 'overcast' in x:
            return 'cloudy'
        elif 'rain' in x or 'shower' in x or 'rainy' in x:
            return 'rainy'
        elif 'controlled climate' in x or 'indoor' in x:
            return 'indoor'
        elif 'snow' in x:
            return 'snowy'
        return None

    def mapGameWeather(self):
        gameWeatherMap = {}
        for w in self.data.GameWeather.dropna().unique():
            mean = self.data[self.data.GameWeather == w]['Yards'].mean()
            norm = (mean - self.data.Yards.mean()) / self.data.Yards.std()
            gameWeatherMap[w] = norm
        self.data['GameWeather'] = self.data['GameWeather'].map(gameWeatherMap)

    def cleanStadiumType(self, txt):  # Fixes the typo
        if pd.isna(txt):
            return np.nan
        txt = txt.lower()
        txt = ''.join([c for c in txt if c not in punctuation])
        txt = re.sub(' +', ' ', txt)
        txt = txt.strip()
        txt = txt.replace('outside', 'outdoor')
        txt = txt.replace('outdor', 'outdoor')
        txt = txt.replace('outddors', 'outdoor')
        txt = txt.replace('outdoors', 'outdoor')
        txt = txt.replace('oudoor', 'outdoor')
        txt = txt.replace('indoors', 'indoor')
        txt = txt.replace('ourdoor', 'outdoor')
        txt = txt.replace('retractable', 'rtr.')
        return txt

    # Focuses only on the words: outdoor, indoor, closed and open.
    def cleanStadiumType2(self, txt):
        if pd.isna(txt):
            return np.nan
        if 'outdoor' in txt or 'open' in txt:
            return 1
        if 'indoor' in txt or 'closed' in txt:
            return 0
        return np.nan

    def cleanDefencePersonnel(self):
        arr = [[int(s[0]) for s in t.split(', ')]
               for t in self.data['DefensePersonnel']]
        self.data['DL'] = pd.Series([int(a[0]) for a in arr])
        self.data['LB'] = pd.Series([int(a[1]) for a in arr])
        self.data['DB'] = pd.Series([int(a[2]) for a in arr])
        self.data = self.data.drop(labels=["DefensePersonnel"], axis=1)

    def cleanOffencePersonnel(self):
        arr = [[int(s[0]) for s in t.split(", ")]
               for t in self.data["OffensePersonnel"]]
        self.data["RB"] = pd.Series([int(a[0]) for a in arr])
        self.data["TE"] = pd.Series([int(a[1]) for a in arr])
        self.data["WR"] = pd.Series([int(a[2]) for a in arr])
        self.data = self.data.drop(labels=["OffensePersonnel"], axis=1)

    def cleanOffenseFormation(self):
        """
        This is a function for cleaning the Offense Formation column.
        It will find the mean Yards for and normalize it.
        """

        formationMap = {}
        for f in self.data.OffenseFormation.dropna().unique():
            mean = self.data[self.data.OffenseFormation == f]['Yards'].mean()
            norm = (mean - self.data.Yards.mean()) / self.data.Yards.std()
            formationMap[f] = norm
    
        self.data['OffenseFormation'] = self.data['OffenseFormation'].map(formationMap)

    def cleanHeight(self):
        """
        Parses the PlayerHeight column and converts height into inches
        """
        self.data['PlayerHeight'] = self.data['PlayerHeight'].apply(
            lambda x: 12*int(x.split('-')[0])+int(x.split('-')[1]))

    def cleanTimeHandoff(self):
        self.data['TimeHandoff'] = self.data['TimeHandoff'].apply(
            lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ"))

    def cleanTimeSnap(self):
        self.data['TimeSnap'] = self.data['TimeSnap'].apply(
            lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ"))

    def cleanGameClock(self):
        arr = [[int(s[0]) for s in t.split(":")]
               for t in self.data["GameClock"]]
        self.data["GameHour"] = [int(a[0]) for a in arr]
        self.data["GameMinute"] = [int(a[1]) for a in arr]
        self.data = self.data.drop(labels=['GameClock'], axis=1)

    def cleanTurf(self):
        # from https://www.kaggle.com/c/nfl-big-data-bowl-2020/discussion/112681#latest-649087
        Turf = {'Field Turf': 'Artificial', 'A-Turf Titan': 'Artificial', 'Grass': 'Natural', 'UBU Sports Speed S5-M': 'Artificial',
                'Artificial': 'Artificial', 'DD GrassMaster': 'Artificial', 'Natural Grass': 'Natural',
                'UBU Speed Series-S5-M': 'Artificial', 'FieldTurf': 'Artificial', 'FieldTurf 360': 'Artificial', 'Natural grass': 'Natural', 'grass': 'Natural',
                'Natural': 'Natural', 'Artifical': 'Artificial', 'FieldTurf360': 'Artificial', 'Naturall Grass': 'Natural', 'Field turf': 'Artificial',
                'SISGrass': 'Artificial', 'Twenty-Four/Seven Turf': 'Artificial', 'natural grass': 'Natural'}

        self.data['Turf'] = self.data['Turf'].map(Turf)
        self.data['Turf'] = self.data['Turf'] == 'Natural'

    def cleanPossessionTeam(self):  # fixes problem in team name encoding
        map_abbr = {'ARI': 'ARZ', 'BAL': 'BLT', 'CLE': 'CLV', 'HOU': 'HST'}
        for abb in self.data['PossessionTeam'].unique():
            map_abbr[abb] = abb
        self.data['PossessionTeam'] = self.data['PossessionTeam'].map(
            map_abbr)
        self.data['HomeTeamAbbr'] = self.data['HomeTeamAbbr'].map(map_abbr)
        self.data['VisitorTeamAbbr'] = self.data['VisitorTeamAbbr'].map(
            map_abbr)

    def cleanPlayerBirthDate(self):
        self.data['PlayerBirthDate'] = self.data['PlayerBirthDate'].apply(
            lambda x: datetime.datetime.strptime(x, "%m/%d/%Y"))

    def cleanWindDirection(self, txt):
        if pd.isna(txt):
            return np.nan
        txt = txt.lower()
        txt = ''.join([c for c in txt if c not in punctuation])
        txt = txt.replace('from', '')
        txt = txt.replace(' ', '')
        txt = txt.replace('north', 'n')
        txt = txt.replace('south', 's')
        txt = txt.replace('west', 'w')
        txt = txt.replace('east', 'e')
        return txt
    
    def mapWindDirection(self, txt):
        windDirectionMap = {
            'n': 0,'nne': 1/8,'nen': 1/8,'ne': 2/8,
            'ene': 3/8,'nee': 3/8,'e': 4/8,'ese': 5/8,
            'see': 5/8,'se': 6/8,'ses': 7/8,'sse': 7/8,
            's': 1,'ssw': 9/8,'sws': 9/8,'sw': 10/8,
            'sww': 11/8,'wsw': 11/8,'w': 12/8,'wnw': 13/8,
            'nw': 14/8,'nwn': 15/8,'nnw': 15/8
        }
        try:
            return windDirectionMap[txt]
        except:
            return np.nan

    def cleanPlayDirection(self):
        """
        1 if play direction if right, 0 if play direction is left.
        """
        self.data['PlayDirection'] = self.data['PlayDirection'].apply(
            lambda x: x.strip() == 'right')

    def cleanTeam(self):
        """
        1 if home team, 0 if away team
        """
        self.data['Team'] = self.data['Team'].apply(
            lambda x: x.strip() == 'home')

    def parse(self):
        self.data['WindSpeed'] = self.data['WindSpeed'].apply(self.cleanWindSpeed)
        self.data['GameWeather'] = self.data['GameWeather'].apply(self.cleanGameWeather)
        self.mapGameWeather()
        self.data['StadiumType'] = self.data['StadiumType'].apply(self.cleanStadiumType)
        self.data['StadiumType'] = self.data['StadiumType'].apply(self.cleanStadiumType2)
        self.data['WindDirection'] = self.data['WindDirection'].apply(self.cleanWindDirection)
        self.data['WindDirection'] = self.data['WindDirection'].apply(self.mapWindDirection)
        self.cleanOffencePersonnel()
        self.cleanDefencePersonnel()
        self.cleanHeight()
        self.cleanTimeHandoff()
        self.cleanTimeSnap()
        self.cleanTurf()
        self.cleanPossessionTeam()
        self.cleanPlayerBirthDate()
        self.cleanPlayDirection()
        self.cleanTeam()

        return self.data
