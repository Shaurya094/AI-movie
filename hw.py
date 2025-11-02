import pandas as pd															
from textblob import TextBlob
from colorama import init, Fore
init(autoreset=True)

def load_data():
    df = pd.read_csv('imdb.csv')
    df['combo'] = df['Genre'].fillna('') + ' ' + df['Overview'].fillna('')
    return df

def mood_type(text):
    pol = TextBlob(text).sentiment.polarity
    mood = 'positive' if pol > 0 else 'negative' if pol < 0 else None
    emoji = '😊' if pol > 0 else '😞' if pol < 0 else '😐'
    print(Fore.CYAN + f"Your mood is {mood or 'neutral'} {emoji} (Polarity: {pol:.2f})")
    return mood

def recommend(df, genre=None, mood=None, rating=0):
    df = df[df['IMDB_Rating'] >= rating]
    if genre: df = df[df['Genre'].str.contains(genre, case=False, na=False)]
    recs = []
    for _, row in df.iterrows():
        p = TextBlob(row['Overview']).sentiment.polarity
        if (mood == 'positive' and p >= 0) or (mood == 'negative' and p < 0) or mood is None:
            recs.append((row['Series_Title'], p))
        if len(recs) == 5: break
    return recs

# Main
df = load_data()
name = input(Fore.YELLOW + "Your name: ")
genre = input(Fore.YELLOW + "Genre (or press Enter to skip): ")
mood = input(Fore.YELLOW + "How do you feel today? ")
rating = input(Fore.YELLOW + "Min IMDb rating (or Enter to skip): ")
rating = float(rating) if rating else 0
mtype = mood_type(mood)

print(Fore.MAGENTA + f"\n🎬 Top Picks for {name}:\n")
for i, (title, p) in enumerate(recommend(df, genre, mtype, rating), 1):
    emoji = '😊' if p > 0 else '😞' if p < 0 else '😐'
    print(Fore.CYAN + f"{i}. {title} (Polarity: {p:.2f}) {emoji}")
print(Fore.GREEN + f"\nEnjoy your movie picks, {name}! 🍿🎁")

