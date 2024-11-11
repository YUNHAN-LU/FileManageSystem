from app import db
from app.models.filesystem import FileSystem
import requests
class FileSystemService:
    def __init__(self, s3_manager):
        self.s3_manager = s3_manager

    def create_file(self, file, owner, parent_id):
        try:
            path = self.get_item_path(parent_id) if parent_id!=0 else ''
            path = path + file.filename

          

            # Create database record
            new_item = FileSystem(
                name=file.filename,
                type="file",
                parent_id=parent_id,
                disabled=False
            )


     
            existing_item = FileSystem.query.filter_by(name=file.filename, parent_id=parent_id).first()
            if existing_item:
                raise NameError("File already exists")
         
            db.session.add(new_item)
            db.session.commit()

              # Upload file to S3
            if not self.s3_manager.upload_file(file, path, file.content_type):
                raise Exception("Failed to upload file to S3")
            
            return new_item
        except Exception as e:
            db.session.rollback()
            raise e
        

    def get_item(self, item_id):
        return FileSystem.query.get_or_404(item_id)


    def delete_item(self, item_id):
        try:
            item = self.get_item(item_id)

            db.session.delete(item)
          
            path = self.get_item_path(item_id)[:-1]
         
            if item.type == 'folder':
                self.s3_manager.delete_folder(path)
            else:
                self.s3_manager.delete_file(path)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        

    def get_item_tree(self, item):
      
        return {
            'id': item.id,
            'name': item.name,
            'type': item.type,
            'children': [self.get_item_tree(child) for child in item.children]
        }
      

    def list_items(self):
        root_items = FileSystem.query.filter_by(parent_id=0).all()
        items = []
        for item in root_items:
            if item.disabled == False:
                items.append(self.get_item_tree(item))
        return items
    
    def get_item_path(self, item_id):
        if item_id == 0:
            return ''
        item = self.get_item(item_id)
        path =[item.name]
        while item.parent_id != 0:
            item = self.get_item(item.parent_id)
            path.append(item.name)

        path.reverse()
        path = '/'.join(path) +'/'
        return path

    def get_item_file(self, item_id):
        
        path =self.get_item_path(item_id)
        path = path[:-1]
        url = self.s3_manager.get_presigned_url(path)
        
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            return None

    def create_folder(self, name, parent_id):
        try:
            path = self.get_item_path(parent_id) if parent_id!=0 else ''
            

            new_item = FileSystem(
                name=name,
                type="folder",
                parent_id=parent_id,
                disabled=False
            )

            existing_item = FileSystem.query.filter_by(name=name, parent_id=parent_id).first()
            if existing_item:
                raise NameError("File already exists")
            

            db.session.add(new_item)
            db.session.commit()

            if not self.s3_manager.create_folder(path + name):
                raise Exception("Failed to create folder in S3")
        
            return new_item
        except Exception as e:
            db.session.rollback()
            raise e
