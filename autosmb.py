import os, sys, getpass, subprocess

usrName = getpass.getuser()
passwd = ""
homeDir = subprocess.check_output(['echo', '~']).decode("utf-8")
configFile = "/etc/samba/smb.conf"
conffile = ""

def readFile(flname):
    with open(flname,mode='r') as f:
        return f.read()
def writeFile(flname, contents):
    with open(flname,mode='w') as f:
        f.write(contents)

print("Samba AutoConf v1 BETA")
print("Opening Configuration file...")

# Open Config
conffile = readFile(configFile)

def checkConf():
    os.system("testparm")
def restartSamba():
    os.system("sudo service smbd restart")
def setupUser():
    print("Enter Samba user password:")
    os.system("sudo smbpasswd -a "+usrName)
    print("Username: "+usrName)
def createShare():
    conffile = readFile(configFile)
    print("Create New file share\n\n")
    shrname = input("Share Name: ")
    shrpath = input("Share Path [auto adds ~ to start]: ")
    readonly = input("Share is read-only[yes/no]: ")
    guestok = input("Guest access ok[yes/no]: ")
    browsableok = input("Share is browsable[yes/no]: ")
    custommask = input("Custom file mask [leave blank for defaults]: ")
    if custommask=="":
        custommask="0755"
    os.system("mkdir "+os.path.join(homeDir, shrpath))
    writeFile(configFile,conffile+"""
[<folder_name>]
path = """+os.path.join(homeDir, shrpath)+"""
valid users = """+usrName+"""
read only = """+readonly+"""
browsable = """+browsableok+"""
guest ok = """+guestok+"""
create mask = """+custommask+"""
    """)
def backupdefault():
    os.system("mkdir "+os.path.join(homeDir,"AutoConf"))
    os.system("cp "+configFile+" "+os.path.join(homeDir,"AutoConf"))

def menuSelect():
    os.system("clear")
    print("\nWhat would you like to do? (Enter numbers from least to greatest to follow order)")
    print("1. Setup User")
    print("2. Backup Old Config")
    print("3. Create share")
    print("4. Restart Samba")
    print("5. Check Config file for errors")
    try:
        out = input("Option: ")
        if out<5:
            return out
        else:
            print("Invalid Option!")
    except ValueError:
        print("Invalid Option!")
    
while True:
    option = menuSelect()
    if option==1:
        setupUser()
    if option==2:
        backupdefault()
    if option==3:
        createShare()
    if option==4:
        restartSamba()
    if option==5:
        checkConf()
