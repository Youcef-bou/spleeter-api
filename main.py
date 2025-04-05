from flask import Flask, request, jsonify
import os
import uuid
from spleeter.separator import Separator

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return 'Spleeter API is running!'

@app.route('/separate', methods=['POST'])
def separate():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        # فصل إلى 4 مكونات: غناء، طبل، باس، وآلات أخرى
        separator = Separator('spleeter:4stems')
        output_path = os.path.join('output', filename.split('.')[0])
        separator.separate_to_file(filepath, 'output')

        return jsonify({
            'status': 'success',
            'output_folder': output_path
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
