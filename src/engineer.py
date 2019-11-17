class FeatureEngine:
    """A Feature Engineer for the NFL data

    This class implements an engine that engineers
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
        self.data = data  # Clean data from the parser
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

    def engineerX(self):
        """
        Readjusts X
        """
        self.data['X'] = self.data.apply(
            lambda row: row['X'] if row['PlayDirection'] else 120-row['X'], axis=1)

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
        self.data['TimeDelta'] = self.data.apply(lambda row: (
            row['TimeHandoff'] - row['TimeSnap']).total_seconds(), axis=1)
        self.data = self.data.drop(['TimeHandoff', 'TimeSnap'], axis=1)

    def engineerYardsLeft(self):
        """
        Computes yards left from end-zone

        Note
        ----
        Requires variable HomeField (must execute engineerHomeField before execution)
        """
        self.data['YardsLeft'] = self.data.apply(
            lambda row: 100-row['YardLine'] if row['HomeField'] else row['YardLine'], axis=1)
        self.data['YardsLeft'] = self.data.apply(
            lambda row: row['YardsLeft'] if row['PlayDirection'] else 100-row['YardsLeft'], axis=1)
        self.data.drop(self.data.index[(self.data['YardsLeft'] < self.data['Yards']) | (
            self.data['YardsLeft']-100 > self.data['Yards'])], inplace=True)

    def engineerBMI(self):
        """
        Computes the BMI of a player from height and weight
        """
        self.data['PlayerBMI'] = 703 * \
            (self.data['PlayerWeight']/(self.data['PlayerHeight'])**2)

    def engineerPlayerAge(self):
        """
        Computes the age of the player from TimeHandoff
        """
        seconds_in_year = 60*60*24*365.25
        self.data['PlayerAge'] = self.data.apply(lambda row: (
            row['TimeHandoff']-row['PlayerBirthDate']).total_seconds()/seconds_in_year, axis=1)
        self.data = self.data.drop(['PlayerBirthDate'], axis=1)

    def engineerDefendersInTheBox_vs_Distance(self):
        dfInBox_mode = self.data['DefendersInTheBox'].mode()
        self.data['DefendersInTheBox'].fillna(
            dfInBox_mode.iloc[0], inplace=True)
        self.data['DefendersInTheBox_vs_Distance'] = self.data['DefendersInTheBox'] / \
            self.data['Distance']

    ### Outputs clean and engineered DataFrame ###

    def engineer(self):
        for c in self.include:

            if c in self.exclude:
                continue

            elif c == 'X':
                self.engineerX

            elif c == 'Orientation':
                self.data['Orientation'] = self.data.apply(lambda row: self.engineerOrientation(
                    row['Orientation'], row['PlayDirection']), axis=1)
                self.data['Dir'] = self.data.apply(lambda row: self.engineerOrientation(
                    row['Dir'], row['PlayDirection']), axis=1)

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
