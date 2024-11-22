import os
from dotenv import load_dotenv
from api import create_app, config

load_dotenv()

if __name__ == '__main__':
    app = create_app(config.Config)
    app.run(port=os.getenv('PORT', 5000))