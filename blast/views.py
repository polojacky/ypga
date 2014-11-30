from django_gearman import GearmanClient
from tools.views import blastResultModel

#called from the tools view
def callBlast(queryFile, database, resultFile, num_alignments, num_descriptions, expect,max_target_seqs,jobId):

    client = GearmanClient()
    result = client.submit_job("runBlast",background=True,
                              kwargs={"queryFile": queryFile, "database": database, "resultFile": resultFile,
                                      "num_alignments": num_alignments,"num_descriptions":num_descriptions,
                                      "expect":expect,'max_target_seqs':max_target_seqs,'jobId':jobId})

    print result.state
    # record the job id in the model blastresult
    job = blastResultModel(jobId=jobId,status=result.state,resultFile=resultFile)
    job.save()
    print result