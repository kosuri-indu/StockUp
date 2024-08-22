import firebase_admin
from firebase_admin import credentials

# Path to your service account key file
cred = credentials.Certificate('"C:\Users\HP\OneDrive\Desktop\StockUp\stock-up-7292b-firebase-adminsdk-amvu2-671f84bd92.json"')
firebase_admin.initialize_app(cred)
