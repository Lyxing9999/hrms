from __future__ import annotations


class PayrollFacade:
    def __init__(
        self,
        *,
        generate_monthly_payroll,
    ) -> None:
        self._generate_monthly_payroll = generate_monthly_payroll

    def generate(self, **kwargs):
        return self._generate_monthly_payroll.execute(**kwargs)