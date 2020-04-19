# print("start up")

from app import app

# import os

# print("Mode: " + os.environ.get('MODE'))

# def load_config(mode=os.environ.get('MODE')):
#     """Load config."""
#     try:
#         if mode == 'PRODUCTION':
#             from .production import ProductionConfig
#             return ProductionConfig
#         elif mode == 'TESTING':
#             from .testing import TestingConfig
#             return TestingConfig
#         else:
#             from .development import DevelopmentConfig
#             return DevelopmentConfig
#     except ImportError:
#         from .default import Config
#         return Config

# if __name__ == '__main__':
#     # app.config['JSON_AS_ASCII'] = False
#     app.run(debug=True)