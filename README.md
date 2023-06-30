# Password Assessment Lab
This folder contains practical exercises and supporting data files for learning how to assessment the risk of vulnerable passwords. Primarily this is done through automated password guessing (*password cracking*) with hashcat.

# Why *crack* passwords?
## Assessing Risk due to Vulnerable Passwords
A weak password is vulnerable to exploitation. It puts the systems the password gives access to at risk. What is the likelihood that exploiting that vulnerable password could lead to a material impact on the system? That risk depends on the criticality on of the system being protected, upon the type of threats that might exploit it, and upon how weak the password is.

By "cracking" passwords, we can gain insight into the process that caused the password to be vulnerable. Is it too short? Is it too simple? Is it based on something predictable? Is it similar to the account name it protects? Or the company? Or the system or application?

If we can guess the password we can then assess what made it vulnerable. Are people picking weak passwords due to training? Or perhaps they don't know their passwords are weak? Or perhaps complicated company rules cause people to choose easy-to-type passwords that are also easy-to-guess.

## Recovering Encrypted Data
Another reason to crack passwords is to recover encrypted data. There are many scenarios where important information has been stored in encrypted files, but the password is not available. Perhaps it was malicious encrypted or perhaps and the only employee who knew the password is not available but the data is needed.

In some cases, encrypted data is needed for a legal investigation and password-holders deny knowledge or refuse cooperation.

If we can guess the password, we can recover the data.

# Lab Scenarios
In this lab we will use a realistic but fictional company and present realistic scenarios where password guessing is required. We will show you simple but effective techniques to automate your password guessing.

The scenarios are all inspired by the Canadian television program *Traders*, which aired between 1996 and 2000. *Traders* centers on a Canadian Merchant Bank called Gardner Ross. Gardner Ross is a boutique banking firm knowing for competing with large firms, influencing the market, and some shady dealings. Their main competitor is the larger firm Federated Dundas. In our scenario, Federated Dundas is attempting to aquire Gardner Ross, but there are rumors of potential problems. 

Gardner Ross has as trading floor where they buy and sell stocks to create temporary spikes in cash floor (and commisions for clients in their Wealth Management departement). They have an analysis department that provides research and intelligence to other departments and published a well respected newsletter that investors subscribe to. They have a derivatives trader who uses computer models to engage in high speed training: highly volatile. The main business comes from their support for commercial companies seeking financing, deals, and IPOs. It's highly competitive and sometimes a dirty business.
 
