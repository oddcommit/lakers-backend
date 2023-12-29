from datetime import datetime

from data_models.models import Plan, User, UserPlan


def connect_plan_to_user(
    user: User, plans: list[Plan], plan_start_date: datetime, plan_end_date: datetime
):
    for plan in plans:
        UserPlan.objects.create(
            plan=plan,
            user=user,
            contract_start_day=plan_start_date,
            contract_end_day=plan_end_date,
        ).save()
