# RUU
Assignments of course Intrusion Detection System at Columbia University given by Professor Salvatore Stolfo. Work of this project is based on paper [Active Authentication using File System Decoys and User Behavior Modeling: Results of a Large Scale Study](https://www.sciencedirect.com/science/article/pii/S0167404818311258). 

## Workflow
1. Assumption: Intruders have got permissions to the system, but not familiar with the environment.
2. Log Collection: I defined three classes for collecting log WindowSensor, FileSensor and ProcessSensor in window_sensor.py, file_sensor.py and process_sensor.py. Examples of how to use them were included in each file. 
3. Feature Extraction: Actions in 1 min is taken as one instance, and 9 features were selected(number of process_created, process_deleted, window_top, window_leave, file_modified file_created, file_deleted, directory_created, directory_deleted). Parser class is defined for parsing three different log files, and parse them into a 2-D array with these features.
4. Model: the process of building a GMM model is included in model.py. 
5. Result: I have asked two friends to use my laptop for around 40 mins, and their log files are stranger_*_log.txt and stranger2_*_log.txt. 