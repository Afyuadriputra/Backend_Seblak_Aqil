from datetime import UTC, datetime
from zoneinfo import ZoneInfo

APP_TIMEZONE = ZoneInfo("Asia/Jakarta")
APP_TIMEZONE_LABEL = "WIB"
MONTH_NAMES_ID = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "Mei",
    6: "Jun",
    7: "Jul",
    8: "Agu",
    9: "Sep",
    10: "Okt",
    11: "Nov",
    12: "Des",
}


def utc_now() -> datetime:
    return datetime.now(UTC)


def jakarta_now() -> datetime:
    return datetime.now(APP_TIMEZONE)


def format_datetime_jakarta(value: datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    local_value = value.astimezone(APP_TIMEZONE)
    month_name = MONTH_NAMES_ID[local_value.month]
    return (
        f"{local_value.day:02d} {month_name} {local_value.year}, "
        f"{local_value.hour:02d}.{local_value.minute:02d} {APP_TIMEZONE_LABEL}"
    )
