#!/bin/bash

if [ $1 == 1 ]; then
  python ./BenchManagementRaspbPI/kasa_energy_consumption.py

elif [ $1 == 0 ]; then
  python ./BenchManagementRaspbPI/temp_socket_testing_manager.py

else
  echo $1 is an invalid argument. Valid arguments
  echo "    1 starts the logging service"
  echo "    0 stops the logging service"
  exit 1
fi