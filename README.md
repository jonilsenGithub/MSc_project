# MSc_project

## Folders and files explained

### -unused_attempts:
Contains 3 models attempted. However, due to various reasons specified in dissertation paper, paragraph VIII, they could not be deployed. These have not been commented as they are not a part of the complete project, but only included to show the extent to which they have required time consumption.

### -models:
#### --euclidean_distance.ipynb:
Displays the creation of the euclidean distance model deployed in flask_euc.py

#### --machine_learning.ipynb:
Displays the creation of both KNN and SVC deployed in flask_ml.py.

Structure:
- Dataset was processed

- KNN was applied
- GridSearch was performed to determine the best parameter combination for KNN
- Cross-validation was used to determine what average accuracy score is using several different combinations of trainingset and testset

- SVC was applied
- GridSearch was performed to determine the best parameter combination for SVC
- Cross-validation was also to determine what average accuracy score is using several different combinations of trainingset and testset

### -flask_euc:
Contains the files needed to create a Docker image, which can be instanciated in a Docker container

### -flask_ml:
The folders knn and svc are identical, except different algorithms from Scikit-learn are imported, used and deployed. During testing knn was first used in the image folder. After which, KNeighborsClassifier import was replaced with SVC import and related function names and variable names also changed from 'knn' to 'svc'.

#### |__knn:
Contains the files needed to create a Docker image, which can be instanciated in a Docker container

#### |__svc:
Contains the files needed to create a Docker image, which can be instanciated in a Docker container

### -database_interaction.md:
Describes how the keystroke.csv dataset was imported to Cassandra container, stored in keystroke measurements table, followed by table being copied to a .csv file and exported to the flask application container folders. Additionally a table with profiles was created in the same keyspace to make things as authentic as possible. Profiles were imported into the database and subsequentially copied to .csv file, which was exported to the flask_euc application container folder.

The purpose with this .md file is to visualize what interactions would take place between the applications and databases in a dynamic environment through a software automating these interactions whenever new user measurements was received by the measurements database table.

### -request.py
Sends requests to the running application containers and prints the response. This file was used for both the flask_euc requests and flask_ml requests.

## Instructions for use:
- All images can be build using Docker, if requirements in folder's Dockerfile are met
- Sending requests to the containers will require following instructions in the database_interaction.md file using keystroke dynamics dataset from: https://www.kaggle.com/carnegiecylab/keystroke-dynamics-benchmark-data-set
- After exporting the measurements table you will also need to further export a copy to your computer, from which you will be running requirements.py
