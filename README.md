# Penalty Kicks Data Set from Transfermarkt
This repository contains a dataset of all players currently playing in a squad on Transfermarkt and their penalty kicks statistics

# Content
This dataset contains one player per row. I crawled all players on [Transfermarkt](http://www.transfermarkt.co.uk/) which are currently associated to a squad. Retired players are therefore not included (If someone knows a way how to find a list of all retired players on Transfermarkt (or any other page which included penalty kicks data, please tell me). 

# Example

`Premier League;4.11bn;Manchester City;40423;Keeper;Claudio Bravo;10;26`

| Column        | Name          | Description  |
| ------------- |--------------| -----|
| 1      | League name| League the player and the club compete in |
| 2      | Market value of league | Market value of the league as shown on Transermarkt in £ |
| 3      | Club name | Name of the club the player is currently competing for |
| 4      | Transfermarkt ID | Unique ID given by transfermarkt |
| 5      | Position | Position of the player (e.g. Keeper, Right Wing, Left Wing, Centre-Forward) |
| 6      | Player name | Name of the player |
| 7      | Penalty statistic 1 | Penalties saved for keepers, Penalties scored for all other players |
| 8      | Penalty statistic 2 | Penalties not saved for keepers, Penalties missed for all other players |


Further information:

* Market value: At the end of the number, there is either `bn` for billions, `m` for millions, or `k` for thousands. This column may be useful to filter or compare for player of higher or lower value leagues.

* Transfermarkt ID: For Ronaldo the Transfermarkt-URL is `http://www.transfermarkt.com/cristiano-ronaldo/profil/spieler/8198`. So the value of his ID (column 4) is `8198`. This may be useful for further scraping statistics of the player without having to find his URL again.

# Limitations

Please note, that the data (probably especially in lower tier leagues, that is leagues with lower market value) is not necessarily correct. It is certainly correctly scraped from Transermarkt, but I do not know about how accurate the data on Transfermarkt is. One example is Le Tissier: [On Transfermarkt](http://www.transfermarkt.com/matt-le-tissier/elfmetertore/spieler/43705) he is listed as having scored 27 penalties and missed 0. However, there are [UEFA reports](http://www.uefa.com/memberassociations/news/newsid=1913517.html) stating that he scored 48 out of 49 penalties. In this case the reason for this rather big deviation may just be, because Le Tissier has retired years ago and the data on Transfermarkt is better for recent players. Bottom line is, I am quite convinced this is one of the best data sources for penalty kicks out there. If you know another good data source, please let me know.

There is only one aggregate data point per player. In future (aka. *when I find time*), I would like to extend this data set to reflect the penalty statistics more granularly. For instance it would be interesting to get data about each penalty (when it was scored etc.). 

