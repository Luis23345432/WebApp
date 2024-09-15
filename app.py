#!/usr/bin/env python3
import os

import aws_cdk as cdk

from web_app.web_app_stack import WebAppStack


app = cdk.App()
WebAppStack(app, "WebAppStack", env={
    'account': '711397755029',  # Tu Account ID de AWS
    'region': 'us-east-1'  # Utiliza una variable de entorno o define la región directamente
})

app.synth()
