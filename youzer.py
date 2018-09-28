#!/usr/bin/python3

import argparse
import sys
import random
import string

try:
    from faker import Factory
except:
    print("[!] Tool requires Faker library : pip install Faker")
import csv

def banner(version):
    banner = """


?88   d8P  d8888b ?88   d8Pd88888P  d8888b  88bd88b
d88   88  d8P' ?88d88   88    d8P' d8b_,dP  88P'  `
?8(  d88  88b  d88?8(  d88  d8P'   88b     d88
`?88P'?8b `?8888P'`?88P'?8bd88888P'`?888P'd88'
       )88
      ,d8P                            version : %s
   `?888P'

author  : @lorentzenman
team    : SpiderLabs

""" %version

    print(banner)


def create_user(fake, generated_usernames):
    firstname = fake.first_name()
    lastname = fake.last_name()
    name = firstname + " " + lastname
    username = firstname
    address = fake.address()
    if username in generated_usernames:
        username = username + lastname[0]
    generated_usernames.append(username)
    return firstname, lastname, username, name, address


def create_powershell_script(ou, output, domain):
    """writes the powershell importfile"""

    script ="""

$banner = @"
?88   d8P  d8888b ?88   d8Pd88888P  d8888b  88bd88b
d88   88  d8P' ?88d88   88    d8P' d8b_,dP  88P'  `
?8(  d88  88b  d88?8(  d88  d8P'   88b     d88
`?88P'?8b `?8888P'`?88P'?8bd88888P'`?888P'd88'
       )88
      ,d8P
   `?888P'

====================================================
"@
write-host $banner

$ErrorActionPreference = "SilentlyContinue"
$objOU=[ADSI]"LDAP://%s"
$dataSource = import-csv %s
foreach($dataRecord in $dataSource) {
    $givenName = $dataRecord.GivenName
    $sn = $dataRecord.sn
    $sAMAccountName = $givenName + '.' + $sn
    $userPrincipalName = $sAMAccountName + '@%s'
    $displayName = $dataRecord.Name
    $Password = $dataRecord.password
    $description = $dataRecord.description
    $cn = $dataRecord.Name
    # create object
    $objUser = $objOU.create("user", "CN="+ $cn)
    $objUser.Put("sAMAccountName",$sAMAccountName)
    $objUser.Put("userPrincipalName", $userPrincipalName)
    $objUser.Put("displayName",$displayName)
    $objUser.Put("givenName", $givenName)
    $objUser.Put("description", $description)
    $objUser.Put("sn",$sn)
    $objUser.SetInfo()
    $objUser.AccountDisabled = $false
    # in order to set the password the user needs to be commited
    $objUser.CommitChanges()
    $objUser.psbase.Invoke("SetPassword", $Password)
    $objUser.CommitChanges()
    write-host "Created User : $sAMAccountName"
    }""" % (ou,output,domain)

    powershell_script = output.replace(".csv", ".ps1")
    print("[!] Creating Powershell script for import : " + powershell_script)
    with open(powershell_script, "w") as ps:
        ps.write(script)

def Main():
    # program version
    version = 0.1
    banner(version)
    parser = argparse.ArgumentParser(description="Youzer :: Bulk Fake User Generator for Active Directory Environments")
    parser.add_argument("--generate", action="store_true", help="Generates random password string (upper, lower, number)")
    parser.add_argument("--generate_length", help="Length of generated password.")
    parser.add_argument("--ou", help="Base Organisational Unit (ou) : Example 'ou=users,dc=example,dc=com'", required=True)
    parser.add_argument("--domain", help='Specify Domain Name', required=True)
    parser.add_argument("--description", help="User Description", default="")
    parser.add_argument("--wordlist", help='Specify Wordlist for passwords')
    parser.add_argument("--mix", action="store_true", help='Mix both wordlist and password generation')
    parser.add_argument("--users", help='amount of users', required=True)
    parser.add_argument("--output", help='Path to CSV file output for AD import', required=True)
    parser.add_argument("--verbose", help='Prints users to screen - default is off', action="store_true", default=False)

    # counts the supplied number of arguments and prints help if they are missing
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()


    print("[-] Domain Name set to : " + args.domain)
    # faker object with locale
    fake = Factory.create('en_GB')
    password_options = []
    generated_usernames = []

    # wordlist settings
    if args.wordlist:
        wordlist = args.wordlist
        password_options.append("wordlist")
    if args.generate:
        generate_passwords = True
        password_options.append("generate")
    if args.generate_length:
        password_length = int(args.generate_length)
    else:
        password_length = 8

    # create output file header rows
    if not args.output.endswith(".csv"):
        args.output = args.output + ".csv"
    print("[*] Writing to output file : " + args.output)
    csv_file = open(args.output, 'w')
    writer = csv.writer(csv_file)
    writer.writerow(("Name", "GivenName", "sn", "ou", "password", "address", "description"))

    if args.mix != True and args.wordlist:

        with open(wordlist) as f:
            lines = f.readlines()
        print("[!] Generating %s users in wordlist mode" %args.users)
        for _ in range(0,int(args.users)):
            user = create_user(fake, generated_usernames)
            password = random.choice(lines).strip()
            writer.writerow((user[3], user[0], user[1], args.ou, password, args.description))
            if args.verbose:
                print(user, password)


    if args.mix == True:
        if not args.wordlist:
            print("[!] You need to pass a wordlist when using 'mix' mode")
            sys.exit(1)

        with open(wordlist) as f:
            lines = f.readlines()
        print("[!] Generating %s users in mix mode" %args.users)
        for _ in range(0,int(args.users)):
            user = create_user(fake, generated_usernames)
            if random.choice(password_options) == 'generate':
                password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(password_length))
            else:
                password = random.choice(lines).strip()
            writer.writerow((user[3], user[0], user[1], args.ou, password, args.description))
            if args.verbose:
                print(user, password)


    if args.generate == True:
        print("[!] Generating %s users in password generate mode" %args.users)
        for _ in range(0,int(args.users)):
            user = create_user(fake, generated_usernames)
            password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(password_length))
            writer.writerow((user[3], user[0], user[1], args.ou, password, args.description))
            if args.verbose:
                print(user, password)

    # check to close CSV file
    csv_file.close()

    #create powershell script
    create_powershell_script(args.ou, csv_file.name, args.domain)

if __name__ == "__main__":
    Main()
