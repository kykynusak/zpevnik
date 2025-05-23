import sys
from flask import Flask, render_template, request, redirect, url_for
from db import get_connection  # používáme pouze tuto jedinou funkci pro DB připojení

app = Flask(__name__)

@app.route('/')
def home():
    print("Spouštím homepage", file=sys.stderr)
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, category, name FROM songs ORDER BY category, name;")
                rows = cur.fetchall()
                songs = {"verbunk": [], "vrtena": [], "lidovky": []}
                for row in rows:
                    song_id, category, name = row
                    if category in songs:
                        songs[category].append({"id": song_id, "name": name})
    except Exception as e:
        print("Chyba v DB dotazu:", e, file=sys.stderr)
        return "Chyba při připojení k databázi", 500

    return render_template('index.html', songs=songs)


@app.route('/song/<song_id>')
def song_detail(song_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, category, name, text FROM songs WHERE id = %s;", (song_id,))
            song = cur.fetchone()
    if not song:
        return "Song not found", 404
    return render_template('song_detail.html', song={
        "id": song[0],
        "category": song[1],
        "name": song[2],
        "text": song[3]
    })


@app.route('/add_song', methods=['POST'])
def add_song():
    category = request.form['category']
    song_name = request.form['song_name']
    song_text = request.form['song_text']
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO songs (id, category, name, text) VALUES (gen_random_uuid(), %s, %s, %s);",
                        (category, song_name, song_text))
            conn.commit()
    return redirect(url_for('home'))


@app.route('/delete_song/<song_id>', methods=['POST'])
def delete_song(song_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM songs WHERE id = %s;", (song_id,))
            conn.commit()
    return redirect(url_for('home'))


@app.route('/edit_song/<song_id>', methods=['GET', 'POST'])
def edit_song(song_id):
    if request.method == 'POST':
        name = request.form['song_name']
        text = request.form['song_text']
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE songs SET name = %s, text = %s WHERE id = %s;",
                            (name, text, song_id))
                conn.commit()
        return redirect(url_for('song_detail', song_id=song_id))
    else:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, category, name, text FROM songs WHERE id = %s;", (song_id,))
                song = cur.fetchone()
        if not song:
            return "Song not found", 404
        return render_template('edit_song.html', song={
            "id": song[0],
            "category": song[1],
            "name": song[2],
            "text": song[3]
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