For background (which you will need to complete some challenges) consult:
- [Traders Wiki](http://cyberpursuits.com/heckifiknow/traders/)
- [Traders Episode Guide](https://epguides.com/Traders/)
- [Traders Episode Guide](https://www.tvmaze.com/shows/8845/traders/episodeguide)
- [Traders Wikipedia Page](https://en.wikipedia.org/wiki/Traders_(TV_series))

# Exercises
### Section 1: Extracting Hashes
### Excercise 1a: Extracting hashes from encrypted MS Office documents
One of the most common password guessing tasks in forensics is recovering encrypted MS Office documents. MS Office used to have very poor password protection: it wasn't even enrypted. But in modern versions, the hashes for these documents are hard to crack. AES-256 with tens of thousands of rounds. Long passwords will be hard to guess, but that's OK. If you apply some psychology you can priotize guessing the most common password patterns first.

But before you can crack the password on an MS Office document, you need to extract the hash.

To do this we will use the *office2john.py* script that comes with John the Ripper. This will extract the hash in a format supported not just by "John" but by hashcat as well.

This is a simple lesson. This is all you have to do:

```
~/john/run/office2john.py file.docx > file.hash
cat file.hash
```

The output will look like this:

```
file.docx:$office$*2013*100000*256*16:hash
```

That is the hash you have to crack. Note that it tells you what version of Office made this file, and some of the technical details about the hashing algorithm. These are needed by hash cracking programs like *John the Ripper* and *hashcat*. 

In this example "2013" is the version of the Office document format. "100,000" is the number of rounds of hashing. "256" is the number of bytes in the AES algorithm.

### Excercise 1b: Extracting hashes from encrypted PDF documents
Another common encrypted format is PDF. Like MS Office, in the old days, the password protection on PDF was weak: there was no encryption at all. Today, it is strong and cracking it is a challenge. To extract the hash, we will use another program from *John the Ripper*:

```
~/john/run/pdf2john.pl file.pdf > file.hash
cat file.hash
```

### Excercise 1c: Extracting hashes from Active Directory
TBD This section will be developed later.

Active Directory contains all the records for all users and computers in your organization. Every account in Active Directory has a password (including computers) and these are stored as (very weak) MD4 hashes. If your adversary is able to compromise a Domain Control or an account with high privileges they will extract the NTDS.dit database and the secret keys used to encrypt it. This contains the MD4 hashes for all the account passwords. They are *easy* to crack.

There are many programs and methods for extracting these hashes but I urge you to diregard most of the advice on the Internet. Most pentester blogs will advise you to use methods that will leave senstive artifacts on the Domain Controller, or that will lower the security posture of the Domain Controller. For example, impacket-secretsdump.py is popular, but when run over the network it will start remote services on the Domain Controller and may create Volume Shadow Copies. It will not undo these changes.

Instead use DCSync from a hardened, trusted host that is explicitly added to the Active Directory group authorized to sync AD data. Or use the built-in ntdsutil.exe program to perform an IFM export. These methods are safer and are unlikely to reduce the security posture of the Domain Controller or leave sensitive artifacts on the server.

TBD TODO include standard instructions for securely handling ntdsutil IFM export and using secretsdump.py to extract the hashes.

## Section 2: Guessing Passwords with Hashcat and Pscyhology
In this section we will experiment with several popular methods for automated password guessing. These are not the only methods and they are not necassarily the most advanced. They balance effectiveness with simplicity. You can guess more passwords faster with these methods than with others. If you encounter "hard to crack" passwords, you may need to learn methods beyond these.

### Excercise 2a: Using Hashcat for different hash formats
We are going to use hashcat to automate our password guessing. Hashcat can handle a lot of hash formats. It will try to automatically guess the format of the input file you provide, but typically we would suppy that ourselves: not all formats can be guessed.

#### MS Office Hashes
Earlier we learned how to extract hashes from encrypted MS Office documents. If our input is MS Office 2013, we would use "9600" as our format:

[Extracting Hashes from Password Protected Microsoft Office Documents](https://medium.com/@klockw3rk/extracting-hash-from-password-protected-microsoft-office-files-b206438944d2)

```
./hashcat.bin -m 9600 -o file.txt hash.txt wordlist.txt
```

```
./hashcat.bin -m 9600 -o file.txt hash.txt wordlist.txt
```

#### PDF Hashes
PDF hashes using "10500". 

[Cracking PDF Hashes](https://nicholaslyz.com/blog-posts/2021-07-23-cracking-pdf-hashes/)

```
./hashcat.bin -m 10500 -o file.txt hash.txt wordlist.txt
```

### NTLM hashes
NTLM hashes are extremely popular due to how weak they are and how pervasive they are. Almost all organizations have Active Directory and thus this weakness of the MD4 hashing makes it a target for criminals and auditors who want to ensure passwords are resistant to guessing by criminals.

NTLM extracted from AD is "1000". There are other ways to capture NTLM credentials including those cached on workstations or sniffed on the network. Those have different formats.

```
./hashcat.bin -m 1000 -o file.txt --username hash.txt wordlist.txt
```

Importantly, we have to add "--username" when we crack AD NTLM hashes. Unlike MS Office or PDF documents, accounts have usernames and these will be in the file with multiple hashes. If you do not add "--username" you will get an error.

### Excercise 2b: Guessing with Wordlists ("Dictionary Attacks")
Every time a criminal leaks passwords stolen from a breached system, this can help us better understand how people choose passwords. People stick to patterns, and there are some passwords that are very common: many people pick the same password. 

A common approach to quickly guessing passwords is to assume that a common password might be used. We can use a "dictionary attack" to check if our hash is for a password that is already in an existing list of passwords. This method is easy and very fast.

In this example, we will guess the password of a NTLM passwords. With will use the famous "rockyou.txt" password list. Rockyou was a list of passwords from the breach of the "Rockyou" site. It is large and once was representative of password commonly choosen by many people.

Our hashes are in the file "lab1.txt".
The rockyou file is in "rockyou.txt.gz"

```
./hashcat.bin -O -w 4 -m 1000 --username lab1.txt rockyou.txt.gz
```

This will only take a few minutes. How many did we get?

With hashcat you can use a whole directory of files if you want. If you specify a directory instead of a file, it will try each file in the directory.

You can try this approach with other word lists as well. Check the ~/words/ directory for me. This will take longer.

There are many wordlists in available for download but it takes some strategy to pick the right one. Do you want to use actual leaked passwords? Or generated lists representing patterns? Or maybe phrases from songs? Or maybe names? Or words in languages other than English?

#### Where can I get more wordlists?
- John the Ripper's distribution comes with some
- SecLists on GitHub
- Crackstation
- KoreSecurity

I would advise against using the new "rockyou2021" list is not a good representation of *real human* passwords. It is a compilation of some real leaks, but includes mostly generated lists. Generated word lists are more useful when you apply specific rules to them. You are better off constructing rules or masks than using a precomputed synthetic list.

### Excercise 2c: Brute-force Guessing ("Mask Attacks")
The simplest method of guessing passwords is *brute-force*: guessing all possible combinations of characters, digits, and symbols.


### Excercise 2d: Guessing with Rules  ("Mangling Attacks")
Using "word mangling rules" is highly effective and fast. It is much more effective than a normal dictionary attack, and far faster than a "mask" attack. I recommend this as a starting point.

However, you have to choose your rules and wordlists carefully. 

The idea if that it will take each word in your wordlist and apply a rule to transfer the word. For example, a rule might replace all "a" characters with the symbol "@". People tend to use predictable patterns to create complex patterns. L33tSp3ak. 

Other rules will add numbers, dates, or common puntuation to a word. Common patterns that people use frequently. There are rules that will combine multiple words together, or that reverse words, or that include keyboard patterns like 'qwerty' that people use because they are easily typed and remembered.

To run a rule attack we use mode "0" and have to specify a rule file and a wordlist.

```
hashcat.bin -O -m 1000 --username -a 0 -r rules/best64.rule ntlm.txt words/rockyou.txt.gz
```

#### Rules that come with Hashcat
In hashcat, the "rules" folder contains a great base set of rules. Each does something different.

Listed from biggest to smallest ruleset

- dive.rule
- generated2.rule
- rockyou-30000.rule
- Incisive-leetspeak.rule
- d3ad0ne.rule
- T0XlCv2.rule
- T0XlC_insert_HTML_entities_0_Z.rule
- generated.rule
- T0XlC-insert_00-99_1950-2050_toprules_0_F.rule
- unix-ninja-leetspeak.rule
- toggles5.rule
- InsidePro-HashManager.rule
- T0XlC.rule
- T0XlC-insert_top_100_passwords_1_G.rule
- InsidePro-PasswordsPro.rule
- toggles4.rule
- toggles3.rule
- T0XlC-insert_space_and_special_0_F.rule
- specific.rule
- oscommerce.rule
- T0XlC_3_rule.rule
- best64.rule
- combinator.rule
- toggles2.rule
- leetspeak.rule
- toggles1.rule

## Other ruleset to download

- OneRuletoRuleThemAll
- KoreLogic
- NSA Rules
- Hob0Rules


### Excercise 2e: Statistical Guessing Models ("Markov Attack")
Markov chains are statistical models trained on existing data. In this case the data are previous leaked passwords. We assume that leaked password are representative of passwords choosen by regular humans. The markov model identifies the most common patterns in *normal passwords*.

Hashcat comes with a pre-trained model, but we can train our own model if we have our own unique data or leaked passwords that we think represent the ones we want to crack.

The markov model simply creates mask patterns similar to what we saw in previous methods. It narrows down how many guesses we need to make. For short human created passwords, it is excellent and FAST. I usually try this up to 8 characters as a first or second attack. For long passwords or slow algorithms, other more advanced methods are better, but I will run this as my last attempt and let it run for a week or longer.

```
hashcat.bin -O -w 4 -a 3 -m 1000 --username lab1.txt
```

Everything up to 8 chars will take about 10 minutes

The next 9 chars will take 6 hours
The next 10 chars will take 10 days

## Section 3: Challenges

Now that you have learned a few of the standard techniques for automated password guessing with hashcat, you can challenge yourself in a little competition. How many points can you get in these challenges.

These represent realistic scenarios where password hashes need to be "cracked" by guessing passwords. Yes, you could build CRACKZILLA, a multiple GPU cracking cluster, or spend months of AWS EC2 time to brute-force the passwords. But if you apply some psychology you can priortize the most likely passwords first, and increase your chances of guessing more passwords FASTER.

How many passwords can you guess in an hour? That's the challenge. You won't be able to get them all. 

Should you go for challenges that give you the most points but might be harder? Or should you go for a challenge that lets you earn thousands of points for easy-to-guess passwords? You won't have enough time to go both.

Read these challenges and consider a strategy. If you are new, I suggest starting with the final challenge (NTLM Active Directory) and choosing any method you want. It will still be fun!

### Challenge 1: Due Diligence for Mergers and Aquisitions
You are a consultant hired by Federated Dundas who is planning a merger with Gardner Ross. Your bank has requested all records of existing obligations and opportunities Gardner Ross cited in their proposed valuation of the company. They claim they worth CAD$1.3 billion, but is that true? Rumors are circulating that some of their staff have shady dealings. The board of Federated Dundas wants to make sure they will not be acquring any undisclosed liabilities if the merger goes through.

You have obtained a large quantity of records of interest and they all check out. But there are are several files that are encrypted. The Gardner Ross employees claim they have no record of the passwords but that there is nothing of interest in them. You have been asked to "crack" the passwords on these files so they can be reviewed.

You know the names of the files and some of the concerns Federate Dundas has noted.

Files:
- 

Concerns:
- Is the Jarkata Harbour deal sound? We've heard that the buildings are too tall, and block light to the neighboring harbour causing aquatic plants to die out and subsquently endangering the wildlife in the harbour. The deal is dead if ecological reports were faudulent, or misrepsented. Jack Larkin leads this deal, and Doland Darby is supporting him. (If you crack the passwords of Jack or Donald in a later challenge, this file is considered cracked)
- Does Gardner Ross have the capital they claim? Word on the street is that Marty Stevens have incurred large losses on the trading floor, and that derivatives trader has made up for it *temporarily* but engaging in high-speed trading that gave Gardner Ross a temporary boost that was later lost. You need to get into the records for recent trades.
- Rumor has it that Marty Stevens is engaged in insider trading. He's been accused and recused many times. But rumor is that the phone records that he has been in contact with his nemisis McGrath at Federated Dundas. Are McGrath and Marty working in their own interests and against the interests of Gardner Ross and Federate Dundas (their respective employers)?!
- Ann Krywarick a market analyst and member of the trading floor was recently murdered. Jack Larkin suspects that their client, Private Security firm Obelisque (like Wagner but French) was involved. Gardner Ross is handling investments for Obelisque and Ann suspect they were laundering money to support wars, from which the profit, abroad. Federated Dundas does not mind having a global private security firm as a client, but wants nothing to do with mercanaries: too dangerous. Many of Ann's private files were encrypted. 

Challenge points are awarded for specific files:
- You need to crack Marty's phone records to see if he is insider trading. 100 points
- You need to crack any of Ann's private records: 200 points each
- You need to crack the deratives records: 100 points
- You need to crack the Jarkarta Harbour files OR crack Marty or Donald's accounts (later NTLM challenge): 100 points per file

### Challenge 2: Law Enforcement Forensics: The Crown vs Cedric Ross
Gardner Ross' founder, Cedric Ross was recently arrested and accused of fraud. His Daughter Sall Ross has taken over the company and wants to clear her father's good name. The RCMP have begun an investigation and Sally has turned over all of Cedric's personal computer files, but some of them are encrypted.

You work for a forensics firm hired by the RCMP to recover the encrypted data so that it can be examined. Sally hopes it will exonerate her father... the crown prosecutor... not so much.

For this challenge you earn 100 points if you can crack Cedrics locked file.

### Challenge 3: Insider Information: Hacking the Market Makers
You are a hacker hired by the Russian mafia. You are hired to modify documents created by famed stock market analyst Susanna Marks.

Susanna Marks is an analyst at Gardner Ross. She provides intelligence to the Trading Floor, the Merchant Banking deal makers, and publishes one of the most watched and values newsletters on Bay Street. Susanna has an incredible ability to predict which undervalued stocks are likely to make a break through. Everyone wants to know which stocks she will pick... if she picks a stock, everyone will buy it.

This has attacted the attention of the Russian mafia. They approached her with a bride, asking that she promote a worthless stock they control. If she promoted the stock, people would buy it, and the mafia could make a fortune selling it before it crashes. She refused. Then the mafia threatened her family. The mafia took pictures of her young son at school with his Dudley the Dragon stuffed animal hoping to intimidate her. She still refused. Gardner Ross hired bodyguards from security firm Obelisque and stuck by Susanna.

You must crack the password to Susanna's past and current analysis reports. If you can crack the most recent ones you can gain insight into which stocks she is promoting then the mafia can piggy back and make some quick cash. BUT if you can crack the unpublished report, you can alert it, and people will buy your junk stock, making your millions overnight and only Susanna will take the blame if regulators investigate.

For this challenge you get points based on which documents you crack:
- 10 points each for the first 5 reports of the year
- 20 points for the 2nd last report
- 1000 points for the most recent report

### Challenge 4: IT Audit: Password Assessment

In preparation for the planned merge of Gardner Ross and Federated Dundass, Sally Ross wants to provide evidence that their IT security is excellent. You are a consultant for a firm hired to conduct an audit of the IT systems used to handle their financial dealings.

Part of this audit involves assessing whether their passwords are strong enough. Their Active Directory GPO settings are currently good. But are the passwords really strong? 

You are given an extract of the NTLM hashes of all Active Directory passwords. You are most concerned about the password of privileged accounts: those with access to critical IT systems or senstive documents.

Guess as many AD account passwords as you can. For this challenge you get points based on the criticality of the accounts.
- 1 point per low
- 3 points per medium
- 5 points per high
- 10 points per critical
