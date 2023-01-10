#!/bin/bash

DOWN='down'
UP='up'
MODE=$1

networkUp()
{
    mkdir __logs__/
    
    # Bring up the network
    docker-compose -f __docker__/local/docker-compose.yml -p genac-portal up -d --build

    # Making Migrations
    echo "[Making Migrations ...]"
    docker-compose -f __docker__/local/docker-compose.yml -p genac-portal exec genac-portal python3 manage.py makemigrations

    # Running Migrations
    echo "[Running Migrations ...]"
    docker-compose -f __docker__/local/docker-compose.yml -p genac-portal exec genac-portal python manage.py migrate --noinput

    # Inserting fixtures
    echo "[Inserting fixtures ...]"
    docker-compose -f __docker__/local/docker-compose.yml -p genac-portal exec genac-portal python manage.py loaddata approved_valuators_data default_data eppley_interest_data security_questions

    echo "[Done]"
    exit 1 # Exit script after printing help
}

networkDown() {
    # Destroying the network
    docker-compose -f __docker__/local/docker-compose.yml -p genac-portal down
    # --volume
}

error() {
    echo "\n----------------------------------"
    echo "Invalid Argument \"$MODE\""
    echo "----------------------------------"
    echo "Usage: sh develop [ argument ]"
    echo "Argument:"
    echo " - up"
    echo " - down"
    echo "----------------------------------\n"
}

# Main execution
if [ "$MODE" == "$UP" ] || [ "$MODE" == "" ]
then
    echo "Bring [$UP] the network ..."
    networkUp
elif [ "$MODE" == "$DOWN" ]
then
    echo "Bring [$DOWN] the network ..."
    networkDown
else
    error # Error function
fi