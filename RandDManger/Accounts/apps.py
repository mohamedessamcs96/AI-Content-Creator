import sys

from django.apps import AppConfig
# from diffusers import DiffusionPipeline
# import torch


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Accounts"


# class MyAppConfig(AppConfig):
#     name = 'Accounts'

#     def ready(self):
#         # Initialize your image generation pipeline here
#         self.image_pipeline = DiffusionPipeline.from_pretrained(
#             "runwayml/stable-diffusion-v1-5",
#             torch_dtype=torch.float16
#         )
#         # Move the pipeline to GPU if available
#         if torch.cuda.is_available():
#             self.image_pipeline.to("cuda")
        