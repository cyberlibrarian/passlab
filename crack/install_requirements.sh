#!/bin/sh
####
#### Requirements:
####   -- wget, git, and p7zip

#### 
#### Download hashcat and unpack it
####
wget https://hashcat.net/files/hashcat-6.2.6.7z
7za x hashcat-6.2.6.7z

####
#### Download OneRuleToRuleThemAll
####
#### Read about it here: https://notsosecure.com/one-rule-to-rule-them-all
#### and here https://cryptokait.com/2020/09/02/taking-password-cracking-to-the-next-level/
git clone https://github.com/NotSoSecure/password_cracking_rules.git

####
#### Download wordlists
####
wget https://crackstation.net/files/crackstation.txt.gz
wget https://crackstation.net/files/crackstation-human-only.txt.gz

####
#### Download hashcat rules
####
git clone https://github.com/praetorian-inc/Hob0Rules.git
git clone https://github.com/NSAKEY/nsa-rules.git
git clone https://github.com/NotSoSecure/password_cracking_rules.git
wget https://contest-2010.korelogic.com/hashcat-rules.tar.gz
tar -xzf hashcat-rules.tar.gz

####
#### Download password analysis tools
####
git clone https://github.com/digininja/pipal.git
git clone https://github.com/digininja/CeWL.git

####
#### John the Ripper for those that want it
####
git clone https://github.com/openwall/john.git
