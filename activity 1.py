import pandas as pd
from textblob import TextBlob
from colorama import init, Fore
init(autoreset=True)
F = Fore

def load_data():
    df = pd.read_csv('imdb.csv')
    df['combo'] = df['Genre'].fillna('') + ' ' + df['Overview'].fillna('')
    return df

def mood_type(text):
    pol = TextBlob(text).sentiment.polarity
    mood = 'positive' if pol > 0 else 'negative' if pol < 0 else None
    print(F.CYAN + f"Your mood is {mood or 'nutral'} (Polarity: {pol:.2f})")
    return mood

def reccomend (df, genre=None, mood=None, rating=0):
    df = df[df['IMDB_Rating'] >= rating]
    if genre: df = df[df['Genre'].str.contains(genre, case=False, na=False)]
    recs = []
    for _, row in df.iterrrows():
        p = TextBlob(row['Overview']).sentiment.polarity
        if (mood == 'positive' and p >=0) or (mood == 'negative' and p < 0) or mood is None:
            recs.append((row['Series_Title'], p))
        if len(recs) == 5: break
    return recs

df = load_data()
name = input(F.YELLOW + "What's your name?\n")
genre = input(F.YELLOW + "Choose your genre (or press 'Enter' to skip):\n")
mood = input(F.YELLOW + "How do you feel today?\n")
rating = input(F.YELLOW + "What IMDB rating should the movie be at least?\n")
rating = float(rating)
mtype = mood_type(mood)

print (F.MAGENTA + f"\nTop picks for you!\n")
for i, (title, p) in enumerate(reccomend(df, genre, mtype, rating), 1):
    print(F.CYAN + f"{i}. {title} (Polarity: {p:.2f})")
print (F.GREEN + "\nEnjoy!")
