from azureml.core import Experiment, ScriptRunConfig, Workspace, Environment, Model
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice

# Load Azure ML workspace
ws = Workspace.from_config()

# Define the environment from the YAML file
env = Environment.from_conda_specification(name="my_env", file_path="my_env.yml")

# Create an experiment
experiment = Experiment(workspace=ws, name='train_and_deploy')

# Define the script run configuration for training
training_config = ScriptRunConfig(source_directory='.',
                                  script='my_script.py',
                                  compute_target='cpu-cluster2nd',
                                  environment=env)

# Submit the training job
run = experiment.submit(training_config)
run.wait_for_completion()

# Retrieve the registered model
model = Model(ws, 'group11_model')

# Define the inference configuration
inference_config = InferenceConfig(entry_script="score.py", environment=env)

# Define the deployment configuration
deployment_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)

# Deploy the model
service = Model.deploy(workspace=ws,
                       name="groupeleven-service",
                       models=[model],
                       inference_config=inference_config,
                       deployment_config=deployment_config)

# Wait for the deployment to complete
service.wait_for_deployment(show_output=True)

print(f"Service state: {service.state}")
print(f"Scoring URI: {service.scoring_uri}")
