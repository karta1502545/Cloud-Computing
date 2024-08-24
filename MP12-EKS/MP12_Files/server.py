from kubernetes import client, config, utils
from flask import Flask,request, jsonify
from os import path
from time import sleep
import yaml, random, string, json
import sys
import json
import traceback
import uuid
import time

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CoreV1Api()
batchv1 = client.BatchV1Api()
app = Flask(__name__)
period = 0.1

@app.errorhandler(500)
def internal_server_error(error):
    # Get the traceback as a string
    tb_str = traceback.format_exc()

    # Format the error response with traceback information
    response = jsonify({
        'error': 'Internal Server Error',
        'message': str(error),
        'traceback': tb_str
    })
    response.status_code = 500
    return response

def create_job(api_instance, job, job_name, namespace):
    api_response = api_instance.create_namespaced_job(
        body=job,
        namespace=namespace)
    print(f"Job created. status='{str(api_response.status)}'")
    # get_job_status(api_instance, job_name, namespace)

# def get_job_status(api_instance, job_name, namespace):
#     job_completed = False
#     while not job_completed:
#         api_response = api_instance.read_namespaced_job_status(
#             name=job_name,
#             namespace=namespace)
#         if api_response.status.succeeded is not None or \
#                 api_response.status.failed is not None:
#             job_completed = True
#         sleep(1)
#         print(f"Job status='{str(api_response.status)}'")

@app.route('/config', methods=['GET'])
def get_config():
    pods = []

    # your code here
    pods_info = v1.list_pod_for_all_namespaces(watch=False)
    for pod in pods_info.items:
        pod_info = {
            "node": pod.spec.node_name,
            "ip": pod.status.pod_ip,
            "namespace": pod.metadata.namespace,
            "name": pod.metadata.name,
            "status": pod.status.phase
        }
        pods.append(pod_info)

    output = {"pods": pods}
    output = json.dumps(output)

    return output, 200, {'Content-Type': 'application/json'}

@app.route('/img-classification/free',methods=['POST'])
def post_free():
    yaml_path = path.join(path.dirname(__file__), 'free-job.yaml')

    job_name = "free-job-" + str(uuid.uuid4())
    with open(yaml_path, 'r') as f:
        free_job_yaml = f.read()

    job_obj = yaml.safe_load(free_job_yaml)
    job_obj['metadata']['generateName'] = job_name

    create_job(batchv1, job_obj, job_name, namespace="free-service")
    time.sleep(period)
    return "Job executed successfully", 200


@app.route('/img-classification/premium', methods=['POST'])
def post_premium():
    # your code here
    data = request.get_data(as_text=True).split("\"")[3]
    yaml_path = path.join(path.dirname(__file__), 'premium-job.yaml')

    job_name = "premium-job-" + str(uuid.uuid4())
    with open(yaml_path, 'r') as f:
        premium_job_yaml = f.read()

    job_obj = yaml.safe_load(premium_job_yaml)
    job_obj['spec']['template']['spec']['containers'][0]['env'][0]['value'] = data
    job_obj['metadata']['generateName'] = job_name

    create_job(batchv1, job_obj, job_name, namespace="default")
    time.sleep(period)
    return "Job executed successfully", 200


    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
