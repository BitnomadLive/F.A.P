import os
import psycopg2
import subprocess
import traceback



firmware_folder="/home/thesis2020/Thesis/F.A.P/Firmwares/"
sql = "172.17.0.1"


def create_output_folder(subdir, file):
    #creating output folders for firmadyne extraction docker image
    #print("File: ")

    file_without_extension = os.path.splitext(file)[0]
    folder_to_create = subdir + "/" + file_without_extension
     
    if not os.path.exists(folder_to_create):
        os.makedirs(folder_to_create)
        os.makedirs(folder_to_create + "_tar_extracted")
    
    #try:
    #    os.rmdir(folder_to_create)
    #except:
    #    print("error")

    #try:
    #    os.rmdir(folder_to_create + "_tar_extracted")
    #except:
    #    print("error2")

def get_brand(subdir, file):
    #returns brand name based on position in file path
    path = os.path.join(subdir, file)
    f_list = path.split('/')
    return f_list[6]


def run_extraction_dockerimage(subdir, file):
    #TODO run extract.sh with correct parameters
    # set tar_extracted field in database
    # see database TODO
    file_path = os.path.join(subdir, file)
    file_without_extension = os.path.splitext(file)[0]
    outdir_folder = subdir + "/" + file_without_extension  #filepath wher .tar.gz ends up in
   
   
    #TODO call extraction docker image
    subprocess.check_call('./extractor/extract.sh "%s" "%s" %s %s' % (str(file_path), str(outdir_folder), str(get_brand(subdir, file)),str(sql)),   shell=True)
    
    #get firmware id 
    firmware_id = ""
    for subdir, dirs, files in os.walk(outdir_folder):
        if len(files) > 0:
            for file in files:
                if os.path.splitext(file)[1] == ".gz":
                    firmware_id = os.path.splitext(os.path.splitext(file)[0])[0]
  

    if firmware_id != "":
    
        database = psycopg2.connect(database="firmware",
                                     user="firmadyne",
                                     password="firmadyne",
                                     host=sql)


        #write to databse, set tar_Extracted field
        try:
            cur = database.cursor()
            cur.execute("UPDATE image SET tar_extracted='True' WHERE id=%s", (firmware_id, ) )          #get id from extraction folder
            database.commit()
        except BaseException:
            ret = False
            traceback.print_exc()
            database.rollback()
        finally:
            if cur:
                cur.close()

        #getArch with outdir_folder + firmaware_id + ".tar.gz" (.tar.gz file)
        subprocess.check_call('./getArch/getArch.sh "%s" "%s"' % (str(outdir_folder + "/" +firmware_id + ".tar.gz"), str(sql)),   shell=True)
        

        #TODO add tar2db stuff here
        #add path to schema for extracted firmware folder
        #add path to unextracted firmware file
        #add path to schema for every file  (check if multiple entries for same file are done based on firmaware image id )
        print("Running tar2db")
        tar2db_docker_cmd= 'docker run -it   -v "' + str(outdir_folder) + '":/firmware-in:ro tar2db -i ' + str(firmware_id) +  " -f /firmware-in/" + str(firmware_id) + ".tar.gz"
        subprocess.check_call(tar2db_docker_cmd, shell=True)
        print("Finished tar2db")

        

    print("======================")










#Script starts here
file_list = []
dir_list = []


    #TODO: make sure there is no space in the name
    #see documentationh for bash oneliner -> probably best to create a .sh file for it



all_file_counter = 0
for subdir, dirs, files in os.walk(firmware_folder):
    for file in files:
        #makes sure to skip hidden files
        if file.startswith('.'):
            #print("starts with dot")
            continue
        #print(os.path.join(subdir, file))
        file_list.append(file)
        dir_list.append(subdir)
        all_file_counter = all_file_counter + 1


counter = 0

for file in file_list:
    file_path = os.path.join(subdir, file)
    subdir = dir_list[counter]
    print(file_path)
    print(get_brand(subdir, file))
    #filename=pf_list[-1]
    create_output_folder(subdir, file)
    run_extraction_dockerimage(subdir, file)
    counter = counter + 1     
    print( str(counter) + "/" + str(all_file_counter) + "\n")




