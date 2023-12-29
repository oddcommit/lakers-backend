from datetime import datetime

from dateutil.relativedelta import relativedelta


def calc_term(date_base_string: str, month: int = 3) -> tuple[datetime, datetime]:
    plan_start_date = datetime.strptime(date_base_string, "%Y%m%d")
    plan_end_date = plan_start_date + relativedelta(months=month)
    return plan_start_date, plan_end_date
