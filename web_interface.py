from flask import Flask, render_template, request, send_file
import os
from ruaccent import RUAccent
import text_split

app = Flask(__name__)

ru_accent = RUAccent()
ru_accent.load()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    if request.method == "POST":
        input_text = request.form["input_text"]
        processed_text = ru_accent.process_all(input_text)

        # Create three text files with the same content

        file_name = "accented_text.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(" ".join(processed_text[0]))

        file_name = "omographs.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write("\n".join(processed_text[1]))

        file_name = "unknown.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write("\n".join(processed_text[2]))

        return render_template("result.html")


@app.route("/upload", methods=["POST"])
def upload():
    # Check if the POST request has a file part
    if "file" not in request.files:
        return "No file part"

    file = request.files["file"]

    # If the user submits an empty form
    if file.filename == "":
        return "No selected file"

    # Check if the file is a text file
    if file and file.filename.endswith(".txt"):
        # Save the uploaded file to the server (you might want to store it in a more secure way)
        file.save(file.filename)

        # Process the file content (replace this with your actual processing logic)
        with open(file.filename, "r", encoding="utf-8") as f:
            content = f.read()

        processed_text = ru_accent.process_all(content)

        # Create three text files with the same content

        file_name = "accented_text.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(" ".join(processed_text[0]))

        file_name = "omographs.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write("\n".join(processed_text[1]))

        file_name = "unknown.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write("\n".join(processed_text[2]))

        return render_template("result.html")

    else:
        return "Invalid file format. Please upload a text file."


@app.route("/download/<file_name>")
def download(file_name):
    file_name = f"{file_name}"
    return send_file(file_name, as_attachment=True, download_name=f"{file_name}")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
