import csv

challenge_file = '/home/ec2-user/passlab/challenge.txt'
pot_file = '/home/ec2-user/hashcat/hashcat.potfile'

reader = csv.DictReader(open(challenge_file), delimiter=':')
challenges = list(reader)

users = {}
for challenge in challenges:
    users[challenge['ntlm_hash']] = {}
    users[challenge['ntlm_hash']]['account'] = challenge['account_name']
    users[challenge['ntlm_hash']]['criticality'] = challenge['criticality']
    users[challenge['ntlm_hash']]['department'] = challenge['department']

reader = csv.DictReader(open(pot_file), delimiter=':', fieldnames=['hash','password'])
results = list(reader)

passwords = {}
for result in results:
    try:
        print(f"{users[result['hash']]['account']}:{users[result['hash']]['criticality']}:{result['password']}") 
    except Exception as e:
        pass   
