from dataclasses import dataclass

from data_models.models import City, Plan, PlanArea, PlanType, Prefectures


@dataclass(frozen=True)
class PlanConfFactory:
    prefectures: list[Prefectures]
    cities: list[City]

    @staticmethod
    def build_plan_type(plan_name: str) -> PlanType:
        if not PlanType.objects.filter(name=plan_name).exists():
            return PlanType.objects.create(
                name=plan_name,
                price=100000,
            )

        plan_type = PlanType.objects.filter(name=plan_name).get()
        return plan_type

    def build_plan_area(self, plan_name: str) -> PlanArea:
        return PlanArea.objects.create(
            plan_name=plan_name,
            prefecture_code=self.prefectures[0],
            city_code=self.cities[0],
        )

    def build_plan(self, plan_name: str):
        plan_type = self.build_plan_type(plan_name)
        plan_area = self.build_plan_area(plan_name)
        return Plan.objects.create(plan_type=plan_type, plan_area=plan_area)
