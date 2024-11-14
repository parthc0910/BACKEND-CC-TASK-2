from flask import Flask, request, jsonify

app = Flask(__name__)

def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(line.strip())
    return data

campus_mapping = {
    'P': 'Pilani',
    'G': 'Goa',
    'H': 'Hyderabad',
    'D': 'Dubai',
}

branch_mapping = {
    'A1': 'chemical',
    'A2': 'civil',
    'A3': 'eee',
    'A4': 'mechanical',
    'A5': 'bpharma',
    'A6': 'mba',
    'A7': 'cse',
    'A8': 'eni',
    'A9': 'biotech',
    'B1': 'bio_msc',
    'B2': 'chem_msc',
    'B3': 'eco',
    'B4': 'math',
    'B5': 'physics',
    'AA': 'ece',
    'AB': 'manufacturing'
}

ids_data = load_data('DOC-20241107-WA0013..txt')

@app.route('/')
def get_all_ids():
    format_type = request.args.get('format')
    
    if format_type == 'text':
        return "\n".join(ids_data), 200, {'Content-Type': 'text/plain'}
    
    return jsonify({"ids": ids_data})

@app.route('/filter')
def filter_ids():
    branch = request.args.get('branch')
    year = request.args.get('year')
    filtered_ids = ids_data
    
    if branch:
        filtered_ids = [
            id for id in ids_data if branch_mapping.get(id[4:6], '').lower() == branch.lower()
        ]
    
    if year:
        current_year = 2024
        target_year = current_year - int(year) + 1
        filtered_ids = [id for id in filtered_ids if id.startswith(str(target_year))]
    
    if not filtered_ids:
        return jsonify({"error": "No matching data found"}), 404
    
    return jsonify({"ids": filtered_ids})

@app.route('/<id>')
def get_id_details(id):
    for record in ids_data:
        if record.startswith(id):
            return jsonify({"id": {"year:": record[:4], "branch": branch_mapping.get(record[4:6], ''),"uid": record[6:8], "campus": campus_mapping.get(record[8], '')}})
    return jsonify({"error": "ID not found"}), 404

if __name__ == '__main__':
    app.run(port=8000)