from flask import Flask
app = Flask(__name__) 

app.secret_key = 'your_secret_key' 

def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['original_url']

    # Validate the URL here if needed.

    short_url = generate_short_url()
    
    try:
        conn = sqlite3.connect('url_shortener.db')
        c = conn.cursor()
        c.execute("INSERT INTO urls (original_url, short_url) VALUES (?, ?)", (original_url, short_url))
        conn.commit()
        flash("URL has been shortened successfully.", 'success')
    except sqlite3.Error as e:
        flash("An error occurred while shortening the URL.", 'error')
        print(e)
    finally:
        conn.close()

    return redirect(url_for('index'))

@app.route('/<short_url>')
def redirect_to_original(short_url):
    conn = sqlite3.connect('url_shortener.db')
    c = conn.cursor()
    c.execute("SELECT original_url FROM urls WHERE short_url=?", (short_url,))
    result = c.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        flash("URL not found.", 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)