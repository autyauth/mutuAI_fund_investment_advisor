from flask import jsonify
from services.exceptions import BusinessLogicException, DatabaseException, NotFoundException,UserNotFoundException

def register_error_handlers(app):
    @app.errorhandler(BusinessLogicException)
    def handle_business_logic_exception(error):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(DatabaseException)
    def handle_database_exception(error):
        return jsonify({"error": str(error)}), 500

    @app.errorhandler(Exception)
    def handle_general_exception(error):
        return jsonify({"error": "An unexpected error occurred"}), 500
    
    @app.errorhandler(NotFoundException)
    def handle_not_found_exception(error):
        return jsonify({"error": str(error)}), 404
    @app.errorhandler(UserNotFoundException)
    def handle_user_not_found_exception(error):
        return jsonify({"error": str(error)}), 404