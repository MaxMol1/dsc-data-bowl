## Few notes about positions:
Offense:
- RB is almost always the ballcarrier (if not always in this data)
- G, C, T, TE block defensive players so the RB can gain more yards. These are big meaty players
- QBs are not important, they do almost nothing on run plays
- WR blocks as well but are much lighter in weight than G, C, T, TE. They block on the outside (close to out of bounds line) so they won't matter unless the RB is going to their side.

# Variable descriptions
**GameId** - signifies the game the playId was in. GameId has multiple PlayIds.
**PlayId** - signifies what play the row was involved in.
**Team** - link a player to his team by using HomeTeamAbbr or VisitorTeamAbbr. Likely irrelevant because we can do this with position.
**X and Y** - not a huge indicator but combined with Dir can tell if a player is probably heading out of bounds
**S** - Speed. Faster ball carriers are more likely to pick up more yards, bigger outlier plays (70 yards instead of 5 because they can outrun others)
**A** - Acceleration. Same indicator as S
**Dis** - tells you almost nothing, it's the distance covered by a player in the last 0.1 seconds
**Orientation** - not very indicative, just which way the player is facing, not moving.
**Dir** - combine with S and A to tell where a player is going and how quickly they may get there. Definitely use this for RB to see where they are headed.
**NflId** - ID of the player. We could potentially use this data to indicate and store which players are better. We may want to consider doing this for RBs.
**DisplayName** - doesn't matter when we have NflId
**JerseyNumber** - doesn't matter
**Season** - doesn't matter
**YardLine** - combine with PossessionTeam and FieldPosition to indicate how many yards until the "end zone". For the first row in the data, YardLine = 35 and FieldPosition = NE indicates that we have 65 yards to go because NE is running the ball.
**Quarter** - doesn't matter a lot, but the tension is higher typically in a close game in the 4th quarter
**GameClock** - doesn't matter a lot. Can combine with score to indicate whether a team is trying to "run down the clock" or not.
**PossessionTeam** - combine with YardLine and FieldPosition. Also important to know which team is running the ball.
**Down** - combine with Distance. There are 4 downs in football. Teams usually run if there's a short distance, or can catch a defense off guard by running with a long distance.
**Distance** - combine with Down.
**FieldPosition** - combine with YardLine and FieldPosition.
**HomeScoreBeforePlay** - combine with VisitorScoreBeforePlay to make a scoredifference. Score difference can be indicative of how good a team is.
**VisitorScoreBeforePlay** - see HomeScoreBeforePlay
**NflIdRusher** - tells you who ran the ball. This is important.
**OffenseFormation** - doesn't really tell you much when you have OffensePersonnel to tell you who's on the field.
**OffensePersonnel** - break this into how many RB, TE, WR, OL were on field. If a position is not provided, you can guess it because there are 10 non-QBs on the field.
**DefendersInTheBox** - important, more defenders mean less likely to gain yards.
**DefensePersonnel** - more DL and LBs usually means more likely to stop the run, because those are bigger players closer to the ball.
**PlayDirection** - Can combine with player position data. Running to a side with more players on offense usually means more yards. Running to a side with less defenders also usually leads to more yards.
**TimeHandoff** - doesn't matter
**TimeSnap** - doesn't matter
**Yards** - very important. This is what we're basing our cdf around, we're calculating probability of yards.
**PlayerHeight** - Doesn't matter as much for RBs usually. Most typical RB height though is 5'10 to 6'1
**PlayerWeight** - Only matters for RBs usually. Heavier RBs (225 and up) are usually used for short yardage situations. Lighter players are typically faster and can make more "big yard" plays.
**PlayerBirthDate** - doesn't matter much, but older RBs are typically slower.
**PlayerCollegeName** - Where the player went to college. hard to use this and not that important anyway.
**Position** - can indicate what a player's height and weight roughly is. See notes above.
**HomeTeamAbbr** - use this with the score to indicate who's ahead.
**VisitorTeamAbbr** - use this with the score to indicate who's ahead.
**Week** - doesn't really matter. There are 17 weeks in a season
**Stadium** - doesn't matter.
**StadiumType** - GameWeather is irrelevant for an indoor stadium.
**Turf** - pretty irrelevant
**GameWeather** - not a huge indicator. Rainy might be slippery.
**Temperature, Humidity, WindSpeed, WindDirection** - all are pretty irrelevant

# Summary and Analysis of variables:

- **PlayId** groups plays together
- **S, A, X, Y, Dir** can be used to tell where a player is, how fast they're going, and what direction
- **NflId** identifies a player. We could potentially store RB data to identify which NflIds are most successful running
- **YardLine, PossessionTeam, and FieldPosition** should be combined into one variable that indicates how many yards until the end zone
- **Down** and **Distance** can be important, try to find a correlation with down&distance and yards gained.
- **PossessionTeam** is important because it identifies which team is running the ball.
- **HomeScoreBeforePlay, VisitorScoreBeforePlay, Home/AwayTeamAbbr, and PossessionTeam** should be combined to indicate what the score difference is for the running team.
- **NflIdRusher** is important, tells who's running the ball
- **OffensePersonnel** should be broken down into separate variables to indicate number of OL, TE, RB, WR. See above.
- **DefensePersonnel** should be broken down similar to OffensePersonnel
- **PlayDirection** is very important. That's which side the RB is going to.
- **Yards** is super important. See above.
- **PlayerHeight** and **PlayerWeight** really only matter for RBs. Position is sufficient for all other players because players in a certain position usually fall within a typical range.


- **Quarter** and **Gameclock** don't matter much, but later in games the stakes are higher.
- the only weather value that might cause an outlier are rainy/wet for an outdoor Stadium.

- All other variables are pretty irrelevant, based on my prior football knowledge.