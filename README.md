# Covid Graph Gen

Python Scripts and MySQL schema to recreate the graphs used in my undergraduate thesis

These scripts interact with a database of the provided schema to fill out the database and output gexf files. These gexf files are snapshot graphs each representing a week of data. The size of the temporal snapshot can be editted. 

These scripts rely on data from Chen's COVID-19 dataset linked here. https://github.com/echen102/COVID-19-TweetIDs

Additionally, they depend on these linked Python libraries. 
Twarc: https://github.com/DocNow/twarc

Networkx: https://github.com/networkx
