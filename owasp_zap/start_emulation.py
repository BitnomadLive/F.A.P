#!/usr/bin/env python3
import pexpect
import re
import os

sudo_pass = "firmadyne"

#Image ID
child_iid = pexpect.spawn('/bin/sh -c "ls /zap/firmadyne/images/  | grep ".tar.gz" | grep -oE \"[0-9]+\""')
image_id = child_iid.readline().strip().decode("utf8")
print("IID: ",image_id)

#Architecture
child_arch = pexpect.spawn('/bin/sh -c "/zap/firmadyne/scripts/getArch.sh /zap/firmadyne/images/' +str(image_id) +'.tar.gz | grep -oE \'armel|mipseb|mipsel\' "')
arch = child_arch.readline().strip().decode("utf-8")
print("ARCH: ", arch)

#make Image
print("make Image")
makeimage_cmd = "/zap/firmadyne/scripts/makeImage.sh"
makeimage_args = ["--", makeimage_cmd, str(image_id), str(arch)]
child_im = pexpect.spawn("sudo", makeimage_args)
child_im.sendline(sudo_pass)
child_im.expect_exact(pexpect.EOF)

#infer Network
print("infer Network")
network_cmd = "/zap/firmadyne/scripts/inferNetwork.sh"
network_args = [str(image_id), str(arch)]

child = pexpect.spawn(network_cmd, network_args)
child.expect_exact("Interfaces:", timeout=None)
interfaces = child.readline().strip().decode("utf8")
print ("[+] Network interfaces:", interfaces)
child.expect_exact(pexpect.EOF)



if len(interfaces) > 3:
    #TODO update database wih interface status
    IP = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', interfaces).group()
    print("IP: ", IP)
else:
    print("TODO: Add routine to shutdown docker container and update DB")


#run emulation
runsh_path = "/zap/firmadyne/scratch/" + str(image_id) + "/run.sh"
if not os.path.isfile(runsh_path):
    print ("[!] Cannot emulate firmware, run.sh not generated")
    #return  #write to database
run_cmd = ["--", runsh_path]
child = pexpect.spawn("sudo", run_cmd)
child.sendline(sudo_pass)
child.interact()














