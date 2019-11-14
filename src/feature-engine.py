import re
import pandas as pd
import numpy as np
from string import punctuation
import datetime


class NflFeatureEng:
    """A Feature Engineer for the NFL data

    This class implements a parser that cleans and engineers
    the variables of the NFL dataset for the 2019 NFL data competition held on Kaggle.

    Parameters
    ----------
    data: the nfl data in pandas DataFrame format

    exclude: A list of feature engineering processes to exclude

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

    def __init__(self, data, exclude=[]):
        self.data = data
        self.exclude = exclude  # Pass a list of processes to exclude
        self.include = ['X', 
                        'Orientation', 
                        'HomeField',
                        'FieldEqPossession', 
                        'isRusher', 
                        'PlayerAge',
                        'HandSnapDelta', 
                        'YardsLeft', 
                        'BMI',  
                        'DefendersInTheBox_vs_Distance']

    ### Cleaning functions ###

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

    def mapGameWeather(self, txt):
        """
        Creates the following map: indoor=>3, sunny=>2, cloudy=>1, rainy=>-2, snowy=>-3
        """
        ans = 1
        if pd.isna(txt):
            return 0
        if 'indoor' in txt:
            return ans*3
        if 'sunny' in txt or 'sunny' in txt:
            return ans*2
        if 'cloudy' in txt:
            return ans
        if 'rainy' in txt or 'rainy' in txt:
            return -2*ans
        if 'snowy' in txt:
            return -3*ans
        return 0

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

    def cleanHeight(self):
        """
        Parses the PlayerHeight column and converts height into inches
        """
        self.data['PlayerHeight'] = self.data['PlayerHeight'].apply(lambda x: 12*int(x.split('-')[0])+int(x.split('-')[1]))

    def cleanTimeHandoff(self):
        self.data['TimeHandoff'] = self.data['TimeHandoff'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ"))

    def cleanTimeSnap(self):
        self.data['TimeSnap'] = self.data['TimeSnap'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ"))

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

    def cleanPossessionTeam(self): # fixes problem in team name encoding
        map_abbr = {'ARI': 'ARZ', 'BAL': 'BLT', 'CLE': 'CLV', 'HOU': 'HST'}
        for abb in self.data['PossessionTeam'].unique():
            map_abbr[abb] = abb
        self.data['PossessionTeam'] = self.data['PossessionTeam'].map(map_abbr)
        self.data['HomeTeamAbbr'] = self.data['HomeTeamAbbr'].map(map_abbr)
        self.data['VisitorTeamAbbr'] = self.data['VisitorTeamAbbr'].map(map_abbr)

    def cleanPlayerBirthDate(self): 
        self.data['PlayerBirthDate'] = self.data['PlayerBirthDate'].apply(lambda x: datetime.datetime.strptime(x, "%m/%d/%Y"))

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

    def cleanWindDirection2(self, txt):
        if pd.isna(txt):
            return np.nan
        
        if txt=='n':
            return 0
        if txt=='nne' or txt=='nen':
            return 1/8
        if txt=='ne':
            return 2/8
        if txt=='ene' or txt=='nee':
            return 3/8
        if txt=='e':
            return 4/8
        if txt=='ese' or txt=='see':
            return 5/8
        if txt=='se':
            return 6/8
        if txt=='ses' or txt=='sse':
            return 7/8
        if txt=='s':
            return 8/8
        if txt=='ssw' or txt=='sws':
            return 9/8
        if txt=='sw':
            return 10/8
        if txt=='sww' or txt=='wsw':
            return 11/8
        if txt=='w':
            return 12/8
        if txt=='wnw' or txt=='nww':
            return 13/8
        if txt=='nw':
            return 14/8
        if txt=='nwn' or txt=='nnw':
            return 15/8
        return np.nan

    def cleanPlayDirection(self): 
        """
        1 if play direction if right, 0 if play direction is left.
        """
        self.data['PlayDirection'] = self.data['PlayDirection'].apply(lambda x: x.strip() == 'right')
    
    def cleanTeam(self):
        """
        1 if home team, 0 if away team
        """
        self.data['Team'] = self.data['Team'].apply(lambda x: x.strip()=='home')

   ### Engineering Functions ###

    def engineerX(self):
        """
        Readjusts X
        """ 
        self.data['X'] = self.data.apply(lambda row: row['X'] if row['PlayDirection'] else 120-row['X'], axis=1)

    def engineerOrientation(self, angle, play_direction):
        """
        Readjusts Orientation

        References
        ----------
        #from https://www.kaggle.com/scirpus/hybrid-gp-and-nn
        """
        if play_direction == 0:
            new_angle = 360.0 - angle
            if new_angle == 360.0:
                new_angle = 0.0
            return new_angle
        else:
            return angle

    def engineerFieldEqPossession(self):
        self.data['FieldEqPossession'] = self.data['FieldPosition'] == self.data['PossessionTeam']

    def engineerHomeField(self):
        self.data['HomeField'] = self.data['FieldPosition'] == self.data['HomeTeamAbbr']

    def engineerIsRusher(self):
        self.data['isRusher'] = self.data['NflId'] == self.data['NflIdRusher']
        self.data.drop(['NflId', 'NflIdRusher'], axis=1, inplace=True)

    def engineerHandoffSnapDelta(self):
        self.data['TimeDelta'] = self.data.apply(lambda row: (row['TimeHandoff'] - row['TimeSnap']).total_seconds(), axis=1)
        self.data = self.data.drop(['TimeHandoff', 'TimeSnap'], axis=1)

    def engineerYardsLeft(self):
        """
        Computes yards left from end-zone

        Note
        ----
        Requires variable HomeField (must execute engineerHomeField before execution)
        """
        self.data['YardsLeft'] = self.data.apply(lambda row: 100-row['YardLine'] if row['HomeField'] else row['YardLine'], axis=1)
        self.data['YardsLeft'] = self.data.apply(lambda row: row['YardsLeft'] if row['PlayDirection'] else 100-row['YardsLeft'], axis=1)
        self.data.drop(self.data.index[(self.data['YardsLeft']<self.data['Yards']) | (self.data['YardsLeft']-100>self.data['Yards'])], inplace=True)

    def engineerBMI(self):
        """
        Computes the BMI of a player from height and weight
        """
        self.data['PlayerBMI'] = 703*(self.data['PlayerWeight']/(self.data['PlayerHeight'])**2)

    def engineerPlayerAge(self):
        """
        Computes the age of the player from TimeHandoff
        """
        seconds_in_year = 60*60*24*365.25
        self.data['PlayerAge'] = self.data.apply(lambda row: (row['TimeHandoff']-row['PlayerBirthDate']).total_seconds()/seconds_in_year, axis=1)
        self.data = self.data.drop(['PlayerBirthDate'], axis=1)

    def engineerDefendersInTheBox_vs_Distance(self):
        dfInBox_mode = self.data['DefendersInTheBox'].mode()
        self.data['DefendersInTheBox'].fillna(
            dfInBox_mode.iloc[0], inplace=True)
        self.data['DefendersInTheBox_vs_Distance'] = self.data['DefendersInTheBox'] / \
            self.data['Distance']

    ### Outputs clean and engineered DataFrame ###

    def engineer(self):

        # Clean Data
        self.data['WindSpeed'] = self.data['WindSpeed'].apply(
            lambda p: self.cleanWindSpeed(p))
        self.data['GameWeather'] = self.data['GameWeather'].apply(
            lambda p: self.cleanGameWeather(p))
        self.data['GameWeather'] = self.data['GameWeather'].apply(self.mapGameWeather)
        self.data['StadiumType'] = self.data['StadiumType'].apply(
            self.cleanStadiumType)
        self.data['StadiumType'] = self.data['StadiumType'].apply(
            self.cleanStadiumType2)
        self.data['WindDirection'] = self.data['WindDirection'].apply(self.cleanWindDirection)
        self.data['WindDirection'] = self.data['WindDirection'].apply(self.cleanWindDirection2)
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

        for c in self.include:

            if c in self.exclude:
                continue

            elif c == 'X':
                self.engineerX

            elif c == 'Orientation':
                self.data['Orientation'] = self.data.apply(lambda row: self.engineerOrientation(row['Orientation'], row['PlayDirection']), axis=1)
                self.data['Dir'] = self.data.apply(lambda row: self.engineerOrientation(row['Dir'], row['PlayDirection']), axis=1)

            elif c == 'FieldEqPossession':
                self.engineerFieldEqPossession()

            elif c == 'HomeField':
                self.engineerHomeField()

            elif c == 'YardsLeft':
                self.engineerYardsLeft()

            elif c == 'isRusher':
                self.engineerIsRusher()

            elif c == 'PlayerAge':
                self.engineerPlayerAge()

            elif c == 'HandSnapDelta':
                self.engineerHandoffSnapDelta()

            elif c == 'BMI':
                self.engineerBMI()

            elif c == 'DefendersInTheBox_vs_Distance':
                self.engineerDefendersInTheBox_vs_Distance()

        return self.data

nfl = pd.read_csv('~/Downloads/UC Davis Exchange/dsc-data-bowl/data/train.csv')

engineer = NflFeatureEng(nfl)
engineer.engineer()