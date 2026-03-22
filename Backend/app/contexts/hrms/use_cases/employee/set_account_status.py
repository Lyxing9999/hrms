from __future__ import annotations


class SetAccountStatusUseCase:
    def __init__(self, *, iam_gateway) -> None:
        self.iam_gateway = iam_gateway

    def execute(self, *, user_id: str, status):
        return self.iam_gateway.set_user_status(
            user_id=user_id,
            status=status,
        )