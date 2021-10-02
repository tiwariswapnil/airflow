# Airflow

Apache Airflow is an open-source platform to Author, Schedule and Monitor workflows. Airflow helps create workflows using Python and these workflows can be scheduled and monitored easily with it. These worflows are created as directed acyclic graphs (DAGs) of tasks. 

## Components of Apache Airflow

1. **DAG**: It is the Directed Acyclic Graph – a collection of all the tasks that you want to run which is organized and shows the relationship between different tasks. It is defined in a python script.
2. **Web Server**: It is the user interface built on the Flask. It allows us to monitor the status of the DAGs and trigger them.
3. **Metadata Database**: Airflow stores the status of all the tasks in a database and do all read/write operations of a workflow from here.
4. **Scheduler**: It is responsible for scheduling the execution of DAGs. It retrieves and updates the status of the task in the database.

## Pre-requisites for running Airflow on Docker
1. Install Docker on your system
2. Install Docker compose on your system

To deploy Airflow on Docker compose, execute the following command in terminal-
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.1.1/docker-compose.yaml'
```

## Initializing Environment

1. Create the necessary files, directories and initialize the database
```
mkdir ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

2. On all operating systems, you need to run database migrations and create the first user account
```
docker-compose up airflow-init
```

## Running Airflow

After initialization is complete, you can start all services using the following command:
```
docker-compose up
```

## Accessing the environment

### Accessing the web interface

Once the cluster has started up, you can log in to the web interface and try to run some tasks.

The webserver available at: http://localhost:8080. The default account has the login airflow and the password airflow.

## Define your DAG

### Import the Libraries

Create a python DAG file inside the dags folder. Start by importing the required libraries for the workflow. 
```
from datetime import timedelta

# The DAG object
from airflow import DAG

# Operators
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
```

### Define DAG Arguments

An argument dictionary is created for every DAG and passed in to the DAG. Following are some of the arguments that you can define:

1. owner: The name of the owner of the workflow, should be alphanumeric and can have underscores but should not contain any spaces.
2. depends_on_past: If each time you run your workflow, the data depends upon the past run then mark it as True otherwise mark it as False.
3. start_date: Start date of your workflow
4. email: Your email ID, so that you can receive an email whenever any task fails due to any reason.
5. email_on_failure
6. email_on_retry
7. retries
8. retry_delay: If any task fails, then how much time it should wait to retry it.

```
args = {
    'owner': 'tiwariswapnil',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
```

### Define DAG

```
dag = DAG(
    dag_id='qin-batch2.0-census',
    default_args=args,
    start_date= datetime.now() - timedelta(minutes=15),
    schedule_interval='0 0 1-3 * *',
    dagrun_timeout=timedelta(minutes=60),
    tags=[]
)
```

### Define the Tasks

Tasks are generated when instantiating operator objects. An object instantiated from an operator is called a task. The first argument task_id acts as a unique identifier for the task.

There are different types of operators available. Some examples of the operators are:
1. BashOperator - executes a bash command
2. PythonOperator - calls an arbitrary Python function
3. EmailOperator - sends an email
4. SimpleHttpOperator - sends an HTTP request
5. MySqlOperator, SqliteOperator, PostgresOperator, MsSqlOperator, OracleOperator, JdbcOperator, etc. - executes a SQL command
6. Sensor - waits for a certain time, file, database row, S3 key, etc…
You can also come up with a custom operator as per your need.

t1 and t2 are examples of tasks created using BashOperator.
```
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
```
## Reference-
Refer to the `airflow/dags/upload-file.py /` file for creating a DAG
