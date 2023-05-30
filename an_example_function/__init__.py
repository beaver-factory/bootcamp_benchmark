from .app import app_logic
import azure.functions as func


def main(myblob: func.InputStream):
    # code here, remove pass
    app_logic()
    pass
