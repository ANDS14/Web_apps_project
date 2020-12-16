from flask import Blueprint,render_template


error = Blueprint("errors", __name__)

@error.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@error.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403
