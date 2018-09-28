# youzer
Fake User Generator for Active Directory Environments

## Introduction

The goal of Youzer is to create information rich Active Directory environments.
This uses the python3 library 'faker' to generate random accounts. 
```
pip3 install faker
```

You can either supply a wordlist or have the passwords generated. The generated option is great for testing things like hashcat rule masks. Wordlist option is useful when wanting to supply a specific password list seeded into an environment, or to practice dictionary attacks.

The output is a CSV and a PowerShell script where both can be copied to the target. When executed, the PowerShell script binds over LDAP so doesn't rely on the newer Active Directory modules and creates each user object. Currently the OU's need to exist, but this tool is a sub-project of 'Labseed' where the Active Directory structure will be created.

### RoadMap

* Generate multiple departments (OU's)
* Generate grouping structure and randomly assign
* Implement additional Faker object options to populate other LDAP fields such as Address, Region
* Create an organisational chart of the nested grouping structure


# Examples

Youzer can create 100,000 users in under 30 seconds and 1,000,000 users in around 3 minutes.

```
[-] Domain Name set to : example
[*] Writing to output file : sales_example.csv
[!] Generating 100000 users in password generate mode
[!] Creating Powershell script for import : sales_example.ps1
python3 youzer.py --generate --generate_length 20 --ou  --domain example      20.35s user 0.11s system 95% cpu 21.354 total
```

### Creating 1000 user accounts with a randomly generated alphanumeric password choice of 20 characters

```
python3 youzer.py --generate --generate_length 20 --ou "ou=sales,dc=example,dc=domain" --domain example --users 1000 --output sales_example.csv



?88   d8P  d8888b ?88   d8Pd88888P  d8888b  88bd88b
d88   88  d8P' ?88d88   88    d8P' d8b_,dP  88P'  `
?8(  d88  88b  d88?8(  d88  d8P'   88b     d88
`?88P'?8b `?8888P'`?88P'?8bd88888P'`?888P'd88'
       )88
      ,d8P                            version : 0.1
   `?888P'

author  : @lorentzenman
team    : SpiderLabs


[-] Domain Name set to : example
[*] Writing to output file : sales_example.csv
[!] Generating 1000 users in password generate mode
[!] Creating Powershell script for import : sales_example.ps1

```

Sample output from CSV file created from generate option

```
Name,GivenName,sn,ou,password,address,description
Dennis Shaw,Dennis,Shaw,"ou=sales,dc=example,dc=domain",VwVeloi09FaECRdNbbXD,
Sam Francis,Sam,Francis,"ou=sales,dc=example,dc=domain",qhitxgjDW4gZFuraLJbB,
Ellie Freeman,Ellie,Freeman,"ou=sales,dc=example,dc=domain",7qbLcknqlPtpkOzdLyw3,
Terence Arnold,Terence,Arnold,"ou=sales,dc=example,dc=domain",lumPMbDk1YomypRj26by,
Anne Murphy,Anne,Murphy,"ou=sales,dc=example,dc=domain",6r42EGGoEJYe9PydHRTV,
Wendy Smith,Wendy,Smith,"ou=sales,dc=example,dc=domain",tKI2zFUOU8XdK4ZTUJas,
Jay Lyons,Jay,Lyons,"ou=sales,dc=example,dc=domain",wxEIbw18tW9uFYXtMI9H,
Jonathan White,Jonathan,White,"ou=sales,dc=example,dc=domain",caoHcm2Y90lIH7zskJYr,
Adam Roberts,Adam,Roberts,"ou=sales,dc=example,dc=domain",Qu0y7mlb2haQQddxYrcN,
Georgina Jones,Georgina,Jones,"ou=sales,dc=example,dc=domain",rYBjxs4tpj9Qza7HcKYI,
Lee Newton,Lee,Newton,"ou=sales,dc=example,dc=domain",6CVlBvEutc3Ahco2UI5q,
Aaron Smith,Aaron,Smith,"ou=sales,dc=example,dc=domain",hmSSoKILfvrHuHbPTDIQ,
Max Hall,Max,Hall,"ou=sales,dc=example,dc=domain",11Ys9Zdk2M8J1JAScBkP,
Kimberley Douglas,Kimberley,Douglas,"ou=sales,dc=example,dc=domain",WQ9285gSHv2MXkwoLYlg,
Denise Fisher,Denise,Fisher,"ou=sales,dc=example,dc=domain",CT1pbfAnCoezuyrJbQX9,

```




### Creating 1000 user accounts from a source word list

```
python3 youzer.py --wordlist ~/tools/pw/Probable-Wordlists/Real-Passwords/Top12Thousand-probable-v2.txt --ou "ou=IT,dc=example,dc=domain" --domain example --users 1000 --output IT_example.csv 



?88   d8P  d8888b ?88   d8Pd88888P  d8888b  88bd88b
d88   88  d8P' ?88d88   88    d8P' d8b_,dP  88P'  `
?8(  d88  88b  d88?8(  d88  d8P'   88b     d88
`?88P'?8b `?8888P'`?88P'?8bd88888P'`?888P'd88'
       )88
      ,d8P                            version : 0.1
   `?888P'

author  : @lorentzenman
team    : SpiderLabs


[-] Domain Name set to : example
[*] Writing to output file : IT_example.csv
[!] Generating 1000 users in wordlist mode
[!] Creating Powershell script for import : IT_example.ps1

```

Sample output of CSV file from above wordlist option

```
Name,GivenName,sn,ou,password,address,description
Rhys Parker,Rhys,Parker,"ou=IT,dc=example,dc=domain",houston,
Geoffrey Harris,Geoffrey,Harris,"ou=IT,dc=example,dc=domain",clothing,
Georgia Davis,Georgia,Davis,"ou=IT,dc=example,dc=domain",spotty,
Gemma Norris,Gemma,Norris,"ou=IT,dc=example,dc=domain",brendan1,
Daniel Marsh,Daniel,Marsh,"ou=IT,dc=example,dc=domain",pauline,
Dominic Harvey,Dominic,Harvey,"ou=IT,dc=example,dc=domain",devin,
Teresa Stokes,Teresa,Stokes,"ou=IT,dc=example,dc=domain",snapple,
Joanna Morgan,Joanna,Morgan,"ou=IT,dc=example,dc=domain",volcom,
Oliver Middleton,Oliver,Middleton,"ou=IT,dc=example,dc=domain",master,

```
