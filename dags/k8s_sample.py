import datetime

from airflow import DAG
from kubernetes.client import models as k8s
#from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
#    KubernetesPodOperator,
#)

from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

resources = k8s.V1ResourceRequirements(
    limits={"memory": "1Gi", "cpu": "1"},
    requests={"memory": "100Mi", "cpu": "0.1"},
)
with DAG(
    "example_kubernetes_python",
    schedule_interval=None,
    start_date=datetime.datetime(2020, 2, 2),
    tags=["example"],
) as dag:

    run_python = KubernetesPodOperator(
        task_id="run_python_script",
        name="run_python_script",
        namespace="airflow",
        image="python:3.10-slim",  # 이 이미지에 필요한 파이썬 스크립트와 의존성이 포함되어 있어야 합니다.
        is_delete_operator_pod=True,
        cmds=["python", "-c"],
        arguments=[
            'print("Hello, World!")'
        ],  # 여기에 파이썬 스크립트를 입력하거나 실행할 파이썬 파일의 경로를 제공하세요.
        get_logs=True,
        # resources=resources,
    )
