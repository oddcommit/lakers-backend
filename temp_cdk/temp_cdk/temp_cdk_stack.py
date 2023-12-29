# pylint: skip-file

import os.path

from aws_cdk import Stack
from aws_cdk import aws_applicationautoscaling as appscaling
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ssm as ssm
from aws_cdk.aws_ecr_assets import DockerImageAsset
from aws_cdk.aws_ecs_patterns import (
    ScheduledFargateTask,
    ScheduledFargateTaskImageOptions,
)
from constructs import Construct

dirname = os.path.dirname(__file__)


class TempCdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        target_env = self.node.try_get_context("env")
        self.target_env = target_env
        target_env_ctx: dict = self.node.try_get_context("envs")[self.target_env]

        vpc = ec2.Vpc.from_lookup(self, "Vpc", vpc_id=target_env_ctx["vpc_id"])

        cluster = ecs.Cluster(self, "TempBackendJobCluster", vpc=vpc)
        asset = DockerImageAsset(
            self,
            "BuildImage",
            directory=os.path.join(dirname, "../.."),
            file="temp-batch.Dockerfile",
        )

        image = ecs.ContainerImage.from_docker_image_asset(asset)
        secrets = {
            "CORS_ALLOWED_ORIGINS": ecs.Secret.from_ssm_parameter(
                ssm.StringParameter.from_secure_string_parameter_attributes(
                    self,
                    "Secure_CORS_ALLOWED_ORIGINS",
                    parameter_name="/lakers-saas/backend/cors-allowed-origins",
                )
            ),
            "DB_USER": ecs.Secret.from_ssm_parameter(
                ssm.StringParameter.from_secure_string_parameter_attributes(
                    self,
                    "Secure_DB_USER",
                    parameter_name="/lakers-saas/backend/db-user",
                )
            ),
            "SECRET_KEY": ecs.Secret.from_ssm_parameter(
                ssm.StringParameter.from_secure_string_parameter_attributes(
                    self,
                    "Secure_SECRET_KEY",
                    parameter_name="/lakers-saas/backend/django-secret-key",
                )
            ),
            "ALLOWED_HOST": ecs.Secret.from_ssm_parameter(
                ssm.StringParameter.from_secure_string_parameter_attributes(
                    self,
                    "Secure_ALLOWED_HOST",
                    parameter_name="/lakers-saas/backend/allowed-host",
                )
            ),
            "DB_NAME": ecs.Secret.from_ssm_parameter(
                ssm.StringParameter.from_secure_string_parameter_attributes(
                    self,
                    "Secure_DB_NAME",
                    parameter_name="/lakers-saas/backend/db-name",
                )
            ),
            "DB_HOST": ecs.Secret.from_ssm_parameter(
                ssm.StringParameter.from_secure_string_parameter_attributes(
                    self,
                    "Secure_DB_HOST",
                    parameter_name="/lakers-saas/backend/db-host",
                )
            ),
            "DB_PASSWORD": ecs.Secret.from_ssm_parameter(
                ssm.StringParameter.from_secure_string_parameter_attributes(
                    self,
                    "Secure_DB_PASSWORD",
                    parameter_name="/lakers-saas/backend/db-password",
                )
            ),
        }
        security_group = ec2.SecurityGroup.from_lookup_by_id(
            self, "SG", security_group_id=target_env_ctx["security_group_id"]
        )
        task = ScheduledFargateTask(
            self,
            "ScheduledFargateTask",
            cluster=cluster,
            scheduled_fargate_task_image_options=ScheduledFargateTaskImageOptions(
                image=image,
                secrets=secrets,
                memory_limit_mib=122880,  # High spec
                cpu=16384,
            ),
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            schedule=appscaling.Schedule.cron(
                minute="*/30", hour="*", day="3", month="9"  # fix. <- UTC
            ),
            security_groups=[security_group],
        )
        task.task_definition.node.default_child.add_property_override(
            "EphemeralStorage.SizeInGiB", 50
        )
        task.task_definition.default_container.add_ulimits(
            ecs.Ulimit(
                name=ecs.UlimitName.NOFILE,
                soft_limit=1048576,
                hard_limit=1048576,
            )
        )
