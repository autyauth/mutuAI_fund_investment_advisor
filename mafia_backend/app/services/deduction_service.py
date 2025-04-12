from adapters.models.deduction_model import DeductionModel
from adapters.repositories.deduction_repository import DeductionRepository
from adapters.repositories.deduction_2025_repository import Deduction2025Repository
from dto.deduction_dto import DeductionDTO
from dto.deduction_2025_dto import Deduction2025DTO

class DeductionService:
    def __init__(self, deduction_repository: DeductionRepository, deduction_2025_repository: Deduction2025Repository):
        self.deduction_repository = deduction_repository
        self.deduction_2025_repository = deduction_2025_repository

    def get_deduction(self, username: str, year: int):
        deduction = self.deduction_repository.get_deduction(username, year)
        if deduction is None:
            return None
        deduction = DeductionDTO.from_model(deduction)
        return deduction.to_dict() if deduction else None
    def get_deduct_2025(self, username: str, year: int):
        deduction = self.deduction_2025_repository.get_deduction(username, year)
        if deduction is None:
            return None
        deduction = Deduction2025DTO.from_model(deduction)
        return deduction.to_dict() if deduction else None
