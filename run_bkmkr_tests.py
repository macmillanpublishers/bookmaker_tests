import os
import shutil
import inspect
import sys
import traceback
import subprocess
import platform, getpass
import multiprocessing
from datetime import datetime

#########################   DECLARATIONS
hostOS = platform.system()
currentuser = getpass.getuser()
test_repo_name = 'bookmaker_tests'
#  set per OS paths & batch filetype
if hostOS == "Windows":
    bookmaker_tmp_dir = os.path.join('S:', os.sep, 'bookmaker_tmp')
    bookmaker_repos_dir = os.path.join('S:', os.sep, 'resources', 'bookmaker_scripts')
    test_direct_ext = 'bat'
else:
    bookmaker_tmp_dir = os.path.join(os.sep, 'Users', currentuser, 'bookmaker_tmp')
    bookmaker_repos_dir = os.path.join(os.sep, 'Users', currentuser, 'bookmaker-dev')
    test_direct_ext = 'sh'
# key paths
tests_tmp_dir = os.path.join(bookmaker_tmp_dir, test_repo_name)
test_manuscript_dir = os.path.join(bookmaker_repos_dir, test_repo_name, 'test_manuscripts')
current_validfiles_dir = os.path.join(bookmaker_repos_dir, test_repo_name, 'verified_files')
test_bat = os.path.join(bookmaker_repos_dir, 'bookmaker_deploy', 'bookmaker_test_direct.{}'.format(test_direct_ext))

#########################   METHODS

def mkdir_p(path):
    try:
        os.makedirs(path)
    except:
        if os.path.isdir(path):
            pass
        else:
            raise

def rmExistingFSObject(path):
    if os.path.exists(path):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except Exception as e:
            errstring = 'Error during "{}", exiting'.format(inspect.stack()[0][3])
            print(errstring, e.message, e.args)
            traceback.print_exc()
            sys.exit(1)

def runtest(file):
    try:
        args = [test_bat, file, 'direct', "", ""]
        result = subprocess.check_output(args)
        # result = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # output,error = result.communicate()
        # print (output)
    except Exception as e:
        errstring = 'Error during "{}", exiting'.format(inspect.stack()[0][3])
        print(errstring, e.message, e.args)
        traceback.print_exc()
        sys.exit(1)

def kickoffTestforFile(testfile):
    # setup
    filename = os.path.basename(testfile)
    print ("starting tests for {}, at {}".format(filename, datetime.now()))
    no_ext_basename = os.path.splitext(filename)[0]
    test_tmpdir = os.path.join(tests_tmp_dir, no_ext_basename)
    # rm existing dir
    rmExistingFSObject(test_tmpdir)
    # (re-)make dir and copy flie to tmp
    mkdir_p(test_tmpdir)
    shutil.copyfile(testfile, os.path.join(test_tmpdir, filename))
    # copy images to tmp`
    imagesdir = os.path.join(test_manuscript_dir, '{}_images'.format(no_ext_basename))
    if os.path.isdir(imagesdir):
        sf_dir = os.path.join(test_tmpdir, 'submitted_files')
        # mkdir_p(sf_dir)
        shutil.copytree(imagesdir, sf_dir)
    runtest(os.path.join(test_tmpdir, filename))
    print ("finished tests for {}, at {}".format(filename, datetime.now()))


#########################   MAIN

if __name__ == '__main__':
    # 'freeze_support' required for multprocessing in Windows
    multiprocessing.freeze_support()

    # setup
    mkdir_p(tests_tmp_dir)
    testfiles = []

    for filename in os.listdir(test_manuscript_dir):
        testfile = os.path.join(test_manuscript_dir, filename)
        if not os.path.isdir(testfile):
            # kickoffTestforFile(testfile)
            testfiles.append(testfile)


    p = multiprocessing.Pool()
    p.map(kickoffTestforFile, testfiles)
