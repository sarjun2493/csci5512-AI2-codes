/*
*CSci5512 Spring'16 Homework 4
*login: subra174
*date: 04/14/16
*name: Arjun Subrahmanyan
*id: 5217513
*algorithm: Decision Tree (max depth 4)*/

INSTRUCTIONS TO RUN THE PROGRAM (Tested on Linux (Ubuntu))
----------------------------------------------------------
python dtree4.py <path of file that has training set>


SAMPLE PROGRAM EXECUTION ON COMMAND LINE
----------------------------------------
python dtree4.py trData.txt


SAMPLE RESULT
-------------
The decision tree for this training set is: 
(Pat = Some)  ==> T
(Pat = Full) ^ (Hun = T) ^ (Type = French)  ==> F
(Pat = Full) ^ (Hun = T) ^ (Type = Thai) ^ (Fri = T)  ==> T
(Pat = Full) ^ (Hun = T) ^ (Type = Thai) ^ (Fri = F)  ==> F
(Pat = Full) ^ (Hun = T) ^ (Type = Burger)  ==> T
(Pat = Full) ^ (Hun = T) ^ (Type = Italian)  ==> F
(Pat = Full) ^ (Hun = F)  ==> F
(Pat = None)  ==> F

The training error is: 0.0
LOOCV is : 0.416666666667


PROGRAM DESCRIPTION
-------------------
This program implements a decision tree, with a maximum level of 4. A level counter is maintained to prune the tree at the desired depth.
The path of the filename is passed as an argument. 
Each record is represented as a key value pair between attributes and values.
This is used to construct the tree, based on entropy calculations to decide the attribute to split on at each level. 
The tree is represented via decision nodes and terminal nodes that are defined in Tree.py. 
The training error and LOOCV are calculated as fraction of misclassified instances
