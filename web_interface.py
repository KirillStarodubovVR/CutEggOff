from flask import Flask, render_template, request, send_file
import os
from ruaccent import RUAccent
import text_split

app = Flask(__name__)

ru_accent = RUAccent()
ru_accent.load()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        input_text = request.form['input_text']
        processed_text = ru_accent.process_all(input_text)

        # Create three text files with the same content

        file_name = 'accented_text.txt'
        with open(file_name, 'w', encoding="utf-8") as file:
            file.write(" ".join(processed_text[0]))

        file_name = 'omographs.txt'
        with open(file_name, 'w', encoding="utf-8") as file:
            file.write("\n".join(processed_text[1]))

        file_name = 'unknown.txt'
        with open(file_name, 'w', encoding="utf-8") as file:
            file.write("\n".join(processed_text[2]))


        return render_template('result.html')

@app.route('/download/<file_name>')
def download(file_name):
    file_name = f'{file_name}'
    return send_file(file_name, as_attachment=True, download_name=f'{file_name}')

if __name__ == '__main__':
    app.run(debug=True, port=5001)