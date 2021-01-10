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
  
  ## CO-DEPENDENCY ERROR ##
  # List the DAGs.
  # Decipher the error message.
  # Use cat workspace/dags/codependent.py to view the Python code.
  
  ERROR - Failed to bag_dag: /home/repl/workspace/dags/codependent.py
  
  cat workspace/dags/codependent.py
  
  ----------------------------------


repl:~$ cat workspace/dags/codependent.py

from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = {
  'owner': 'dsmith',
  'start_date': datetime(2020, 2, 12),
  'retries': 1
}

codependency_dag = DAG('codependency', default_args=default_args)

task1 = BashOperator(task_id='first_task',
                     bash_command='echo 1',
                     dag=codependency_dag)

task2 = BashOperator(task_id='second_task',
                     bash_command='echo 2',
                     dag=codependency_dag)

task3 = BashOperator(task_id='third_task',
                     bash_command='echo 3',
                     dag=codependency_dag)

# task1 must run before task2 which must run before task3
task1 >> task2
task2 >> task3
task3 >> task1 # THIS LINE NEEDS TO BE DELETED.
# Using the Airflow UI to determine any issues with your DAGs is a great troubleshooting step. 
# For this particular issue, a loop, or cycle, is present within the DAG. 
# Note that technically removing the first dependency would resolve the issue as well, but the comments specifically reference the desired effect. 
# Commenting the desired effect in this way can often help resolve bugs in Airflow DAG execution.

### PythonOperator ###
  
  ## Example 1 ##
  # A simple printme function that writes a message to the task logs.
  
  # Import the PythonOperator
  from airflow.operators.python_operator import PythonOperator
  
  # Create the function printme()
  def printme():
    print("This goes in the logs!")
  
  # Create the PythonOperator instance called python_task and add the necessary arguments
  python_task = PythonOperator(
    task_id = 'simple_print',
    python_callable = printme,
    dag = example_dag)
  
  ## op_kwargs example ##
  # Define the function
  def sleep(length_of_time):
    time.sleep(length_of_time)
  
  # Create the PythonOperator
  sleep_task = PythonOperator(
    task_id = 'sleep',
    python_callable = sleep,
    op_kwargs = {'length_of_time': 5},
    # Note that the dictionary key must match the name of the function argument
    dag = example_dag)
  
  ## Example 1 ##
  # Pulls a file from a URL, then saves it to a designated path
  
  def pull_file(URL, savepath):
    r = requests.get(URL)
    with open(savepath, 'wb') as f:
        f.write(r.content)   
    # Use the print method for logging
    print(f"File pulled from {URL} and saved to {savepath}")
    # Note the use of f-strings above!
    # https://realpython.com/python-f-strings/
  
  from airflow.operators.python_operator import PythonOperator

  # Create the task
  pull_file_task = PythonOperator(
    task_id='pull_file',
    # Add the callable
    python_callable= pull_file,
    # Define the arguments
    op_kwargs= {'URL':'http://dataserver/sales.json', 'savepath':'latestsales.json'},
    dag=process_sales_dag
)
  
  # Add another Python task
  parse_file_task = PythonOperator(
    task_id= 'parse_file',
    # Set the function to call
    python_callable = parse_file,
    # Add the arguments
    op_kwargs={'inputfile':'latestsales.json', 'outputfile':'parsedfile.json'},
    # Add the DAG
    dag=process_sales_dag
)
  
  # Import the Operator
  from airflow.operators.email_operator import EmailOperator

  # Define the task
  email_manager_task = EmailOperator(
    task_id='email_manager',
    to='manager@datacamp.com',
    subject='Latest sales JSON',
    html_content='Attached is the latest sales JSON file as requested.',
    files='parsedfile.json',
    dag=process_sales_dag
)

# Set the order of tasks
pull_file_task >> parse_file_task >> email_manager_task
  
### EmailOperator ###
  
  ## Email Example ##
  # Sending a generated sales report upon completion of a workflow
  
  # Import the EmailOperator
  from airflow.operators.email_operator import EmailOperator
  
  # Create the operator
  email_task = EmailOperator(
    task_id = 'email_sales_report',
    to = 'sales_manager@example.com',
    subject = 'Automated Sales Report',
    html_content = 'Attached is the latest sales report',
    files = 'latest_sales.xlsx',
    dag = example_dag
  )
  
  
  
  
  
  
  
  
  
  
