from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.beam.operators.beam import BeamRunPythonPipelineOperator

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'aeo_pos_batch',
    default_args=default_args,
    description='Daily POS batch processing',
    schedule_interval='@daily',
    start_date=datetime(2026, 2, 1),
    catchup=False
)

pos_batch = BeamRunPythonPipelineOperator(
    task_id='process_pos_batch',
    template_path='gs://{{ var.value.project_id }}-templates/pos_batch_template',
    py_requirements_file='gs://{{ var.value.project_id }}-dags/requirements.txt',
    parameters={
        'input': 'gs://{{ var.value.project_id }}-aeo-raw-data-dev/*.csv',
        'output': '{{ var.value.project_id }}:aeo_curated_dev.pos_sales_fact'
    },
    gcp_conn_id='google_cloud_default',
    job_name='aeo-pos-batch-{{ ds_nodash }}',
    dag=dag
)
