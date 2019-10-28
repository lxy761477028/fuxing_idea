# coding: utf8
import os
import csv
import sys
import time
import config
import subprocess

from pydicom.dataset import Dataset
from pynetdicom import AE
from pynetdicom.sop_class import \
    PatientRootQueryRetrieveInformationModelFind, \
    StudyRootQueryRetrieveInformationModelFind, \
    PatientRootQueryRetrieveInformationModelMove, \
    StudyRootQueryRetrieveInformationModelMove


# Read CSV file and pick up Patient ID
# There is no unique format,
# we have to write special functions for doing this
def read_file(file, column):
    # Patient ID list
    patientList = []

    # Open file and read line by line
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=',')

        # Pick up data line by line
        for i, line in enumerate(reader):
            if i == 0: continue

            if len(line) > column:
                findVal = line[column]
                patientList.append(findVal)

    return patientList


# Query Study list by special parameters
def query_study(localAE, localPort, destIP, destAE, destPort,
                patientID, accessionNumber, studyInstanceUID, moodality, studyDateStart, studyDateEnd):
    # Prepare local information
    ae = AE(ae_title=localAE)
    ae.acse_timeout = 30

    # Add a requested presentation context
    ae.add_requested_context(StudyRootQueryRetrieveInformationModelFind)

    # Create local Identifier dataset
    ds = Dataset()
    ds.PatientName = ''
    ds.PatientID = patientID
    ds.StudyInstanceUID = studyInstanceUID
    ds.AccessionNumber = accessionNumber
    ds.Modality = moodality
    ds.StudyDate = studyDateStart + '-' + studyDateEnd
    ds.QueryRetrieveLevel = 'STUDY'

    # Associate with Peer
    assoc = ae.associate(destIP, destPort, ae_title=destAE)

    # Result list
    studyList = []

    if assoc.is_established:
        # Find information from Peer
        responses = assoc.send_c_find(ds, StudyRootQueryRetrieveInformationModelFind)

        # Check find result one by one
        for (status, identifier) in responses:
            if status:
                #print('C-FIND Status:0x{0:04x}'.format(status.Status))
                # Add result into list when status is pending or success
                if status.Status in (0xFF00, 0xFF01):
                    print('Pick up Study information: %s' % identifier.PatientID)
                    studyList.append(identifier)
            else:
                print('Connection timed out, was aborted or received invalid response')

        assoc.release()
    else:
        print('Association rejected, aborted or never connected')

    return studyList


# Move Study by study list
def move_study(localAE, localPort, destIP, destAE, destPort, study):
    # Prepare local information
    ae = AE(ae_title=localAE)
    ae.acse_timeout = 30

    # Add a requested presentation context
    ae.add_requested_context(StudyRootQueryRetrieveInformationModelMove)

    # Associate with Peer
    assoc = ae.associate(destIP, destPort, ae_title=destAE)

    if assoc.is_established:
        # Use the C-Move service to send identifier
        responses = assoc.send_c_move(study, localAE, StudyRootQueryRetrieveInformationModelMove)

        imageIndex = 1
        for (status, identifier) in responses:
            if status:
                # print('C-MOVE query status: 0x{0:04x}'.format(status.Status))
                if status.Status in (0xFF00, 0xFF01):
                    print('Imaging is being downloaded... %s' % imageIndex)
                    imageIndex += 1
                elif status.Status in (0x0000,):
                    print('Download is finished')

                    # Save study images into correct folder
                    folderName = study.PatientID + study.StudyInstanceUID
                    os.system("mkdir .\\images\\" + folderName)
                    os.system("move .\\rcv\\* .\\images\\" + folderName)
                    time.sleep(1)
                    print('Store study into %s' % folderName)

                    # Update task status
                    with open('tasks.txt', 'w') as f:
                        f.writelines(study.PatientID)
            else:
                print('Connection timed out, was aborted or received invalid response')

        # Release the association
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')


# This test have to work with office PACS environment
def test_demo():
    # Load config items
    localAE = config.dicom['localAE']
    localPort = config.dicom['localPort']
    destIP = config.dicom['destIP']
    destAE = config.dicom['destAE']
    destPort = config.dicom['destPort']

    # Import file configuration
    importFile = config.dicom['importFile']
    column = config.dicom['column']
    studyList = query_study(localAE, localPort, destIP, destAE, destPort,
                            '', '', '', 'CT', '20170101', '20181231')
    for study in studyList:
        print(study)
        move_study(localAE, localPort, destIP, destAE, destPort, study)


# Check saved task status
def check_task_status(patientIDList):
    taskList = []
    with open('tasks.txt', 'r') as f:
        taskList = f.read().splitlines()

    # Just remain the rest of task
    restList = list(set(patientIDList).difference(set(taskList)))

    return restList


# Main function
def main():
    # Load config items
    localAE = config.dicom['localAE']
    localPort = config.dicom['localPort']
    destIP = config.dicom['destIP']
    destAE = config.dicom['destAE']
    destPort = config.dicom['destPort']

    # Import file configuration
    importFile = config.dicom['importFile']
    column = config.dicom['column']

    # Start Store-SCP service
    storescpArgs = ['.\\dcm4che-3.3.8\\bin\\storescp.bat', '-b', localAE + ':' + str(localPort), '--directory', 'rcv',
                    '--sop-classes', '.\sop-classes.properties']
    print("Start storescp:")
    proc1 = subprocess.Popen(storescpArgs)

    # Read file and get PatientID
    patientIDList = read_file(importFile, column)

    # Check the status of last task
    patientIDList = check_task_status(patientIDList)

    # Query/Retrieve Studies
    for patientID in patientIDList:
        studyList = query_study(localAE, localPort, destIP, destAE, destPort,
                                patientID, '', '', 'CT', '20170101', '20181231')

        # Move Studies
        for study in studyList:
            print(study)
            move_study(localAE, localPort, destIP, destAE, destPort, study)

    proc1.kill()
    print('Move studies complete')

if __name__ == '__main__':
    #test_demo()
    main()
