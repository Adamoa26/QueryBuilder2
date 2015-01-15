import paramiko, getpass, os
from querybuilder.modules import logs

class SSHConnection:
    def __init__(self):
        '''
		# Constructor
		# This will intake directly from the emailparser class
		'''
        self.client = paramiko.SSHClient()

    def getsshinfo(self):
        """
	    # This method checks if the ssh.conf file is empty.
	    # If it is, it prompts user for ssh info.
	    # Else, it grabs the ssh info from the file.
	    :returns
	    [IP, User, Password]
	    """
        creds = [None] * 3
        dirpath = os.path.dirname(__file__)
        relativepath = "ssh.conf"
        absfilepath = os.path.join(dirpath, relativepath)
        try:
            file = open(absfilepath, 'r')
        except IOError:
            message = "There is no ssh.conf file or it won't open for writing."
            logs.exitGracefully(message)
        else:
            if os.stat(absfilepath).st_size == 0:
                self.configuressh()
            else:
                for i, line in enumerate(file):
                    if i == 0:
                        creds[0] = line.strip()
                    if i == 1:
                        creds[1] = line.strip()
                    if i == 2:
                        creds[2] = line.strip()
        return creds

    def getsshconfig(self):
        '''
	    # This method prompts for ssh info
	    :returns
	    [ip, Username, Password]
	    '''
        sshconfig = [None] * 3
        sshconfig[0] = str(raw_input("Remote IP address: "))
        sshconfig[1] = str(raw_input("Username: "))
        sshconfig[2] = str(getpass.getpass("Password: "))
        return sshconfig

    def configuressh(self):
        '''
	    # This method runs getsshconfig() and saves the results into ssh.conf in this format:
        # IP
	    # User
	    # Password
	    # ---End File---#
	    :returns
	    None
	    '''
        dirpath = os.path.dirname(__file__)
        relativepath = "ssh.conf"
        absfilepath = os.path.join(dirpath, relativepath)
        file1 = open(absfilepath, 'w')
        config = self.getsshconfig()
        for i in config:
            file1.writelines(i + "\n")

    def SSHConnect(self, command):
        '''
		Uses Paramiko to connect to remote server and execute the given command.
    	Returns command output

    	THIS IS THE ONLY METHOD YOU SHOULD NEED TO CALL FROM THIS CLASS.
    	IT RELIES ON ALL THE OTHERS TO FUNCTION, AND WILL HANDLE A FEW CONNECTIVITY ISSUES ON ITS OWN.

		:param command:
		:return:
		'''
        try:
            self.client.load_system_host_keys()
            sshinfo = self.getsshinfo()
            self.client.connect(sshinfo[0],             # Connects a shell to specified machine
                                username=sshinfo[1],    # and runs all the relevant commands for the search.
                                password=sshinfo[2])
            (sshin, sshout, ssherr) = self.client.exec_command(command)  # Executes command in remote shell.
            lines = sshout.readlines()  # Returns command output.
            self.client.close()  # Finally, it closes the self.client connection.
            return lines
        except paramiko.SSHException as e:
            logs.exitGracefully(e)