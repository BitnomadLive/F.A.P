FROM owasp/zap2docker-stable

USER root
# Update packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y sudo

#Install git 
RUN apt-get install git

#install postgresql add this for final build
#RUN apt-get install postgresql

#Use FAT to install firmadyne
RUN git clone https://github.com/attify/firmware-analysis-toolkit.git

RUN ./firmware-analysis-toolkit/setup.sh


#Copy modified inferNetwork
#COPY inferNetwork.sh /zap/firmadyne/scripts/

#Copy modified makeImage
#COPY makeImage.sh /zap/firmadyne/scripts/

#Copy emulation python script
COPY start_emulation.py /zap/firmadyne/start_emulation.py

#install pexpect python module
#RUN sudo pip install pexpect

# Create firmadyne user
RUN useradd -m firmadyne
RUN echo "firmadyne:firmadyne" | chpasswd && adduser firmadyne sudo

USER firmadyne
CMD ["/bin/bash"]
