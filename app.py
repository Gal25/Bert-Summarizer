from flask import Flask, request, jsonify
import joblib


app = Flask(__name__)
model = joblib.load('finalized_model.sav')

@app.route('/')
def hello_world():
    return 'Summarization service'


@app.route('/summarize/ratio', methods=['POST'])
def sum_ratio():
    data = request.form
    ratio = data['ratio']
    text = data['text']
    sum_result = model(text, ratio=float(ratio))
    response = {'result: ': sum_result}
    return jsonify(response)


@app.route('/summarize/number', methods=['POST'])
def sum_number():
    data = request.form
    number = data['number']
    text = data['text']
    sum_result = model(text, num_sentences=int(number))
    response = {'result: ': sum_result}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=1313, host='0.0.0.0', threaded=True)