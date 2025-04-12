from flask import Flask
from presentations.mutual_fund_controller import create_mutual_fund_bp
from presentations.nav_history_controller import create_nav_history_bp
from presentations.tax_controller import create_tax_bp
from presentations.transaction_controller import create_transaction_bp
from presentations.portfolio_controller import create_portfolio_bp
from presentations.user_controller import create_user_bp
from presentations.notification_controller import create_notification_bp
from presentations.goal_controller import create_goal_bp
from presentations.auth_controller import create_auth_bp
from containers import Container
from presentations.exception_handlers import register_error_handlers
from presentations.prediction_trend_funds_controller import create_prediction_trend_funds_bp
from presentations.performance_mutual_funds_controller import create_performance_mutual_funds_bp
from presentations.tax_2025_controller import create_tax_2025_bp
from presentations.deduction_controller import create_deduction_bp
from presentations.user_advise_controller import user_advise_bp

from flask_jwt_extended import JWTManager
from flask_talisman import Talisman
import dotenv
import os
dotenv.load_dotenv()

def create_app():
   app = Flask(__name__)

   Talisman(app, 
       force_https=False,  # Set to True in production
       session_cookie_secure=False,  # Set to True in production
       content_security_policy={
           'default-src': "'self'",
           'img-src': "'self' data:",
           'script-src': "'self'"
       }
   )
   container = Container()
   container.config.database_uri.from_env("MYSQL_URL")
   print(container.config.database_uri())
   
   perfprmance_mutual_funds_service = container.performance_mutual_funds_service()
   # Create blueprints with services
   mutual_fund_service = container.mutual_fund_service()
   mutual_fund_blueprint = create_mutual_fund_bp(mutual_fund_service)
   
   tax_service = container.tax_service()
   tax_blueprint = create_tax_bp(tax_service)
   
   transaction_service = container.transaction_service()
   transaction_blueprint = create_transaction_bp(transaction_service)

   portfolio_service = container.portfolio_service()
   portfolio_blueprint = create_portfolio_bp(portfolio_service)

   nav_history_service = container.nav_history_service()
   nav_history_blueprint = create_nav_history_bp(nav_history_service, perfprmance_mutual_funds_service, portfolio_service)

   user_service = container.user_service()
   user_blueprint = create_user_bp(user_service)

   notification_service = container.notification_service()
   notification_blueprint = create_notification_bp(notification_service)

   goal_service = container.goal_service()
   goal_blueprint = create_goal_bp(goal_service)

   auth_service = container.auth_service()
   auth_blueprint = create_auth_bp(auth_service)
   
   prediction_trend_funds_service = container.prediction_trend_funds_service()
   prediction_trend_funds_blueprint = create_prediction_trend_funds_bp(prediction_trend_funds_service)
   
   tax_2025_service = container.tax_2025_service()
   tax_2025_blueprint = create_tax_2025_bp(tax_2025_service)
   
   deduction_service = container.deduction_service()
   deduction_blueprint = create_deduction_bp(deduction_service)
   
   
   perfprmance_mutual_funds_blueprint = create_performance_mutual_funds_bp(perfprmance_mutual_funds_service)
   
   advise_service = container.advisor_service()
   user_advise_blueprint = user_advise_bp(advise_service,user_service)
   
   # Setup JWT
   app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
   jwt = JWTManager(app)

   # Register all blueprints
   app.register_blueprint(mutual_fund_blueprint)
   app.register_blueprint(nav_history_blueprint)
   app.register_blueprint(tax_blueprint)
   app.register_blueprint(transaction_blueprint)
   app.register_blueprint(portfolio_blueprint)
   app.register_blueprint(user_blueprint)
   app.register_blueprint(notification_blueprint)
   app.register_blueprint(goal_blueprint)
   app.register_blueprint(auth_blueprint)
   app.register_blueprint(prediction_trend_funds_blueprint)
   app.register_blueprint(perfprmance_mutual_funds_blueprint)
   app.register_blueprint(tax_2025_blueprint)
   app.register_blueprint(deduction_blueprint)
   app.register_blueprint(user_advise_blueprint)
   
   register_error_handlers(app)

   return app

if __name__ == "__main__":
   app = create_app()
   app.run(debug=True, host='0.0.0.0', port=5000)