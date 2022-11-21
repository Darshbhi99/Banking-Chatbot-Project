# Banking-Chatbot-Project

## Create the Virtual Environment 
"conda create -p venv python=3.9"

## Activate the environment
"conda activate ./venv"

## Run the requirement file
pip install -r requirements.txt

## Edit the mysql database information in the mysqldata.txt
### host
### user
### password
### port
### database

## Run the python file for getting the dataset from the mysql
"python data_retriever.py"

## Run the file for flask app
"python main.py"