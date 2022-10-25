#!/usr/bin/python3
"""
    This is the index page handler for Flask.
"""

from api.v1.views import app_views

@app_views.route('/')
def status():
    """
      Displays status
    """
    return {"status": "OK"}
