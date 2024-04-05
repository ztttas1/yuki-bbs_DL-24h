from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# 公開したいディレクトリのパス
DIRECTORY_PATH = '/bbs'

@app.route('/files/<path:path>')
def serve_files(path):
    return send_from_directory(DIRECTORY_PATH, path)

@app.route('/')
def list_files():
    files = os.listdir(DIRECTORY_PATH)
    files_list = '<ul>'
    for file in files:
        files_list += f'<li><a href="/files/{file}">{file}</a></li>'
    files_list += '</ul>'
    return files_list

if __name__ == '__main__':
    app.run(debug=True)
