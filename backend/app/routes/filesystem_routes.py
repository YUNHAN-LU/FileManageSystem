from flask import Blueprint, request, jsonify, current_app
from app.services.filesystem_service import FileSystemService

filesystem_bp = Blueprint('filesystem', __name__, url_prefix='/filesystem')

@filesystem_bp.route('/upload', methods=['POST'])
def create_item():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    owner = request.form.get('owner')
    parent_id = int(request.form.get('parentId'))
    
    try:
        fs_service = FileSystemService(current_app.s3_manager)
        new_item = fs_service.create_file(file, owner, parent_id)
        
        return jsonify({
            'id': new_item.id,
            'name': new_item.name,
            'type': new_item.type,
            'parent_id': new_item.parent_id
        }), 201
    except NameError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@filesystem_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        fs_service = FileSystemService(current_app.s3_manager)
        fs_service.delete_item(item_id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@filesystem_bp.route('/<int:item_id>', methods=['GET'])
def list_items(item_id):
    fs_service = FileSystemService(current_app.s3_manager)
    current_name, current_id, parent_id, child_items = fs_service.list_items(item_id)
    return jsonify({"currentItem": {"name": current_name, "id": current_id, "parentId": parent_id}, "filesystem": child_items}), 200

@filesystem_bp.route('/<int:item_id>/file', methods=['GET'])
def get_item_file(item_id):
    fs_service = FileSystemService(current_app.s3_manager)
    return fs_service.get_item_file(item_id)

@filesystem_bp.route('/folder', methods=['POST'])
def create_folder():

    folder_name = request.form.get('name')
    parent_id = int(request.form.get('parentId'))
    try:
        fs_service = FileSystemService(current_app.s3_manager)
        new_item = fs_service.create_folder(folder_name, parent_id)
        return jsonify({
            'id': new_item.id,
            'name': new_item.name,
            'type': new_item.type,
            'parent_id': new_item.parent_id
        }), 201
    except NameError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 400