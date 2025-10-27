from app import app

class Config:
    DEBUG = True
    SECRET_KEY = "4u8ot834vt4qtiwti5e0v9uyvmwayuvwa4uyna[ayuvw"

app.config.from_object(Config)

if __name__ == '__main__':
    app.run()