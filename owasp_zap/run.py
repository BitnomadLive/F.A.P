import subprocess
outdir = "/home/thesis2020/Thesis/F.A.P1/Firmwares/netgear/WNAP/WNAP320"



owasp_zap_docker_cmd= 'docker run -it -p 8080:8080 --privileged -v "' + str(outdir) + '":/zap/firmadyne/images:ro -v "' +str(outdir) + "_report"  + '":/zap/firmadyne/scratch owasp_container_test '

print(owasp_zap_docker_cmd)
subprocess.check_call(owasp_zap_docker_cmd, shell=True)


#sollte jetzt alles ohne arch machbar sein da sql geupdated wurde

#firmadyne@bdbdd5a4595a:/zap/firmadyne$ export IMAGEID=`ls /zap/firmadyne/images/  | grep ".tar.gz" | grep -oE "\b[0-9]+\b"`

#firmadyne@bdbdd5a4595a:/zap/firmadyne$ export ARCHITECTURE = `/zap/firmadyne/scripts/getArch.sh /zap/firmadyne/images/$IMAGEID".tar.gz" | grep -oE 'armel|mipseb|mipsel'`


#firmadyne@0d8eba8d5127:/zap/firmadyne$ echo "firmadyne" | sudo -SE ./scripts/makeImage.sh 126 mipseb
#firmadyne@0d8eba8d5127:/zap/firmadyne$ ./scripts/inferNetwork.sh 126 mipseb | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" #should get IP
#firmadyne@0d8eba8d5127:/zap/firmadyne$ ./scratch/126/run.sh
#delete echo "firmadyne" | sudo -SE rm -r /scratch/126/image 
#delete echo "firmadyne" | sudo -SE /scratch/126/image.raw




#sudo ./zap-x.sh -daemon -host 0.0.0.0 -port 8080 -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true -config api.disablekey=true


#get all http request
#/JSON/core/view/sites/?zapapiformat=JSON&formMethod=GET

