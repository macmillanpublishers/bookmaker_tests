import os
import shutil
import sys

import run_bkmkr_tests as runtests

if __name__ == '__main__':
    # # \/ Can set up to update valid files for a single testfile only too
    # if len(sys.argv) == 2:
    #     vfile = sys.argv[1]
    # else:
    #     vfile = None

    for filename in os.listdir(runtests.test_manuscript_dir):
        if os.path.splitext(filename)[1] == '.docx':
            no_ext_fname = os.path.splitext(filename)[0]
            new_validfiles_dir = os.path.join(runtests.tests_tmp_dir, 'verified_files', no_ext_fname)
            if os.path.isdir(new_validfiles_dir):
                # rm and recreate vfiledir in repo
                current_vfile_dir = os.path.join(runtests.current_validfiles_dir, no_ext_fname)
                runtests.rmExistingFSObject(current_vfile_dir)
                runtests.mkdir_p(current_vfile_dir)
                # copy files
                for vfile in os.listdir(new_validfiles_dir):
                    shutil.copyfile(os.path.join(new_validfiles_dir, vfile), os.path.join(current_vfile_dir, vfile))
