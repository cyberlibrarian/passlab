#!/bin/python

# install jupyter notbooks for analysis
#pip3 install notebook pandas openpyxl jellyfish

## Requirements
import pandas as pd
import openpyxl as xl
import csv
import jellyfish as jf
import re

# Let's make sure we can see our output
pd.set_option("max_columns", None)
pd.set_option("max_colwidth", None)
pd.set_option("expand_frame_repr", False)
pd.options.display.max_seq_items = 200
pd.options.display.max_rows = 500

## Define location of files we will work with
# Hashes for every account from Active Directory, including history
hashes = "/home/ec2-user/crack/ad/hashes.ntds"
# hashcat potfile: hashes and recovered passwords
potfile = "/home/ec2-user/crack/potfile"
# Splunk ES identity inventory
identity = "/home/ec2-user/crack/ad/identities.csv"

## TODO: How will we get AD groups? Is there a python module that can help us extract that from NTDS.dit?
#https://airman604.medium.com/dumping-active-directory-password-hashes-deb9468d1633

## Load the hashes into a pandas dataframe
colnames = ['account', 'id', 'lm_hash', 'ntlm_hash', 'empty1', 'empty2', 'status_data1', 'status_data2']
df_account = pd.read_csv(hashes, delimiter=":", header=None, names=colnames)

# We need to concatentate status_data1 and status_data2. When the record contains pwdLastSet=<date> there is a colon which will acts
# as a deliminter in the parsring above. But when pwdLastSet=never, status_data2 will be empty. Putting them together solves the issue
df_account['status_data'] = df_account['status_data1'] + df_account['status_data2']

## Parse the domain from the account name
##  The account field will have several different types of account
##   1) domain\account
##   2) computer$
##   3) $account (not sure what starts with a dollar)
df_account[['username_without_history', 'history']] = df_account['account'].apply(lambda x: pd.Series(str(x).split('_history')) if('_history' in str(x)) else pd.Series([str(x), float('NaN')]))


df_account[['username_without_history']].value_counts()

df_account[['domain', 'username']] = df_account['username_without_history'].apply(lambda x: pd.Series(str(x).split('\\') if('\\' in str(x)) else pd.Series([float('NaN'), str(x)])))

# Right now we only set this for the current password
df_account['is_enabled'] = df_account['status_data'].str.match('.*\(status=Enabled\).*')

df_account['is_enabled'].value_counts()

df_account.loc[df_account['is_enabled']==True]

df_account['is_computer'] = df_account['username'].str.match('^.*\$.*$')

df_account[['username', 'is_computer']][df_account['is_computer']==False]

df_account['last_set'] = df_account['status_data'].str.extract('\(pwdLastSet=(\d{4}-\d{2}-\d{2})\s')

df_account['last_set'].value_counts()

## Load the potfile into a pandas dataframe
pot_colnames = ['ntlm_hash', 'password']
df_pot = pd.read_csv(potfile, delimiter=":", header=None, names=pot_colnames)
df_pot['pw_id'] = df_pot['password'].index
df_pot = df_pot.astype({"pw_id": "int32"})

### Password Length Analysis
df_pot['pw_length'] = df_pot['password'].str.len()
df_pot['pw_less_than_8'] = df_pot['pw_length'].apply(lambda x: True if x < 8 else False)
df_pot['pw_less_than_12'] = df_pot['pw_length'].apply(lambda x: True if x < 12 else False)
df_pot['pw_less_than_15'] = df_pot['pw_length'].apply(lambda x: True if x < 15 else False)

### Password is based on Password
df_pot['pw_password_jarow_score'] = df_pot['password'].apply(lambda x: jf.jaro_winkler_similarity('password'.upper(), str(x).upper()))
df_pot['pw_based_password'] = df_pot['password'].apply(lambda x: True if jf.jaro_winkler_similarity('password'.upper(), str(x).upper()) > 0.71 and 'crawford'.upper() not in str(x).upper() else False)

### Is this simple password?
df_pot['pw_is_simple'] = df_pot['password'].str.match(r'\w([a-z]+)(\d+)(\W+)')

# Find passwords based on keyboard patterns
keyboard_patterns = ['zxv', 'zxc', 'qwe', 'asd', 'jkl', 'zaq', 'aq1', 'xsw', 'z1x', 'q1w', 'a1s', '1qa', '2ws', 'qaz', 'wsx', 'fds']
df_pot['pw_based_keyboard'] = df_pot['password'].apply(lambda x: True if any(pattern in str(x).lower() for pattern in keyboard_patterns) else False)

df_pot[df_pot['pw_based_keyboard']==True][['password', 'pw_based_keyboard']]

#df_pot.loc[df_pot['password'].str.match(r'\w([a-z]+)(\d+)(\W+)') == True]
df_pot.loc[df_pot['pw_is_simple'] == True]


df_all = pd.merge(
    df_account,
    df_pot,
    how="outer",
    on="ntlm_hash",
    left_on=None,
    right_on=None,
    left_index=False,
    right_index=False,
    sort=True,
    suffixes=("_x", "_y"),
    copy=True,
    indicator=False,
    validate=None
)
df_all.fillna(value='unknown', inplace=True)
df_all.reset_index()

df_all[['username', 'history', 'ntlm_hash', 'password', 'pw_based_password', 'pw_length']]

# Only include current, enabled, non-computer accounts
df_person = df_all[df_all['is_computer']==False]
df_current = df_person[df_person['history']=='unknown']
df_enabled = df_current[df_current['is_enabled']==True]

df_enabled[['username', 'is_enabled']]['is_enabled'].value_counts()

df_enabled[df_enabled['password']!='unknown']['password']

# Count how often each password occurs in results
dfc_enabled = df_enabled.copy()
dfc_enabled['pw_reused'] = df_enabled['password'].apply(lambda x: int(df_enabled[df_enabled['password']==x].username.count()))
df_enabled = dfc_enabled

df_enabled[df_enabled['password']=="Winter2023!"][['username', 'pw_id', 'pw_reused']]

## Load the potfile into a pandas dataframe
df_identity = pd.read_csv(identity, delimiter=",")

# Merge the identity information with the password analysis
df_all = pd.merge(
    df_enabled,
    df_identity,
    how="outer",
    on="username",
    left_on=None,
    right_on=None,
    left_index=False,
    right_index=False,
    sort=True,
    suffixes=("_x", "_y"),
    copy=True,
    indicator=False,
    validate=None
)
df_all.fillna(value='unknown', inplace=True)

df_all[['username', 'password', 'title', 'business_unit']]

# Flag those accounts who passwords were recocovered
df_all['recovered'] = df_all['password'].apply(lambda x: False if str(x)=='unknown' else True)

df_all['recovered'].value_counts()

df_all.count()

# This is where we do something fancy eventually to create an xlsx table
# Maybe for now we just save a CSV file.
cols = ['username', 'display_name', 'type', 'title', 'business_unit', 'vip', 'da', 
        'last_logon', 'last_set', 'recovered', 'pw_id', 'pw_length', 'pw_reused', 
        'pw_based_password', 'pw_is_simple', 'pw_based_keyboard']
df_all.to_excel("analysis.xlsx", sheet_name="recovered_accounts", index=False, columns=cols)

# Explore final data
df_all[df_all['pw_based_password']==True][['username', 'password']]


