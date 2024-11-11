from app import db

class FileSystem(db.Model):
    __tablename__ = 'file_system'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('file_system.id', ondelete='CASCADE'))
    # disabled = db.Column(db.Boolean, default=False)
    children = db.relationship('FileSystem', 
                             backref=db.backref('parent', remote_side=[id]),
                             cascade='all, delete-orphan')
    disabled = db.Column(db.Boolean, default=False)