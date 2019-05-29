""" flask app run """
from app_impl.routes import app

app.run(debug=True, host='0.0.0.0')
