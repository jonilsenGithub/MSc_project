# Creating database


#### Creating Cassandra container called 'keystroke_database' from public Docker image:
````
sudo docker run --name keystroke_database -p 9042:9042 -d cassandra:latest
````
Entering container:
````
sudo docker exec -it cassandra-test cqlsh
````
#### Creating keyspace in container:
````
CREATE KEYSPACE keystroke WITH REPLICATION = {'class':'SimpleStrategy','replication_factor':1};
````
#### Creating the table 'measurements' in keyspace:
````
CREATE TABLE keystroke.measurements(subject varchar, sessionIndex int, rep int, H_Period float, DD_period_t float, UD_period_t float, H_t float, DD_t_i float, UD_t_i float, H_i float, DD_i_e float, UD_i_e float, H_e float, DD_e_five float, UD_e_five float, H_five float, DD_five_Shift_r float, UD_five_Shift_r float, H_Shift_r float, DD_Shift_r_o float, UD_Shift_r_o float, H_o float, DD_o_a float, UD_o_a float, H_a float, DD_a_n float, UD_a_n float, H_n float, DD_n_l float, UD_n_l float, H_l float, DD_l_Return float, UD_l_Return float, H_Return float, primary key(subject,rep,sessionIndex));
````
Copying keystroke.csv dataset from Ubuntu server to Cassandra container keystroke_database:
````
sudo docker cp /home/ubuntu/profiles.csv 15705f651efa:/home
````
Inserting samples from keystroke.csv into measurements table:
````
COPY keystroke.measurements(subject,sessionIndex, rep, H_Period , DD_period_t , UD_period_t , H_t , DD_t_i , UD_t_i , H_i , DD_i_e , UD_i_e , H_e , DD_e_five , UD_e_five , H_five , DD_five_Shift_r , UD_five_Shift_r , H_Shift_r , DD_Shift_r_o , UD_Shift_r_o , H_o , DD_o_a , UD_o_a , H_a , DD_a_n , UD_a_n , H_n , DD_n_l , UD_n_l , H_l , DD_l_Return , UD_l_Return , H_Return) FROM '/home/keystroke.csv' WITH delimiter=',' AND header=TRUE;
````
#### Creating the table profiles:
````
CREATE TABLE keystroke.profiles(subject int,salt int,H_Period float, DD_period_t float, UD_period_t float, H_t float, DD_t_i float, UD_t_i float, H_i float, DD_i_e float, UD_i_e float, H_e float, DD_e_five float, UD_e_five float, H_five float, DD_five_Shift_r float, UD_five_Shift_r float, H_Shift_r float, DD_Shift_r_o float, UD_Shift_r_o float, H_o float, DD_o_a float, UD_o_a float, H_a float, DD_a_n float, UD_a_n float, H_n float, DD_n_l float, UD_n_l float, H_l float, DD_l_Return float, UD_l_Return float, H_Return float, primary key(subject));
````
Copying profiles.csv produced by euc_profiles.py to Cassandfra container keystroke_database:
````
sudo docker cp /home/ubuntu/flask_euc/profiles.csv 15705f651efa:/profiles.csv
````
Inserting profiles produces by euc_profiles.py
````
COPY keystroke.profiles(subject,salt,H_Period , DD_period_t , UD_period_t , H_t , DD_t_i , UD_t_i , H_i , DD_i_e , UD_i_e , H_e , DD_e_five , UD_e_five , H_five , DD_five_Shift_r , UD_five_Shift_r , H_Shift_r , DD_Shift_r_o , UD_Shift_r_o , H_o , DD_o_a , UD_o_a , H_a , DD_a_n , UD_a_n , H_n , DD_n_l , UD_n_l , H_l , DD_l_Return , UD_l_Return , H_Return) FROM '/home/profiles.csv' WITH delimiter=',' AND header=TRUE;
````
# PLEASE NOTE

In an active environment where the database would constantly receive new user samples, the code below belong to a separate script created to handle .csv export whenever the database was updated with new user samples. However, as we are working with a static dataset this is done manually once from command line.

#### Exporting databases to .csv files in containers home folder:
````
COPY keystroke.measurements TO '/home/kd.csv' WITH delimiter=',' AND header=TRUE;

````
#### Manually copying .csv file saved in Cassandra container to both model containers:
````
sudo docker cp 15705f651efa:/home/kd.csv /home/ubuntu/flask_euc
sudo docker cp 15705f651efa:/home/kd.csv /home/ubuntu/flask_ml
````
