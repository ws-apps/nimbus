#!/usr/bin/env python

import pexpect
import sys
import os

to=int(os.environ["NIMBUS_TEST_TIMEOUT"])
tst_image_name = os.environ['NIMBUS_TEST_IMAGE']
tst_image_src = os.environ['NIMBUS_SOURCE_TEST_IMAGE']

cc_home=os.environ['CLOUD_CLIENT_HOME']
nimbus_home=os.environ['NIMBUS_HOME']
logfile = sys.stdout

try:
    os.mkdir("%s/history/vm-999" % (cc_home))
except:
    print "The directory already exists"
    pass

cmd = "%s/bin/cloud-client.sh --transfer --sourcefile %s" % (cc_home, tst_image_src)
(x, rc)=pexpect.run(cmd, withexitstatus=1)

cmd = "%s/bin/cloud-client.sh --run --name %s --hours .5" % (cc_home, tst_image_name)
child = pexpect.spawn (cmd, timeout=to, maxread=20000, logfile=logfile)
rc = child.expect ('Running:')
if rc != 0:
    print "%s not found in the list" % (tst_image_name)
    sys.exit(1)
handle = child.readline().strip().replace("'", "")
rc = child.expect(pexpect.EOF)
if rc != 0:
    print "run"
    sys.exit(1)

cmd = "%s/bin/nimbus-admin --debug --list" % (nimbus_home)
print cmd
(x, rc)=pexpect.run(cmd, withexitstatus=1)
print x

cmd = "%s/bin/nimbus-admin --batch --shutdown --all" % (nimbus_home)
print cmd
(x, rc)=pexpect.run(cmd, withexitstatus=1)
print x

cmd = "%s/bin/cloud-client.sh --delete --name %s" % (cc_home, tst_image_name)
(x, rc)=pexpect.run(cmd, withexitstatus=1)
sys.exit(0)
