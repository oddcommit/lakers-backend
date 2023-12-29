#!/usr/bin/env python3
# pylint: skip-file
import os

import aws_cdk as cdk

from temp_cdk.from_book_batch_stack import FromBookBatchStack
from temp_cdk.temp_cdk_stack import TempCdkStack

app = cdk.App()
TempCdkStack(
    app,
    "TempCdkStack",
    env=cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
)
FromBookBatchStack(
    app,
    "FromBookBatchStack",
    env=cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
)

app.synth()
