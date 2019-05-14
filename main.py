from optparse import OptionParser as parser
from database import *
pars = parser()
pars.add_option("-m","--mode",action='store',dest="mode",type="str",
help="Choosing one of the program's modes:\n- retrieve\n- registerKey\n- registerSite")
pars.add_option("-r","--random",action='store',dest="len",type="int",
help="Enable random password of length LEN generation for the site.")
pars.add_option("-s","--site",action='store',dest="site",type="str",
help="The site to be registered/retrieved in the database.")
pars.add_option("-u","--username",action='store',dest="username",type="str",
help="The username to be associated with the site.")
pars.add_option("-p","--password",action='store',dest="password",type="str",
help="The password to be associated with the site 'requires -m registerSite'.")
pars.add_option("-k","--key",action='store',dest="key",type="str",
help="The key to encrypt/decrypt the database's data.")
pars.add_option("-K","--Key",action='store',dest="Key",type="str",
help="The key to be registered in the database 'requires -m registerKey'.")
pars.add_option("-i","--initial",action="store_const",dest="initial",const=1,
help="An option to be used for creating a key first time (use -k option).")
(options, args) = pars.parse_args()
if not options.mode:
    print("\nError: An operating mode must be supplied")
if options.initial:
    with open("keys.db","w+") as file:
        Hash = sha512(options.key.encode()).hexdigest()
        file.write(Hash)
        file.close()
else:
    program = Database(options.key)
    if options.mode=="retrieve":
        print('\n'+'========================='+'\n'+program.retrieve(options.site))
    elif options.mode=="registerKey":
        program.registerKey(options.Key)
    elif options.mode=="registerSite":
        if options.len:
            program.registerSite(options.site,options.username,randPass=True,N=options.len)
        else:
            program.registerSite(options.site,options.username,password=options.password)
    else:
        print("\nError: Uknown mode.")
