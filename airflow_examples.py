etl_dag = DAG(
  dag_id = 'etl_pipeline',
  default_args = {"start_date": "2020-01-08"}
# Note that within any Python code, etl_dag is the variable identifier, but within the Airflow shell command, you must use the dag_id.
  
# Running a simple Airflow task
  # airflow run <dag_id> <task_id> <start_date>
  airflow run example-etl download-file 2020-01-10
  
# DAGs on the command line
  # list all DAGs
  airflow list_dags
  
  # help
  airflow -h
  
### EXAMPLE 1 ###  
# Import the DAG object
from airflow.models import DAG

# Define the default_args dictionary
default_args = {
  'owner': 'dsmith',
  'start_date': datetime(2020, 1, 14),
  'retries': 2
}

# Instantiate the DAG object
etl_dag = DAG('example_etl', default_args=default_args)
  
### EXAMPLE 2 ###
from airflow.models import DAG
default_args = {
  'owner': 'jdoe',
  'start_date': '2019-01-01'
}
dag = DAG( dag_id="etl_update", default_args=default_args )
  
### EXAMPLE 3 ###
from airflow.models import DAG
default_args = {
  'owner': 'jdoe',
  'email': 'jdoe@datacamp.com'
}
dag = DAG( 'refresh_data', default_args=default_args )  
  
### WEB INTERFACE ###
  
airflow webserver -h
# Start an airflow webserver on port 9090  
airflow webserver -p 9090
  
### OPERATORS ###
## TROUBLESHOOTING ##
  
  # The dummy operator is used for troubleshooting or for a task that has NOT yet been implemented
  DummyOperator(task_id = 'example', dag = dag)
## BASH OPERATOR ##
  # Import the BashOperator
  from airflow.operators.bash_operator import BashOperator
  # Executes a given bash command or script
  ## EXAMPLE 1 ##
  # Runs a bash command to echo "Example!" to standard output
  BashOperator(
    task_id = 'bash_example',
    bash_command = 'echo "Example!"',
    dag = ml_dag)
  ## Example 2 ##
  # Runs a predefined bash script for its command, runcleanup
  BashOperator(
    task_id = 'bash_script_example',
    bash_command = 'run_cleanup.sh',
    dag = ml_dag)
  ## Example 3 ##
  # Run a task_id, run the bash_command 'echo 1', and assisn the operator to a DAG.
  # Note that we defined the DAG in line 37.
  example_task = BashOperator(
    task_id = 'bash_ex',
    bash_command = 'echo 1',
    dag = dag)
  
  ## Example 4 ##
  # Run a quick data cleaning operation using cat and awk.
  bash_task = BashOperator(
    task_id = 'clean_addresses',
    bash_command = 'cat addresses.txt | awk "NF == 10" > cleaned.txt',
    dag = dag)
  
  ## Example 5 ##
  # A collection of 3 BashOperators in an Airflow workflow, with dependencies by the BitShift operator.
  
  # This adds reliability and repeatablity to common tasks run from the shell.
  # Import the BashOperator
  from airflow.operators.bash_operator import BashOperator

  # Define the first BashOperator 
    task1_cleanup = BashOperator(
      task_id='first_cleanup_task',
      # Define the bash_command
      bash_command='cleanup.sh',
      # Add the task to the dag
      dag= analytics_dag)
  
  # Define a second operator to run the `consolidate_data.sh` script
    task2_consolidate = BashOperator(
      task_id='second_consolidate_task',
      bash_command= 'consolidate_data.sh',
      dag = analytics_dag)

  # Define a final operator to execute the `push_data.sh` script
    task3_push_data = BashOperator(
      task_id='third_pushdata_task',
      bash_command='push_data.sh',
      dag = analytics_dag)
  
  ## DEPENDENCIES ##
  # task 1 must run before task 2
  # task 3 must run before task 2
  # task 1 or task 3 don
  task1_cleanup >> task2_consolidate
  task3_push_data >> task2_consolidate
  
  # Example of chained tasks
  # task_1 >> task_2 >> task_3
  
  
  
