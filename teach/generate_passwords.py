#!/bin/python3
####
#### This script will generate a series of passwords to be used
#### in password cracking assignments. The passwords are grouped
#### by patterns that represent different risks as identified
#### in my assessment method. 
####
#### In the learning lab, each password is worth points. Some
#### passwords are worth more than others.
#### 
####

####
#### Point System
####
#### This is not intended to be related to cryptographic difficulty
#### We are guessing the password based on risk factor. How easy are
#### these to guess?

####  -- 1 point per too short password
####  -- 2 points per simple password
####  -- 3 points per password substitution
####  -- 3 points per based on "password"
####  -- 4 points per keyboard pattern
####  -- 5 points per based on 
####  -- 5 points > 14 chars
####  -- 2 points random complex 8-9 chars
####  -- 3 points random complex 10-11 chars
####  -- 4 points random complex 12-14 chars
####  -- 2 points per character! random complex 15+ chars

####  -- 1 point per criticality level (1-5)


#### Generate Random Complex Passwords of each length 3-21 characters

def random_complex(int length):
