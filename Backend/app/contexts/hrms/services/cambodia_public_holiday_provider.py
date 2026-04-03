from __future__ import annotations

from datetime import date as date_type
from typing import Any
import requests


class CambodiaPublicHolidayProvider:
    BASE_URL = "https://calendarific.com/api/v2/holidays"

    def __init__(self, *, api_key: str) -> None:
        self.api_key = api_key

    def get_cambodia_holidays(self, year: int) -> list[dict[str, Any]]:
        if not self.api_key:
            raise ValueError("CALENDARIFIC_API_KEY is not configured")

        response = requests.get(
            self.BASE_URL,
            params={
                "api_key": self.api_key,
                "country": "KH",
                "year": year,
            },
            timeout=20,
        )
        response.raise_for_status()

        payload = response.json()
        holidays = payload.get("response", {}).get("holidays", [])

        items: list[dict[str, Any]] = []

        for item in holidays:
            raw_date = item.get("date", {}).get("iso")
            if not raw_date:
                continue

            holiday_date = date_type.fromisoformat(str(raw_date)[:10])

            name = (item.get("name") or "").strip()
            description = (item.get("description") or "").strip() or None

            local_name = None
            for t in item.get("name_local", []) or []:
                if isinstance(t, dict):
                    local_name = (t.get("text") or "").strip() or None
                    if local_name:
                        break

            if not name:
                continue

            items.append(
                {
                    "name": name,
                    "name_kh": local_name,
                    "date": holiday_date,
                    "is_paid": True,
                    "description": description,
                }
            )

        unique_by_date: dict[str, dict[str, Any]] = {}
        for item in items:
            unique_by_date[item["date"].isoformat()] = item

        return list(unique_by_date.values())