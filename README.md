# Overview
The purpose of this repo is to provide end-to-end testing of bookmaker content transforms for any test manuscript provided. It bypasses the flask_api now used to invoke bookmaker, but still uses a bookmaker_deploy toolchain ([bookmaker_test_direct.bat](https://github.com/macmillanpublishers/bookmaker_deploy/blob/master/bookmaker_test_direct.bat)) to manually invoke what is essentially a 'bookmaker_firstpass' run: plus one extra script ([bookmaker_tests.rb](https://github.com/macmillanpublishers/bookmaker_addons/blob/master/bookmaker_tests.rb)) to diff working html, xml, css & logfiles.

***

# Usage
## Run tests
To invoke the test, in cmd or Terminal window type: `python run_bkmkr_tests.py`.
That launches the tests via bookmaker_test_direct.bat for any manuscript (.docx) files in the 'test_manuscripts' folder. Tests run in parallel for each manuscript. It should all be done in < 30 min.  

## Review test results
#### Review diffs
Goto output folder to review test output for each/any testfile:
"S:\bookmaker_tmp\bookmaker_tests\test_tmpdir"
Each test manuscript will have its own folder. Inside each folder will be output from diffs, in a file: testoutput.txt. Review and make sure diffs reflect expected changes.
#### Look over actual output
Some layout changes will not be apparent in file diffs (particularly css/js changes). It's recommended that you visually inspect the new epub and the new pdf for any significant problems as well as expected changes. You can also run Acrobat's 'Compare Documents' to compare the new pdf to the verified one in greater detail.

## Update verified files
To update verified files to reflect your successful code updates (congrats!):
###### Update verified output for all test-files
+ run in cmd or Terminal window: `python update_valid_files.py`

###### Update verified output for a single file
+ for test-file dir folder in "S:\bookmaker_tmp\bookmaker_tests\verified_files\",  copy contents to their respective folders in 'bookmaker_tests\verified_files'

Then add, commit, and merge updated files.

***

# Add a new test manuscript
1. Put your new .docx test file in 'test_manuscripts' folder.
2. If there are any accompanying images or other input files (oneoff.css, config.json, override.js) for your test manuscript:  create a folder in 'test_manuscript' named after the docx filename sans extension, followed by: '__images_'.
  * Example: for file: test_ms.docx, create folder _test_ms_images_
3. Put all of the aforementioned accompanying files for your new test manuscript into the folder created in step 2.
4. Run the _run_bkmkr_tests.py_. Wait 5-10 minutes.
5. Go to "S:\bookmaker_tmp\bookmaker_tests\verified_files" and look for the folder matching your new testfile's name (sans .docx extension): it should be there, with 10 files inside.   
6. Copy that whole folder to 'bookmaker_tests\verified_files' folder
7. Run _run_bkmkr_tests.py_ again, and check file: "S:\bookmaker_tmp\bookmaker_tests\test_tmpdir\\*YOUR_TESTFILE_NAME*\testoutput.txt"
The file should show very few (if any) diffs.
8. Add, commit and push your files to the repo.

***

##### Notes for future development:
* add at least one RSuite styled manuscript as a test manuscript
* create .bat/.sh for updating verified files automatically
* create _run_bookmaker-test-direct_.sh for running tests in non-Windows env.
