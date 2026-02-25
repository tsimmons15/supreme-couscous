from datetime import datetime
from airflow import DAG
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator

dag = DAG(
    'aeo_web_streaming',
    description='Monitor AEO web streaming pipeline',
    schedule_interval=None,  # Streaming - manual trigger
    start_date=datetime(2026, 2, 1),
    catchup=False
)

start_streaming = DataflowTemplatedJobStartOperator(
    task_id='start_web_streaming',
    template='gs://{{ var.value.project_id }}-templates/web_streaming_template',
    gcp_conn_id='google_cloud_default',
    parameters={
        'input_topic': 'projects/{{ var.value.project_id }}/topics/aeo-web-events-{{ var.value.env }}',
        'output_table': '{{ var.value.project_id }}:aeo_curated_{{ var.value.env }}.web_events_fact'
    },
    dag=dag
)
