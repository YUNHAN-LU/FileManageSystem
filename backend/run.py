# run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        from app import db
        db.create_all()
    app.run(host='0.0.0.0', port=1234, debug=True)