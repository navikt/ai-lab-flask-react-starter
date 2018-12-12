import json
import sys
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from fastText import load_model
from app.S3.s3_connector import AWSS3Connector


STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__,static_folder="./static/build/static", template_folder="./static/build")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
model = None


def download_fasttext_model():
    s3_conn = AWSS3Connector(bucket_name='ai-lab')
    s3_conn.download_blob(blob_name='ai-lab-nace-poc/nace_model.bin', destination_path=f'{STATIC_PATH}/model.bin')


def load_fasttext_model():
    global model
    mf = f'{STATIC_PATH}/model.bin'
    try:
        model = load_model(mf)
    except IOError as e:
        print(f'I/O error {e.errno},{e.strerror}')
    except ValueError as e:
        print(f'Value error {e}')
    except:
        print(f'Unexpected error: {sys.exc_info()[0]}')
  

@app.route('/', methods=['GET', 'POST'])
def react():
    return render_template('index.html')


@app.route('/isReady', methods=['GET'])
def isReady():
    if model is not None:
        return "OK"


@app.route('/isAlive', methods=['GET'])
def isAlive():
    return "OK"


@app.route('/api', methods=['GET'])
def api():
    if 'q' in request.args:
        query = request.args['q']
        if not isinstance(query, str):
            return
        if len(query) < 3:
            return
    else:
        return

    if model is None:      
        load_fasttext_model()

    result = model.predict(query, k=5)
    ret = []
    for i, pred in enumerate(result[0]):
        ret.append({'nace':pred.replace('__label__','').replace('"',''),'value':str(result[1][i])})
    return json.dumps(ret)


if __name__ == '__main__':
    download_fasttext_model()
    load_fasttext_model()
    app.run(host='0.0.0.0', port=5400, debug=True)

