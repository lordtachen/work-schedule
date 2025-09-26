import pulumi
import pulumi_gcp as gcp
import pulumi_docker as docker

# Config
config = pulumi.Config()
image_name = "docker.io/library/nginx:latest" # e.g. "nginx:latest"
service_name = config.get("serviceName") or "my-service"

# 1. Pull the image from Docker Hub
docker_image = docker.RemoteImage("remoteImage",
    name=image_name
)

# 2. Create a Cloud Run service
cloud_run_service = gcp.cloudrun.Service(service_name,
    location="us-central1",
    template=gcp.cloudrun.ServiceTemplateArgs(
        spec=gcp.cloudrun.ServiceTemplateSpecArgs(
            containers=[gcp.cloudrun.ServiceTemplateSpecContainerArgs(
                image=docker_image.name,
            )],
        ),
    ),
)

# 3. Allow unauthenticated access
iam = gcp.cloudrun.IamMember("invoker",
    service=cloud_run_service.name,
    location=cloud_run_service.location,
    role="roles/run.invoker",
    member="allUsers"
)

# Export the Cloud Run URL
pulumi.export("url", cloud_run_service.statuses[0].url)
