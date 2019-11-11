class NflFeatureEng:
    """A Feature Engineer for the NFL data
    
    This class implements a feature engineer that cleans and engineers 
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
    """
    
    def __init__(self, data, exclude = []):
        self.data = data
        self.exclude = exclude
        self.include = ['WindSpeed', 
                        'GameWeather', 
                        'FieldEqPossession', 
                        'isRusher', 
                        'TimeHandoff', 
                        'TimeSnap', 
                        'HandSnapDiff', 
                        'BMI', 
                        'DefencePersonnel', 
                        'OffencePersonnel', 
                        'GameClock', 
                        'PlayerAge']
    
    def windSpeed(self, x):
        x = str(x) # convert all values to string
        x = x.lower() # convert all upper case to lowercase
        if '-' in x:
            x = (int(x.split('-')[0]) + int(x.split('-')[1])) / 2
        elif ' gusts up to 25 ' in x:
            x = (int(x.split(' gusts up tp 25 ')))
        try: 
            return float(x)
        except:
            return -1
        
    def gameWeather(self, x):
        x = str(x).lower()
        if 'sunny' in x or 'clear' in x or 'fair' in x:
            return 'sunny'
        elif 'cloud' in x or 'coudy' in x or 'clouidy' in x or 'hazy' in x or 'sun & clouds' in x or 'overcast' in x:
            return 'cloudy'
        elif 'rain' in x or 'shower' in x or 'rainy' in x:
            return 'rainy'
        elif 'controlled climate' in x or 'indoor' in x:
            return 'indoors'
        elif 'snow' in x:
            return 'snow'
        return None
    
    def fieldEqPossession(self):
        self.data['FieldEqPossession'] = self.data['FieldPosition'] == self.data['PossessionTeam']
        
    def isRusher(self):
        self.data['isRusher'] = self.data['NflId'] == self.data['NflIdRusher']
    
    def timeHandoff(self):
        self.data['TimeHandoff_min'] = pd.Series([int(x[-7:-5]) for x in self.data['TimeHandoff']])
        self.data['TimeHandoff_sec'] = pd.Series([int(x[-4:-2]) for x in self.data['TimeHandoff']])
        self.data['TimeHandoff'] = pd.Series([x[11:-1] for x in self.data['TimeHandoff']])
        
    def timeSnap(self):
        self.data['TimeSnap_min'] = pd.Series([int(x[-7:-5]) for x in self.data['TimeSnap']])
        self.data['TimeSnap_sec'] = pd.Series([int(x[-7:-5]) for x in self.data['TimeSnap']])
        self.data['TimeSnap'] = pd.Series([x[11:-1] for x in self.data['TimeSnap']])
    
    def handSnapDiff(self):
        self.data['HandSnapDiff_min'] = self.data['TimeHandoff_min'] - self.data['TimeSnap_min']
        self.data['handoff_snap_diff_sec'] = self.data['HandSnapDiff_min'] * 60 + self.data['TimeHandoff_sec'] - self.data['TimeSnap_sec']
    
    def BMI(self):
        self.data['height_1'] = pd.Series([int(x[0]) for x in self.data['PlayerHeight']])
        self.data['height_2'] = pd.Series([int(x[2]) for x in self.data['PlayerHeight']])
        self.data['height_3'] = self.data['height_1'] * 12 + self.data['height_2']
        self.data['BMI'] = (self.data['PlayerWeight'] * 703) / (self.data['height_1'] * 12 + self.data['height_2'] ** 2)
        
    def defencePersonnel(self):
        arr = [[int(s[0]) for s in t.split(', ')] for t in self.data['DefensePersonnel']]
        self.data['DL'] = pd.Series([int(a[0]) for a in arr])
        self.data['LB'] = pd.Series([int(a[1]) for a in arr])
        self.data['DB'] = pd.Series([int(a[2]) for a in arr])
    
    def offencePersonnel(self):
        arr = [[int(s[0]) for s in t.split(", ")] for t in self.data["OffensePersonnel"]]
        self.data["RB"] = pd.Series([int(a[0]) for a in arr])
        self.data["TE"] = pd.Series([int(a[1]) for a in arr])
        self.data["WR"] = pd.Series([int(a[2]) for a in arr])
    
    def gameClock(self):
        arr = [[int(s[0]) for s in t.split(":")] for t in self.data["GameClock"]]
        self.data["GameHour"] = pd.Series([int(a[0]) for a in arr])
        self.data["GameMinute"] = pd.Series([int(a[1]) for a in arr])
        
    def playerAge(self):
        self.data['Season'] = pd.Series([int(x) for x in self.data['Season']])
        self.data["BirthY"] = pd.Series([int(t.split('/')[2]) for t in self.data["PlayerBirthDate"]])
        self.data['age'] = self.data['Season'] - self.data['BirthY']
        
    def engineer(self):
        for c in self.include:
            
            if c in self.exclude: continue
                
            elif c == 'WindSpeed':
                self.data['WindSpeed'] = self.data['WindSpeed'].apply(lambda p: self.windSpeed(p))
            
            elif c == 'GameWeather':
                self.data['GameWeather'] = self.data['GameWeather'].apply(lambda p: self.gameWeather(p))

            elif c == 'FieldEqPossession':
                self.fieldEqPossession()
            
            elif c == 'isRusher':
                self.isRusher()
            
            elif c == 'TimeHandoff':
                self.timeHandoff()
            
            elif c == 'TimeSnap':
                self.timeSnap()
            
            elif c == 'HandSnapDiff':
                self.handSnapDiff()
            
            elif c == 'BMI':
                self.BMI()
            
            elif c == 'DefencePersonnel':
                self.defencePersonnel()
                
            elif c == 'OffencePersonnel':
                self.offencePersonnel()
                
            elif c == 'GameClock':
                self.gameClock()
                
            elif c == 'PlayerAge':
                self.playerAge()
        
        return self.data