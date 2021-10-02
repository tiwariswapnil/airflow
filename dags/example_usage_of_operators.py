import airflow
import json
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.models import Variable
from datetime import timedelta, datetime, timezone

args = {
    'owner': 'tiwariswapnil',
}

dag = DAG(
    dag_id='example_dags',
    default_args=args,
    start_date= datetime.now() - timedelta(minutes=15),
    schedule_interval='0 0 1-3 * *',
    dagrun_timeout=timedelta(minutes=60),
    tags=[]
)

def check_service_response(response, ti):
    print("Response Status: {}".format(response.status_code))
    print("Url: {}".format(response.url))
    access_token = response.json()['data']['access_token']
    print("access_token: {}".format(access_token))
    ti.xcom_push('access_token', access_token)
    return True

def check_upload_file_service_response(response, ti):
    print("Url: {}".format(response.url))
    print("Upload file Response Status: {}".format(response.status_code))
    return True

# t1 and t2 are examples of BashOperator
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    dag=dag,
)

# t3 and t4 are examples of API call operators
t3 = SimpleHttpOperator(
    task_id='get_authentication',
    http_conn_id='abc',
    method='POST',
    endpoint='Authentication',
    data={"username":"admin","password":"admin"},
    response_check=check_service_response,
    dag=dag)

t4 = SimpleHttpOperator(
    task_id='upload_endpoint',
    http_conn_id='upload',
    method='POST',
    endpoint='UploadFile',
    headers={"Content-Type": "multipart/form-data", "Authorization": "Bearer " + "{{ ti.xcom_pull(task_ids='get_authentication', key = 'access_token') }}"},
    data={"file": open('/opt/airflow/file_name.txt', 'rb'), "folderName" : "folder"},
    response_check=check_upload_file_service_response,
    dag=dag)

# t5 is an example of oracle operators - Run query on a database
t5 = OracleOperator(
    task_id='get_batchId',
    oracle_conn_id='Oracle_schema',
    sql= 'SQL Query',
    dag=dag)

t3 >> t4