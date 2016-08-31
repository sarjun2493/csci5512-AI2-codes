/*
*CSci5512 Spring'16 Homework 4
*login: subra174
*date: 04/14/16
*name: Arjun Subrahmanyan
*id: 5217513
*algorithm: 2-Decision List */

INSTRUCTIONS TO RUN THE PROGRAM (Tested on Linux (Ubuntu))
----------------------------------------------------------
python dlist2.py <path of file that has training set>


SAMPLE PROGRAM EXECUTION ON COMMAND LINE
----------------------------------------
python dlist2.py trData.txt


SAMPLE RESULT
-------------
The decision list is: 
1 : (Pat = Some) ==> T
2 : (Hun = F) ==> F
3 : (Fri = T) ^ (Price = $) ==> T
4 : (Alt = T) ==> F
5 : () ==> F

Training error : 0.0
LOOCV : 0.416666666667


PROGRAM DESCRIPTION
-------------------
This program implements a decision list, with a maximum of 2 literals for each test. 
The path of the filename is passed as an argument. 
Each record is represented as a key value pair between attributes and values.

This is used to construct the list. All possible tests of 1 and 2 literals are exhausted to find out the best one that removes the most number of examples at once.
The list is represented via decision nodes and terminal nodes that are defined in DecisionList.py. 
The training error and LOOCV are calculated as fraction of misclassified instances
