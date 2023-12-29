# pylint: skip-file

import json
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


class FromBookBatchStack(Stack):
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
            file="from-book-batch.Dockerfile",
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
        if prefs_file := self.node.try_get_context("prefs-file"):
            with open(prefs_file) as f:
                prefs_config: dict = json.load(f)
                for prefs, config in prefs_config["prefectures"].items():
                    chunk_num_arg: str = config.get("chunk-num")
                    self.configure_scheduled_tasks(
                        prefs, chunk_num_arg, cluster, image, secrets, security_group
                    )
        else:
            prefs: str = self.node.try_get_context("prefs")
            chunk_num_arg: str = self.node.try_get_context("chunk-num")
            self.configure_scheduled_tasks(
                prefs, chunk_num_arg, cluster, image, secrets, security_group
            )

    def configure_scheduled_tasks(
        self, prefs: str, chunk_num_arg: str, cluster, image, secrets, security_group
    ):
        chunk_num_int: int = int(chunk_num_arg) if chunk_num_arg else 1
        task_envs = {
            "LAKERS_TARGET_PREFECTURES": prefs,
        }
        for i in range(chunk_num_int):
            idx = i + 1
            envs = dict(task_envs)
            if chunk_num_arg:
                envs["LAKERS_TARGET_CITIES_CHUNK"] = f"{idx}/{chunk_num_arg}"
            task = ScheduledFargateTask(
                self,
                f"ScheduledFargateTask{prefs.replace(',', '')}Chunk{idx}",
                cluster=cluster,
                scheduled_fargate_task_image_options=ScheduledFargateTaskImageOptions(
                    image=image,
                    secrets=secrets,
                    memory_limit_mib=122880,  # High spec
                    cpu=16384,
                    environment=envs,
                ),
                subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                schedule=appscaling.Schedule.cron(
                    minute="10", hour="7", day="6", month="9"  # fix. <- UTC
                ),
                security_groups=[security_group],
            )
            task.task_definition.default_container.add_ulimits(
                ecs.Ulimit(
                    name=ecs.UlimitName.NOFILE,
                    soft_limit=1048576,
                    hard_limit=1048576,
                )
            )
