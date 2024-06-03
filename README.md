1. Replace tenant-id in main.tf and subscription-id in config.json with actual ids.
2. in terminal run the following commands: (terraform init - terraform fmt - terraform apply) to create azure ml resources
3. run: python train_and_deploy.py (to create a job that runs the model training and registering script, and then to deploy the model)
