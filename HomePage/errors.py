from werkzeug.exceptions import HTTPException
from flask import render_template

from HomePage import app

@app.errorhandler(Exception)
def all_exception_handler(e):
    if isinstance(e, HTTPException):
        print(e.code,e.description)
        return render_template('error.html', code=e.code, description=e.description)

    return render_template('error.html', code=500, description='Error')

