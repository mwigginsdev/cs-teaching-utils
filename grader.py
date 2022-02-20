import zipfile
import argparse
import os
from os.path import isfile, join
import shutil
import subprocess
import re


def runTest(dir):
    bashCommand = 'g++ ./tmp/test.cpp -o ./tmp/run --std=c++14'
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    bashCommand = './tmp/run'
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(error)
    print(output)
    return output.decode("utf-8")


def writeScore(zipName, score):
    with open("grades.csv", "a") as myfile:
        myfile.write(zipName + "," + score + ",\n")


def writeError(zipName, error, files):
    with open("errors.csv", "a") as myfile:
        myfile.write(zipName + "," + error + "," + files + ",\n")


workingDir = os.getcwd() + '/tmp'

print("Current working dir: " + workingDir)

parser = argparse.ArgumentParser(description='Process hw submissions')
parser.add_argument('path', help='path to folder of all hw zip files')
parser.add_argument('tester', help='path to tester file')

args = parser.parse_args()

print(os.getcwd() + '/grades.csv')
try:
    shutil.rmtree(os.getcwd() + 'grades.csv')
except:
    print("no grades file")


try:
    shutil.rmtree(os.getcwd() + '/errors.csv')
except:
    print("no errors file")


with open("grades.csv", "a") as myfile:
    myfile.write("name, score,\n")

with open("errors.csv", "a") as myfile:
    myfile.write("name, error,files,\n")

zips = os.listdir(args.path)

for zip in zips:
    print("PROCESSING: " + zip)
    if ".zip" in zip:
        try:
            with zipfile.ZipFile(args.path + '/' + zip, 'r') as zip_ref:
                os.mkdir(workingDir)
                zip_ref.extractall(workingDir)
                shutil.copy(args.tester, workingDir + '/test.cpp')
                workingContents = os.listdir(workingDir)
                print("WORKING CONTENTS: ", workingContents)
                for root, dirs, files in os.walk(workingDir, topdown=False):
                   for name in files:
                      if (name in ["List.h", "Queue.h", "Stack.h"] and root != workingDir):
                          shutil.copy(os.path.join(root, name), os.path.join(workingDir, name))

                workingContents = os.listdir(workingDir)
                output = runTest(workingDir)
                print(output)
                score = re.search("Tests: (.+?) out of 20", output)
                writeScore(zip, score.group(1))

        except Exception as e:
            print("error running: ", zip)
            print(e)
            print(os.listdir(workingDir))
            writeError(zip, str(e), str(os.listdir(workingDir)))

    try:
        shutil.rmtree(workingDir)
    except:
        print("missing workingDir")

print("**************ALL DONE**************")
