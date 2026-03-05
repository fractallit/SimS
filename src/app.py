from flask import Flask, render_template, request, jsonify
import handler
import os
import requests as req

app = Flask(__name__)

OLLAMA_URL = os.getenv("OLLAMA_SERVER_URL", "http://localhost:11434")


@app.route('/get_ollama_tags', methods=['GET'])
def get_ollama_tags():
    response = req.get(f"{OLLAMA_URL}/api/tags").json()
    return jsonify(response)


@app.route('/summarize', methods=['POST'])
def summarize():
    content_source = request.form['content_source_tab']

    is_data_from_link = content_source == 'link'

    if not is_data_from_link:
        data = request.files['file_input']
    else:
        data = request.form['link_input']

    prompt = request.form['prompt']

    llm_model = request.form['select_llm_model']
    stt_model = request.form['select_stt_model']

    result = handler.work_with_data(is_data_from_link, data, prompt, llm_model, stt_model, OLLAMA_URL)

    return jsonify({'result': result})


@app.route('/')
def home():
    default_prompt = "Make summary of this video"

    return render_template('index.html', default_prompt=default_prompt)


if __name__ == '__main__':
    app.run(debug=True)

