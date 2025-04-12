from dependency_injector import containers, providers
from adapters.database.mysql_database import MysqlDatabase
from adapters.repositories.mutual_fund_repository import MutualFundRepository
from adapters.repositories.nav_history_repository import NavHistoryRepository
from adapters.repositories.tax_repository import TaxRepository
from adapters.repositories.transaction_repository import TransactionRepository
from adapters.repositories.portfolio_repository import PortfolioRepository
from adapters.repositories.user_repository import UserRepository
from adapters.repositories.notification_repository import NotificationRepository
from adapters.repositories.goal_repository import GoalRepository
from adapters.repositories.prediction_trend_funds_repository import PredictionTrendFundsRepository
from adapters.repositories.deduction_2025_repository import Deduction2025Repository
from adapters.repositories.deduction_repository import DeductionRepository
from adapters.repositories.performance_mutual_funds_repository import PerformanceMutualFundsRepository
from adapters.repositories.user_advise_repository import UserAdviseRepository
from adapters.repositories.tax_repository import TaxRepository
from adapters.repositories.goal_repository import GoalRepository
from adapters.repositories.deduction_2025_repository import Deduction2025Repository
from services.tax_2025_service import TaxDeduction2025Service

from services.mutual_fund_service import MutualFundService
from services.nav_history_service import NavHistoryService
from services.tax_service import TaxService
from services.transaction_service import TransactionService
from services.portfolio_service import PortfolioService
from services.user_service import UserService
from services.notification_service import NotificationService
from services.goal_service import GoalService
from services.auth_service import AuthService  
from services.prediction_trend_funds_service import PredictionTrendFundsService
from services.tax_2025_service import TaxDeduction2025Service
from services.deduction_service import DeductionService
from services.performance_mutual_funds_service import PerformanceMutualFundsService
from services.advisor_service import AdvisorService
class Container(containers.DeclarativeContainer):
    # Configurations
    config = providers.Configuration()
    
    # Database Dependency
    database = providers.Singleton(MysqlDatabase, uri=config.database_uri)
    
    # Repositories
    mutual_fund_repository = providers.Factory(
        MutualFundRepository, 
        database=database
    )
    
    nav_history_repository = providers.Factory(
        NavHistoryRepository,
        database=database
    )

    tax_repository = providers.Singleton(
        TaxRepository,
        database=database
    )

    transaction_repository = providers.Factory(
        TransactionRepository,
        database=database
    )

    portfolio_repository = providers.Factory(
        PortfolioRepository,
        database=database
    )

    user_repository = providers.Factory(
        UserRepository,
        database=database
    )

    notification_repository = providers.Factory(
        NotificationRepository,
        database=database
    )

    goal_repository = providers.Singleton(
        GoalRepository,
        database=database
    )
    
    prediction_trend_funds_repository = providers.Factory(
        PredictionTrendFundsRepository,
        database=database
    )
    deduction_2025_repository = providers.Factory(
       Deduction2025Repository,
       database=database
    )
    deduction_repository = providers.Factory(
        DeductionRepository,
        database=database
    )
    performance_mutual_funds_repository = providers.Factory(
        PerformanceMutualFundsRepository,
        database=database
    )
    user_advise_repository = providers.Factory(
        UserAdviseRepository,
        database=database
    )
    # Services
    mutual_fund_service = providers.Factory(
        MutualFundService, 
        mutual_fund_repository=mutual_fund_repository
    )
    
    nav_history_service = providers.Factory(
        NavHistoryService,
        nav_history_repository=nav_history_repository
    )

    tax_service = providers.Factory(
        TaxService,
        tax_repository=tax_repository
    )

    transaction_service = providers.Factory(
        TransactionService,
        transaction_repository=transaction_repository,
        nav_history_repository=nav_history_repository,
        portfolio_repository=portfolio_repository,
        user_repository=user_repository,
        goal_repository=goal_repository  # Added goal_repository
    )

    portfolio_service = providers.Factory(
        PortfolioService,
        portfolio_repository=portfolio_repository
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository
    )

    notification_service = providers.Factory(
        NotificationService,
        notification_repository=notification_repository
    )

    goal_service = providers.Factory(
        GoalService,
        goal_repository=goal_repository
    )

    auth_service = providers.Factory(
        AuthService,
        user_repository=user_repository
    )
    
    prediction_trend_funds_service = providers.Factory(
        PredictionTrendFundsService,
        prediction_trend_funds_repository=prediction_trend_funds_repository,
        transaction_repository=transaction_repository,
        goal_repository=goal_repository,
        user_repository=user_repository
    )
    
    tax_2025_service = providers.Singleton(
        TaxDeduction2025Service,  # Changed from TransactionService
        deduction_repository=deduction_2025_repository,
        tax_repository=tax_repository,
        goal_repository=goal_repository
    )
    
    deduction_service = providers.Factory(
        DeductionService,
        deduction_repository=deduction_repository,
        deduction_2025_repository=deduction_2025_repository
    )
    performance_mutual_funds_service = providers.Factory(
        PerformanceMutualFundsService,
        nav_history_repository=nav_history_repository,
        performance_mutual_funds_repository=performance_mutual_funds_repository,
        mutual_fund_repository=mutual_fund_repository,
        goal_repository=goal_repository
    )
    advisor_service = providers.Factory(
        AdvisorService,
        prediction_trend_funds_repository=prediction_trend_funds_repository,
        goal_repository=goal_repository,
        portfolio_repository=portfolio_repository,
        deduction_2025_repository=deduction_2025_repository,
        deduction_repository=deduction_repository
    )
    