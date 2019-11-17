def DataReshaper(data):
    """
    Takes the parsed and feature engineered data and outputs X_train and y_train
    vectors that are compatible for neural networks and machine learning algorithms

    Parameters:
    -----------
    data: parsed and feature engineered data (pandas dataframe format)

    Returns:
    --------
    X_train: a 2 dimentional vector housing all predictor variables
    y_train: a 1 dimentional vector housing all response variable

    Note:
    -----
    Requires 
    """
    
	data = data.sort_values(by=['PlayId', 'Team', 'isRusher', 'JerseyNumber'].reset_index()
	data.drop(['GameId', 'PlayId', 'index', 'isRusher', 'Team'], axis=1, inplace=True)

	self.drop_col = []
	for c in data.columns:
			if data[c].dtype == 'object':
					data.append(c)
	data.drop(drop_col, axis=1, inplace=True)
	print('The following columns were dropped:', drop_col)

	self.play_col = data.drop(players_col + ['Yards'], axis=1).columns

	X_play_col = np.zeros(shape=(X_train.shape[0], len(play_col)))
	for i, col in enumerate(play_col):
			X_play_col[:, i] = data[col][::22]

	X_train = np.concatenate([X_train, X_play_col], axis=1)
	y_train = data['Yards'][::22]

	scaler = StandardScaler()
	X_train = scaler.fit_transform(X_train)

	return X_train, y_train