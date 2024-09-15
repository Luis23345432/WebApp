from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    DefaultStackSynthesizer
)
from aws_cdk import Environment
from constructs import Construct

class WebAppStack(Stack):

    def _init_(self, scope: Construct, id: str, **kwargs) -> None:
        # Configuración del DefaultStackSynthesizer
        synthesizer = DefaultStackSynthesizer(
            file_assets_bucket_name="pruebaluis1223",
            bucket_prefix="",
            cloud_formation_execution_role="arn:aws:iam::711397755029:role/LabRole",
            deploy_role_arn="arn:aws:iam::711397755029:role/LabRole",
            file_asset_publishing_role_arn="arn:aws:iam::711397755029:role/LabRole",
            image_asset_publishing_role_arn="arn:aws:iam::711397755029:role/LabRole"
        )

        super()._init_(scope, id, synthesizer=synthesizer, **kwargs)

        # Configuración de recursos AWS
        vpc = ec2.Vpc.from_lookup(self, "ExistingVpc", vpc_id="vpc-0bb0e5149780c8b1e")

        instance_role = iam.Role.from_role_arn(
            self, "ExistingRole",
            role_arn="arn:aws:iam::711397755029:role/LabRole"
        )

        # Usar LookupMachineImage para encontrar la última imagen de Ubuntu
        ubuntu_ami = ec2.LookupMachineImage(
            name="ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*",
            owners=["099720109477"]  # Canonical
        )

        instance = ec2.Instance(self, "WebServer",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ubuntu_ami,
            vpc=vpc,
            role=instance_role
        )

        user_data_commands = [
            "apt-get update -y",
            "apt-get install -y git",
            "git clone https://github.com/Luis23345432/websimple.git",
            "git clone https://github.com/Luis23345432/webplantilla.git",
            "cd web-simple",
            "nohup python3 -m http.server 8001 &",
            "cd ../web-plantilla",
            "nohup python3 -m http.server 8002 &"
        ]

        instance.user_data.add_commands(*user_data_commands)

        instance.connections.allow_from_any_ipv4(ec2.Port.tcp(8001), "Allow HTTP traffic on port 8001")
        instance.connections.allow_from_any_ipv4(ec2.Port.tcp(8002), "Allow HTTP traffic on port 8002")