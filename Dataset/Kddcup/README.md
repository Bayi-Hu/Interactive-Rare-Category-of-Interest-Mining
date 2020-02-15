# Description of Kddcup Dataset

Software to detect network intrusions protects a computer network from unauthorized users, including perhaps insiders. The intrusion detector learning task is to build a predictive model (i.e. a classifier) capable of distinguishing between \``bad\'' connections, called intrusions or attacks, and \``good\'' normal connections.
The 1998 DARPA Intrusion Detection Evaluation Program was prepared and managed by MIT Lincoln Labs.
The objective was to survey and evaluate research in intrusion detection. 
A standard set of data to be audited, which includes a wide variety of intrusions simulated in a military network environment, was provided.  
The 1999 KDD intrusion detection contest uses a version of this dataset, therefore it was also called KDDcup dataset).

In our rare category mining task, the version of a 10% subset is adopted, i.e., kddcup.data_10_percent.

1. **Number of Instances**: 494,021

2. **Number of Attributes**: 41

    A complete listing of the set of features defined for the connection records is given in the three tables below.  The data schema of the contest dataset is available in machine-readable form .

    |feature name | description | type |
    | ----------- | ----------- | ---- |
    |  duration   |length (number of seconds) of the connection | continuous |
    |protocol_type | type of the protocol, e.g. tcp, udp, etc. | discrete |
    |service | network service on the destination, e.g., http, telnet, etc. | discrete |
    |src_bytes | number of data bytes from source to destination | continuous |
    |dst_bytes | number of data bytes from destination to source | continuous |
    |flag | normal or error status of the connection |discrete| 
    |land | 1 if connection is from/to the same host/port; 0 otherwise | discrete|
    |wrong_fragment | number of \``wrong\'' fragments | continuous|
    |urgent | number of urgent packets | continuous |
    Table 1: Basic features of individual TCP connections.

    |feature name | description | type |
    | ----------- | ----------- | ---- |
    |hot | number of \``hot\'' indicators | continuous |
    |num_failed_logins | number of failed login attempts |	continuous |
    |logged_in | 1 if successfully logged in; 0 otherwise | discrete |
    |num_compromised |	number of \``compromised\'' conditions | continuous |
    |root_shell | 1 if root shell is obtained; 0 otherwise | discrete |
    |su_attempted |	1 if \``su root\'' command attempted; 0 otherwise | discrete|
    |num_root |	number of ``root'' accesses | continuous |
    |num_file_creations | number of file creation operations | continuous |
    |num_shells | number of shell prompts |	continuous |
    |num_access_files |	number of operations on access control files | continuous|
    |num_outbound_cmds | number of outbound commands in an ftp session 	| continuous|
    |is_hot_login |	1 if the login belongs to the ``hot'' list; 0 otherwise  | discrete|
    |is_guest_login | 1 if the login is a ``guest''login; 0 otherwise | discrete|
    Table 2: Content features within a connection suggested by domain knowledge.

    |feature name | description | type |
    | ----------- | ----------- | ---- |
    |count | number of connections to the same host as the current connection in the past two seconds | continuous|
    | |Note: The following  features refer to these same-host connections.|	|
    |serror_rate | \% of connections that have \``SYN\'' errors | continuous |
    |rerror_rate |	\% of connections that have \``REJ\'' errors | continuous |
    |same_srv_rate | \% of connections to the same service | continuous |
    |diff_srv_rate | \% of connections to different services |continuous |
    |srv_count | number of connections to the same service as the current connection in the past two seconds |continuous|
    | |Note: The following features refer to these same-service connections.| |	
    |srv_serror_rate | \% of connections that have ``SYN'' errors |	continuous|
    |srv_rerror_rate | \% of connections that have ``REJ'' errors | continuous|
    |srv_diff_host_rate | \% of connections to different hosts | continuous|
    Table 3: Traffic features computed using a two-second time window.
    
3. **Class Distribution**

    |Class Index |    Class Name   | Number of Instances | Percentage(%)|
    |---| --------------------- | ------------------- | ------------ |
    | 0 | smurf | 280790 | 56.838
    | 1 | satan | 1589 | 0.322
    | 2 | normal | 97278 | 19.691
    | 3 | neptune | 107201 | 21.7
    | 4 | pod | 264 | 0.053
    | 5 | ipsweep | 1247 | 0.252
    | 6 | teardrop | 979 | 0.198
    | 7 | back | 2203 | 0.446
    | 8 | portsweep | 1040 | 0.211
    | 9 | warezclient | 1020 | 0.206
    | 10 | imap | 12 | 0.002
    | 11 | nmap | 231 | 0.047
    | 12 | guess_passwd | 53 | 0.011
    | 13 | land | 21 | 0.004
    | 14 | warezmaster | 20 | 0.004
    | 15 | rootkit | 10 | 0.002
    | 16 | buffer_overflow | 30 | 0.006
    | 17 | loadmodule | 9 | 0.002
    | 18 | phf | 4 | 0.001
    | 19 | ftp_write | 8 | 0.002
    | 20 | spy | 2 | 0.0
    | 21 | perl | 3 | 0.001
    | 22 | multihop | 7 | 0.001
    
---
#### Acknowledgement:

This document is adapted from the paper:
> Cost-based Modeling and Evaluation for Data Mining With Application to Fraud and Intrusion Detection: Results from the JAM Project by Salvatore J. Stolfo, Wei Fan, Wenke Lee, Andreas Prodromidis, and Philip K. Chan. 
  
For more details, please refer to http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html.

For original data download, plese refer to http://kdd.ics.uci.edu/databases/kddcup99/kddcup.data_10_percent.gz
    
    