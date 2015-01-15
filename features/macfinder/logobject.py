import re, datetime, pytz

class ConnLog:
    def __init__(self, logstring):
        newlog = logstring.strip()
        self.log = re.split('\s|\t', newlog)
        self.rawlog = newlog
        self.timestamp = float(self.log[0])
        self.uid = self.log[1]
        self.orig_h = self.log[2]
        self.orig_p = self.log[3]
        self.resp_h = self.log[4]
        self.resp_p = self.log[5]
        self.proto = self.log[6]
        self.service = self.log[7]
        self.duration = self.log[8]
        self.orig_bytes = self.log[9]
        self.resp_bytes = self.log[10]
        self.conn_state = self.log[11]
        self.local_orig = self.log[12]
        self.missed_bytes = self.log[13]
        self.history = self.log[14]
        self.orig_pkts = self.log[15]
        self.orig_ip_bytes = self.log[16]
        self.resp_pkts = self.log[17]
        self.resp_ip_bytes = self.log[18]
        self.tunnel_parents = self.log[19]
        self.orig_cc = self.log[20]
        self.resp_cc = self.log[21]

    def show_raw(self):
        print self.rawlog

    def get_raw(self):
        return self.rawlog

    def get_orig_h(self):
        return self.orig_h

    def get_orig_p(self):
        return self.orig_p

    def get_resp_h(self):
        return self.resp_h

    def get_resp_p(self):
        return self.resp_p
    
    def get_time(self):
        readtime = datetime.datetime.fromtimestamp(float(self.timestamp), tz=pytz.utc)
        return readtime

    def internal(self):
        if re.match(r"10\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", self.orig_h) is not None:
            return True
        else:
            return False

    def match_ip(self, ip):
        if self.orig_h == ip:
            return True
        else:
            return False
    
    def timeDifference(self, origTimestamp):
        diff = abs(float(self.timestamp) - float(origTimestamp))
        return int(diff)

    def find(self, searchtype, ip):
            if searchtype == "resp":
                assert ip is not None
                out = self.match_ip(ip)
            elif searchtype == "internal":
                out = self.internal()
            else:
                print searchtype + " is not a valid search type."
                return None
            return out

    def readabletimestamp(self):
        self.log[0] = datetime.datetime.fromtimestamp(self.timestamp, tz=pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
        return '    '.join(self.log)


class DHCPLog(ConnLog):
    def __init__(self, logstring):
        newlog = logstring.strip()
        self.log = re.split('\s|\t', newlog)
        self.rawlog = newlog
        self.timestamp = float(self.log[0])
        self.uid = self.log[1]
        self.orig_h = self.log[2]
        self.orig_p = self.log[3]
        self.resp_h = self.log[4]
        self.resp_p = self.log[5]
        self.mac = self.log[6]
        self.assigned_ip = self.log[7]
        self.lease_time = self.log[8]
        self.trans_id = self.log[9]

    def get_mac(self):
        return self.mac

    def get_assigned_ip(self):
        return self.assigned_ip

    def get_lease_time(self):
        return self.lease_time

    def get_trans_id(self):
        return self.trans_id

    def match_ip(self, ip):
        if self.assigned_ip == ip:
            return True
        else:
            return False

    def find(self, searchtype, ip):
        if searchtype == "mac":
            assert ip is not None
            out = self.match_ip(ip)
            return out
        else:
            print searchtype + " is not a valid search type."
            return None


#log1 = "1411256756.614964	C98UMG3l0MinSrqwf4	129.15.131.144	34412	50.23.91.81	48352	tcp	-1	12.163794	625	68	RSTR	F	0	ShADadr	6	949	6	380	(empty)	US	US	bro1-em2"
#log2 = "1411256756.614540	C6H4knllaiL242v4k	10.193.146.122	56426	50.23.91.81	48352	tcp	-1	12.164658	625	68	RSTR	T	0	ShADadr	24	3796	18	1140	(empty)	-1	US	bro6-em2"
#log3 = "1411255935.464448	CxdqcCwtDHeubsJea	10.193.146.122	68	10.193.128.1	67	3c:15:c2:e5:db:62	10.193.146.122	7200.000000	322391808"

#test1 = ConnLog(log1)
#test2 = ConnLog(log2)
#test3 = DHCPLog(log3)
#print test1.readabletimestamp()
#print test2.readabletimestamp()
#print test2.readabletimestamp()