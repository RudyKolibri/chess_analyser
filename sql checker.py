import sqlite3

# Maak verbinding met je database
database = sqlite3.connect('chess_analyser.db')
cursor = database.cursor()

# Haal alle rijen op uit de tabel 'games'
cursor.execute("SELECT * FROM games")
alle_data = cursor.fetchall()

# Print elke rij netjes uit
i = 0
for rij in alle_data:
    print(rij)
    i+=1
print(i)
database.close()