from dao.billing_dao import BillingDAO
from models.billing import Billing
from typing import List, Optional
from datetime import datetime

class BillingService:
    @staticmethod
    def add_billing(billing: Billing) -> bool:
        # Business rule: Amount must be positive
        if billing.amount <= 0:
            raise ValueError("Billing amount must be positive.")

        # You can add additional validations here (e.g., valid patient, appointment IDs)

        return BillingDAO.insert_billing(billing)

    @staticmethod
    def update_billing(billing: Billing) -> bool:
        if billing.amount <= 0:
            raise ValueError("Billing amount must be positive.")

        return BillingDAO.update_billing(billing)

    @staticmethod
    def delete_billing(billing_id: int) -> bool:
        return BillingDAO.delete_billing(billing_id)

    @staticmethod
    def get_billing_by_id(billing_id: int) -> Optional[Billing]:
        return BillingDAO.get_billing_by_id(billing_id)

    @staticmethod
    def get_billings_by_patient(patient_id: int) -> List[Billing]:
        return BillingDAO.get_billings_by_patient(patient_id)

    @staticmethod
    def get_all_billings() -> List[Billing]:
        return BillingDAO.get_all_billings()

    @staticmethod
    def mark_billing_as_paid(billing: Billing) -> bool:
        billing.mark_as_paid()
        return BillingDAO.update_billing(billing)

    @staticmethod
    def get_overdue_billings() -> List[Billing]:
        all_billings = BillingDAO.get_all_billings()
        return [b for b in all_billings if b.is_overdue()]
