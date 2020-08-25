#### Creating keystroke measurements database:

````
ubuntu@ip-172-31-74-205:~/flask_ml$ sudo docker run --name keystroke_database -p 9042:9042 -d cassandra:latest
ubuntu@ip-172-31-74-205:~/flask_ml$ sudo docker exec -it cassandra-test cqlsh
````

#### Creating keyspace and table for the measurements:

````
cqlsh> CREATE KEYSPACE keystroke WITH REPLICATION = {'class':'SimpleStrategy','replication_factor':1};
````
````
cqlsh> CREATE TABLE keystroke.measurements(subject varchar, sessionIndex int, rep int, H_Period float, DD_period_t float, UD_period_t float, H_t float, DD_t_i float, UD_t_i float, H_i float, DD_i_e float, UD_i_e float, H_e float, DD_e_five float, UD_e_five float, H_five float, DD_five_Shift_r float, UD_five_Shift_r float, H_Shift_r float, DD_Shift_r_o float, UD_Shift_r_o float, H_o float, DD_o_a float, UD_o_a float, H_a float, DD_a_n float, UD_a_n float, H_n float, DD_n_l float, UD_n_l float, H_l float, DD_l_Return float, UD_l_Return float, H_Return float, primary key(subject,rep,sessionIndex));
````

### PLEASE NOTE
In an active environment where the database would constantly receive new user samples, the code below belong to a separate script created to handle .csv export whenever the database was updated with new user samples. However, as we working with a static dataset this is done manually once from command line.

##### Exporting database to .csv file in containers home folder:

````
cqlsh> COPY keystroke.measurements TO '/home/kd.csv' WITH delimiter=',' AND header=TRUE;
````

##### Manually copying .csv file saved in Cassandra container to both model containers:

````
ubuntu@ip-172-31-74-205:~/flask_ml$ sudo docker cp 15705f651efa:/home/kd.csv /home/ubuntu/flask_euc
ubuntu@ip-172-31-74-205:~/flask_ml$ sudo docker cp 15705f651efa:/home/kd.csv /home/ubuntu/flask_ml
````
