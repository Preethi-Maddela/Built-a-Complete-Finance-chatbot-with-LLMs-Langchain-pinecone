"""
calculators.py

Deterministic financial calculators for the Finance AI Chatbot.

These functions perform standard banking calculations (EMI, loan eligibility)
using fixed mathematical formulas and rule-based logic. They intentionally
do NOT use an LLM, RAG, or any AI component, because financial math must be
exact and reproducible every time - an LLM can occasionally make arithmetic
mistakes, while a formula never will.
"""

from typing import Optional


def calculate_emi(
    principal: float,
    annual_rate: float,
    tenure_years: int
) -> dict:
    """
    Calculate the EMI (Equated Monthly Installment) for a loan.

    Args:
        principal: The loan amount (e.g., 500000 for 5 lakh rupees).
        annual_rate: The yearly interest rate as a percentage (e.g., 8.5 for 8.5%).
        tenure_years: The loan duration in years (e.g., 5).

    Returns:
        A dictionary containing:
            - emi: the fixed monthly payment amount
            - total_payment: total amount paid over the full loan tenure
            - total_interest: total interest paid over the full loan tenure

    Raises:
        ValueError: if principal, annual_rate, or tenure_years is not positive.

    Example:
        >>> calculate_emi(500000, 8.5, 5)
        {'emi': 10258.29, 'total_payment': 615497.4, 'total_interest': 115497.4}
    """
    if principal <= 0:
        raise ValueError("Principal must be a positive number.")
    if annual_rate < 0:
        raise ValueError("Annual rate cannot be negative.")
    if tenure_years <= 0:
        raise ValueError("Tenure must be a positive number of years.")

    tenure_months = tenure_years * 12

    # Special case: a 0% interest loan is just principal divided evenly
    if annual_rate == 0:
        emi = principal / tenure_months
        total_payment = principal
        total_interest = 0.0
    else:
        monthly_rate = (annual_rate / 12) / 100  # convert yearly % to monthly decimal

        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / (
            (1 + monthly_rate) ** tenure_months - 1
        )
        total_payment = emi * tenure_months
        total_interest = total_payment - principal

    return {
        "emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
    }


def check_loan_eligibility(
    monthly_income: float,
    existing_emis: float,
    requested_loan_amount: float,
    tenure_years: int,
    annual_rate: float = 8.5,
    foir_limit: float = 0.50
) -> dict:
    """
    Check whether a person is likely eligible for a requested loan, based on
    the FOIR (Fixed Obligation to Income Ratio) rule commonly used by banks.

    Most banks cap total EMI obligations (existing + new) at 40-50% of a
    person's monthly income. This function uses that same principle.

    Args:
        monthly_income: The applicant's gross monthly income.
        existing_emis: Total of all EMIs the applicant is already paying.
        requested_loan_amount: The loan amount being applied for.
        tenure_years: Requested loan tenure in years.
        annual_rate: Interest rate to use for the eligibility calculation.
            Defaults to 8.5%, a typical personal/home loan rate.
        foir_limit: The maximum fraction of income allowed for total EMIs.
            Defaults to 0.50 (50%), a common conservative bank threshold.

    Returns:
        A dictionary containing:
            - eligible: True or False
            - reason: a human-readable explanation of the decision
            - requested_emi: the EMI that would apply to the requested loan
            - available_emi_capacity: how much EMI room the applicant has left

    Raises:
        ValueError: if monthly_income is not positive.

    Example:
        >>> check_loan_eligibility(50000, 5000, 1000000, 10)
        {'eligible': False, 'reason': '...', 'requested_emi': ..., 'available_emi_capacity': ...}
    """
    if monthly_income <= 0:
        raise ValueError("Monthly income must be a positive number.")
    if existing_emis < 0:
        raise ValueError("Existing EMIs cannot be negative.")

    max_allowed_emi = monthly_income * foir_limit
    available_emi_capacity = max_allowed_emi - existing_emis

    if available_emi_capacity <= 0:
        return {
            "eligible": False,
            "reason": (
                "Existing EMI obligations already meet or exceed the "
                f"recommended {int(foir_limit * 100)}% of monthly income limit."
            ),
            "requested_emi": None,
            "available_emi_capacity": round(available_emi_capacity, 2),
        }

    requested_emi = calculate_emi(requested_loan_amount, annual_rate, tenure_years)["emi"]

    if requested_emi <= available_emi_capacity:
        return {
            "eligible": True,
            "reason": "Requested loan's EMI is within the applicant's available EMI capacity.",
            "requested_emi": requested_emi,
            "available_emi_capacity": round(available_emi_capacity, 2),
        }
    else:
        return {
            "eligible": False,
            "reason": (
                f"Requested EMI (Rs. {requested_emi}) exceeds available "
                f"EMI capacity (Rs. {round(available_emi_capacity, 2)})."
            ),
            "requested_emi": requested_emi,
            "available_emi_capacity": round(available_emi_capacity, 2),
        }


def suggest_max_eligible_loan(
    monthly_income: float,
    existing_emis: float,
    tenure_years: int,
    annual_rate: float = 8.5,
    foir_limit: float = 0.50
) -> Optional[float]:
    """
    Estimate the maximum loan principal an applicant could be approved for,
    given their available EMI capacity, by working the EMI formula backwards.

    Args:
        monthly_income: The applicant's gross monthly income.
        existing_emis: Total of all EMIs the applicant is already paying.
        tenure_years: The loan tenure to calculate against.
        annual_rate: Interest rate to assume. Defaults to 8.5%.
        foir_limit: Maximum fraction of income allowed for total EMIs.

    Returns:
        The estimated maximum loan principal the applicant could take on,
        or None if the applicant has no remaining EMI capacity.
    """
    max_allowed_emi = monthly_income * foir_limit
    available_emi_capacity = max_allowed_emi - existing_emis

    if available_emi_capacity <= 0:
        return None

    tenure_months = tenure_years * 12
    monthly_rate = (annual_rate / 12) / 100

    if annual_rate == 0:
        max_principal = available_emi_capacity * tenure_months
    else:
        max_principal = (
            available_emi_capacity
            * ((1 + monthly_rate) ** tenure_months - 1)
        ) / (monthly_rate * (1 + monthly_rate) ** tenure_months)

    return round(max_principal, 2)