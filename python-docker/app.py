from flask import Flask
from flask import request
from flask import render_template
from werkzeug.utils import secure_filename
from flask import jsonify
from aes import AESCipher
from flask_cors import CORS
import logging
import shutil
import os
import datetime
import math


from utils import get_metadata
from utils import write_metadata_in_db

AESCipher = AESCipher("nivya secret key")


app = Flask(__name__)
CORS(app)


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/decryption')
def decrypt_data():
    return render_template('decrypt.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    file = request.files['file']
    file_last_modified_time = int(request.headers.get('lastModified')) / 1000
    filename = secure_filename(file.filename)
    file.save(filename)
    os.utime("./"+filename, (file_last_modified_time, file_last_modified_time))

    f = open("./"+filename, "r")
    plain_text = f.read()
    cipher_text = AESCipher.encrypt(plain_text)

    metadata = get_metadata("./"+filename)
    metadata['file_name'] = filename
    metadata['file_type'] = request.headers.get('fileType')
    write_metadata_in_db(metadata=metadata)

    f = open("./"+filename, "w")
    f.write(cipher_text.decode("utf-8"))
    f.close()

    shutil.copy('./'+filename, '/Volumes/NIVYA SHARED FOLDER/')

    return jsonify({"cipher_text": cipher_text.decode("utf-8")})


@app.route('/decrypt', methods=['POST'])
def decrypt():
    f = open("/Volumes/NIVYA SHARED FOLDER/nivya.txt", "r").read()
    cipher = request.form.get('decrypt').encode()
    decrypted_text = AESCipher.decrypt(cipher)
    decrypted_file = AESCipher.decrypt(f.encode())
    return render_template('decrypt_result.html', decrypted_text=decrypted_text, decrypted_file=decrypted_file)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port='5010', threaded=True, debug=True)
