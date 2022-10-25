#!/usr/bin/python3

from api.v1.views import app_views

@app_views.route('/')
def status():
    """
      Displays status
    """
    return {"status": "OK"}
