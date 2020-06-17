#!/usr/bin/env python3
import pexpect
import re

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
makeimage_cmd = "/zap/firmadyne/scripts/makeImage.sh"
makeimage_args = ["--", makeimage_cmd, str(image_id), str(arch)]
child_im = pexpect.spawn("sudo", makeimage_args)
child_im.sendline(sudo_pass)
child_im.expect_exact(pexpect.EOF)

#infer Network
network_cmd = "/zap/firmadyne/scripts/inferNetwork.sh"
network_args = [str(image_id), str(arch)]

child = pexpect.spawn(network_cmd, network_args)
child.expect_exact("Interfaces:", timeout=None)
interfaces = child.readline().strip().decode("utf8")
print ("[+] Network interfaces:", interfaces)
child.expect_exact(pexpect.EOF)

IP = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', interfaces).group()

if len(interfaces) > 1:
    print("IP: ", IP)
    #TODO update database wih interface status
else:
    print("TODO: Add routine to shutdown docker container and update DB")
















