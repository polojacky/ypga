"""
Gearman Job File.
Needs to be called gearman_jobs.py
"""

import os
import time
#import subprocess
from tools.views import blastResultModel

from ypga.settings import BLAST_DIR
from django_gearman.decorators import gearman_job



#blast job
@gearman_job(name='runBlast', queue="blastQueue")
def runBlast(queryFile, database, resultFile, num_alignments, num_descriptions, expect,max_target_seqs,jobId):
    db = BLAST_DIR + r'/database/' + database
    cmd_line = 'blastn -query ' + queryFile + ' -out ' + resultFile + ' -db ' + db + ' -max_target_seqs ' + max_target_seqs+' -evalue '+expect +' -outfmt 6'
    # proc = subprocess.Popen(args=cmd_line)
    # returncode = proc.wait()
    os.system(cmd_line)
    if os.path.isfile(resultFile):
        # record the job id in the model blastresult
        blastResultModel.objects.filter(jobId=jobId).update(status='COMPLETE')

@gearman_job
def reverse(input):
    """Reverse a string"""
    print "[%s] Reversing string: %s" % (os.getpid(), input)
    return input[::-1]


@gearman_job
def background_counting(arg=None):
    """
    Do some incredibly useful counting to 5
    Takes no arguments, returns nothing to the caller.
    """
    print "[%s] Counting from 1 to 5." % os.getpid()
    for i in range(1, 6):
        print i
        time.sleep(1)

