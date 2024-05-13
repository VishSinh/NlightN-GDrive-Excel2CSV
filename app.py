
from flask import Flask, request, jsonify

from utils import download_and_convert_to_csv, get_drive_folders, list_excel_files

app = Flask(__name__)


@app.route('/folders', methods=['GET'])
def get_folders():
    try:
        folders = get_drive_folders()
        return jsonify({'folders': folders})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  
    

@app.route('/files/convert', methods=['GET'])
def convert_excel_to_csv():
    folder_id = request.args.get('folder_id')
    try:
        files = list_excel_files(folder_id)
        csv_paths = [path for file in files for path in download_and_convert_to_csv(file['id'], file['name'])]
        return jsonify({'csv_paths': csv_paths, 'message': 'Files have been converted to CSV', 'total_files': len(csv_paths)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
