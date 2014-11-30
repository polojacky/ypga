from django.db import models
from formatChecker import ContentTypeRestrictedFileField

# DATABASE_CHOICES = (
#          ('genome','All Genome Sequences'),
#          ('gene','All Gene Sequences'),
#          ('protein','All Protein Sequences'),
#          ('draft','All Draft Sequences'),
# )
#
# ALIGNMENTS_CHOICES = (
#          ('10','10'),
#          ('50','50'),
#          ('100','100'),
#          ('250','250'),
#          ('500','500'),
#          ('1000','1000'),
#
# )
#
# EXPECT_CHOICES = (
#          ('0.0001','0.0001'),
#          ('0.01','0.001'),
#          ('1','1'),
#          ('10','10'),
#          ('100','100'),
#          ('1000','1000'),
# )
#
# MATRIX_CHOICES = (
#          ('PAM30','PAM30'),
#          ('PAM70','PAM70'),
#          ('BLOSUM80','BLOSUM80'),
#          ('BLOSUM62','BLOSUM62'),
#          ('BLOSUM45','BLOSUM45'),
# )

# Create your models here.
class blastModel(models.Model):
    querySeq = models.TextField(blank=True)
    queryFile = ContentTypeRestrictedFileField(upload_to='blast/queryFiles/', content_types=['text/plain',''],max_upload_size=1048576*20,blank=True, null=True)
    # database = models.CharField(max_length=20,choices=DATABASE_CHOICES)
    # alignments = models.CharField(max_length=20,choices=ALIGNMENTS_CHOICES)
    # expect = models.CharField(max_length=20,choices=EXPECT_CHOICES)
    # matrix = models.CharField(max_length=20,choices=MATRIX_CHOICES)
    # filterQuery = models.CharField(max_length=20)

class blastResultModel(models.Model):
    jobId = models.CharField(primary_key=True,max_length=40)
    status = models.CharField(max_length=20)  #status
    resultFile = models.CharField(max_length=255)  #result file path


