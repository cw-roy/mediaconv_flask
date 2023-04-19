#!/bin/python3.9
"""Initial POC for Flask front-end"""

import os

from flask import Flask, render_template, request

from pyffmpeg import FFmpeg

app = Flask(__name__, template_folder=".")


@app.route("/")
def index():
    """Sets up index.html"""
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    """Input file, output file, initiate conversion"""

    # check that a file was selected
    if 'file_input' not in request.files:
        return "No file selected"

    file_input = request.files["file_input"]
    file_output = request.form.get("file_output", "converted_video.mp4")
    file_output_path = request.form.get("file_output_path", "./")

    # check that the output file has a .mp4 extension
    if not file_output.lower().endswith(".mp4"):
        file_output += ".mp4"

    # save the input file to disk
    if file_input.filename != "":
        file_input.save(file_input.filename)

        # convert the video
        ff = FFmpeg()
        options_string = f'-i {file_input.filename} -q:v 0 {os.path.join(file_output_path, file_output)}'
        ff.options(options_string.split())

        message = f"File {file_input.filename} converted to {os.path.join(file_output_path, file_output)}"
        return render_template("result.html", message=message)
    else:
        return "No file selected"


if __name__ == "__main__":
    app.run()
