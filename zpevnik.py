import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Načte písničky z JSON souboru
def load_songs_from_file():
    global songs
    try:
        with open('songs.json', 'r', encoding='utf-8') as f:
            songs = json.load(f)  # Načte písničky podle kategorií
    except FileNotFoundError:
        # Pokud soubor neexistuje, použijeme výchozí hodnoty
        songs = {
            "verbunk": [],
            "vrtena": [],
            "lidovky": []
        }
        save_songs_to_file()  # Uloží výchozí hodnoty do souboru

# Uloží písničky do JSON souboru
def save_songs_to_file():
    with open('songs.json', 'w', encoding='utf-8') as f:
        json.dump(songs, f, ensure_ascii=False, indent=4)

@app.route('/song/<category>/<int:song_index>')
def song_detail(category, song_index):
    song = songs[category][song_index]
    return render_template('song_detail.html', song=song, category=category, song_index=song_index)

@app.route('/delete_song/<category>/<int:song_index>', methods=['POST'])
def delete_song(category, song_index):
    if category in songs and 0 <= song_index < len(songs[category]):
        del songs[category][song_index]
        save_songs_to_file()  # Uložení změn po smazání
    return redirect(url_for('home'))

@app.route('/edit_song/<category>/<int:song_index>', methods=['GET', 'POST'])
def edit_song(category, song_index):
    if request.method == 'POST':
        songs[category][song_index]['name'] = request.form['song_name']
        songs[category][song_index]['text'] = request.form['song_text']
        save_songs_to_file()  # Uložení změn po úpravě
        return redirect(url_for('song_detail', category=category, song_index=song_index))
    else:
        song = songs[category][song_index]
        return render_template('edit_song.html', song=song, category=category, song_index=song_index)

@app.route('/add_song', methods=['POST'])
def add_song():
    category = request.form['category']
    song_name = request.form['song_name']
    song_text = request.form['song_text']
    
    songs[category].append({"name": song_name, "text": song_text})  # Přidání písničky do kategorie
    
    save_songs_to_file()  # Uložení dat do souboru
    return redirect(url_for('home'))

@app.route('/')
def home():
    load_songs_from_file()  # Načte písničky při každém restartu aplikace
    return render_template('index.html', songs=songs)

if __name__ == '__main__':
    load_songs_from_file()  # Načte písničky při spuštění aplikace
    app.run(host='0.0.0.0', port=5000, debug=True)