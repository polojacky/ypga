# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from __future__ import unicode_literals

from django.db import models

class Allele(models.Model):
    id_uuid = models.CharField(primary_key=True, max_length=80)
    type = models.CharField(max_length=20)
    genomerefno1 = models.CharField(db_column='genomeRefNo1', max_length=20) # Field name made lowercase.
    strain1 = models.CharField(max_length=20, blank=True)
    locus1 = models.CharField(max_length=80)
    genomerefno2 = models.CharField(db_column='genomeRefNo2', max_length=20, blank=True) # Field name made lowercase.
    strain2 = models.CharField(max_length=20, blank=True)
    locus2 = models.CharField(max_length=80, blank=True)
    allelelist = models.TextField(db_column='alleleList', blank=True) # Field name made lowercase.
    alleletypeno = models.CharField(db_column='alleleTypeNo', max_length=20, blank=True) # Field name made lowercase.
    totalallelenum = models.CharField(db_column='totalAlleleNum', max_length=20, blank=True) # Field name made lowercase.
    source = models.CharField(max_length=1000, blank=True)
    method = models.CharField(max_length=60, blank=True)
    description = models.CharField(max_length=500, blank=True)
    other = models.CharField(max_length=1000, blank=True)
    class Meta:
        managed = False
        db_table = 'allele'

class AlleleStatistics(models.Model):
    id_uuid = models.CharField(primary_key=True, max_length=80)
    genomerefno = models.CharField(db_column='genomeRefNo', max_length=20) # Field name made lowercase.
    strain = models.CharField(max_length=20, blank=True)
    locus = models.CharField(max_length=80)
    allelelist = models.CharField(db_column='alleleList', max_length=1000, blank=True) # Field name made lowercase.
    alleletypeno = models.CharField(db_column='alleleTypeNo', max_length=20, blank=True) # Field name made lowercase.
    source = models.TextField(blank=True)
    method = models.CharField(max_length=60, blank=True)
    description = models.CharField(max_length=500, blank=True)
    other = models.CharField(max_length=1000, blank=True)
    class Meta:
        managed = False
        db_table = 'allele_statistics'

class Fragment(models.Model):
    id = models.CharField(primary_key=True, max_length=80)
    locus = models.CharField(max_length=40, blank=True)
    gino = models.CharField(db_column='giNo', max_length=80, blank=True) # Field name made lowercase.
    type = models.CharField(max_length=20, blank=True)
    genomerefno = models.CharField(db_column='genomeRefNo', max_length=20) # Field name made lowercase.
    strain = models.CharField(max_length=20, blank=True)
    geneid = models.CharField(db_column='geneId', max_length=20, blank=True) # Field name made lowercase.
    genename = models.CharField(db_column='geneName', max_length=20, blank=True) # Field name made lowercase.
    startpos = models.IntegerField(db_column='startPos') # Field name made lowercase.
    endpos = models.IntegerField(db_column='endPos') # Field name made lowercase.
    strand = models.CharField(max_length=4)
    length = models.IntegerField(blank=True, null=True)
    pid = models.CharField(max_length=20, blank=True)
    cogno = models.CharField(db_column='cogNo', max_length=20, blank=True) # Field name made lowercase.
    product = models.CharField(max_length=200, blank=True)
    source = models.TextField(blank=True)
    method = models.CharField(max_length=60, blank=True)
    upstreamgenelocus = models.CharField(db_column='upstreamGeneLocus', max_length=20, blank=True) # Field name made lowercase.
    downstreamgenelocus = models.CharField(db_column='downstreamGeneLocus', max_length=20, blank=True) # Field name made lowercase.
    other = models.CharField(max_length=1000, blank=True)
    seq = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'fragment'


class Genome(models.Model):
    genomerefno = models.CharField(db_column='genomeRefNo', primary_key=True, max_length=100) # Field name made lowercase.
    genometype = models.CharField(db_column='genomeType', max_length=20) # Field name made lowercase.
    genenum = models.IntegerField(db_column='geneNum', blank=True, null=True) # Field name made lowercase.
    gino = models.CharField(db_column='giNo', max_length=20, blank=True) # Field name made lowercase.
    uidno = models.CharField(db_column='uidNo', max_length=20, blank=True) # Field name made lowercase.
    genomename = models.CharField(db_column='genomeName', max_length=60) # Field name made lowercase.
    definition = models.CharField(max_length=200, blank=True)
    length = models.IntegerField()
    type = models.CharField(max_length=20, blank=True)
    biovar = models.CharField(max_length=20, blank=True)
    strain = models.CharField(max_length=20, blank=True)
    updatetime = models.CharField(db_column='updateTime', max_length=20, blank=True) # Field name made lowercase.
    reference = models.TextField(blank=True)
    source = models.CharField(max_length=60, blank=True)
    other = models.CharField(max_length=1000, blank=True)
    seq = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'genome'

class Homology(models.Model):
    id = models.CharField(primary_key=True, max_length=80)
    genomerefno = models.CharField(db_column='genomeRefNo', max_length=20, blank=True) # Field name made lowercase.
    strain = models.CharField(max_length=20, blank=True)
    type = models.CharField(max_length=20)
    locus = models.CharField(max_length=20, blank=True)
    homotype = models.CharField(db_column='homoType', max_length=20) # Field name made lowercase.
    homolist = models.TextField(db_column='homoList', blank=True) # Field name made lowercase.
    homolistnum = models.CharField(db_column='homoListNum', max_length=4, blank=True) # Field name made lowercase.
    orthologylist = models.TextField(db_column='orthologyList', blank=True) # Field name made lowercase.
    orthologylistnum = models.CharField(db_column='orthologyListNum', max_length=4, blank=True) # Field name made lowercase.
    paralogylist = models.TextField(db_column='paralogyList', blank=True) # Field name made lowercase.
    paralogylistnum = models.CharField(db_column='paralogyListNum', max_length=4, blank=True) # Field name made lowercase.
    source = models.TextField(blank=True)
    method = models.CharField(max_length=60, blank=True)
    description = models.CharField(max_length=500, blank=True)
    other = models.CharField(max_length=1000, blank=True)
    class Meta:
        managed = False
        db_table = 'homology'

class Protein(models.Model):
    id_uuid = models.CharField(primary_key=True, max_length=80)
    id_fragment = models.CharField(max_length=80)
    genomerefno = models.CharField(db_column='genomeRefNo', max_length=20, blank=True) # Field name made lowercase.
    strain = models.CharField(max_length=20, blank=True)
    locus = models.CharField(max_length=20, blank=True)
    pid = models.CharField(max_length=20, blank=True)
    refseqno = models.CharField(db_column='refseqNo', max_length=20, blank=True) # Field name made lowercase.
    length = models.IntegerField(blank=True, null=True)
    lib_name = models.CharField(max_length=20, blank=True)
    accessory_cogno = models.CharField(db_column='accessory_cogNo', max_length=20, blank=True) # Field name made lowercase.
    description_product = models.CharField(max_length=1000, blank=True)
    entry_accessory = models.CharField(max_length=20, blank=True)
    entry_description = models.CharField(max_length=100, blank=True)
    go_id_list = models.CharField(max_length=1000, blank=True)
    pathway_id_list = models.CharField(max_length=2000, blank=True)
    source = models.TextField(blank=True)
    method = models.CharField(max_length=60, blank=True)
    other = models.CharField(max_length=1000, blank=True)
    seq = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'protein'

class Reanno(models.Model):
    id_uuid = models.CharField(primary_key=True, max_length=80)
    id = models.CharField(max_length=80)
    type = models.CharField(max_length=80)
    id_original = models.CharField(max_length=80, blank=True)
    genomerefno = models.CharField(db_column='genomeRefNo', max_length=20) # Field name made lowercase.
    strain = models.CharField(max_length=20, blank=True)
    startpos = models.IntegerField(db_column='startPos') # Field name made lowercase.
    endpos = models.IntegerField(db_column='endPos') # Field name made lowercase.
    strand = models.CharField(max_length=4)
    length = models.IntegerField(blank=True, null=True)
    startpos_original = models.IntegerField(db_column='startPos_original', blank=True, null=True) # Field name made lowercase.
    endpos_original = models.IntegerField(db_column='endPos_original', blank=True, null=True) # Field name made lowercase.
    strand_original = models.CharField(max_length=4, blank=True)
    length_original = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=200, blank=True)
    method = models.CharField(max_length=60, blank=True)
    description = models.TextField(blank=True)
    other = models.CharField(max_length=1000, blank=True)
    class Meta:
        managed = False
        db_table = 'reanno'
    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.id_uuid)+" "+self.id_original;

class Repeat(models.Model):
    id_uuid = models.CharField(primary_key=True, max_length=80)
    id = models.CharField(max_length=80)
    type = models.CharField(max_length=80)
    id_original = models.CharField(max_length=80, blank=True)
    genomerefno = models.CharField(db_column='genomeRefNo', max_length=20) # Field name made lowercase.
    strain = models.CharField(max_length=20, blank=True)
    startpos = models.IntegerField(db_column='startPos') # Field name made lowercase.
    endpos = models.IntegerField(db_column='endPos') # Field name made lowercase.
    strand = models.CharField(max_length=4)
    length = models.IntegerField(blank=True, null=True)
    source = models.TextField(blank=True)
    method = models.CharField(max_length=60, blank=True)
    description = models.CharField(max_length=500, blank=True)
    ref_seq = models.TextField(blank=True)
    other = models.CharField(max_length=1000, blank=True)
    class Meta:
        managed = False
        db_table = 'repeat'

class ExpressionProfile(models.Model):
    locus = models.CharField(primary_key=True, max_length=20)
    genomerefno = models.CharField(db_column='genomeRefNo', max_length=20, blank=True) # Field name made lowercase.
    strain = models.CharField(max_length=20, blank=True)
    genename = models.CharField(db_column='geneName', max_length=60, blank=True) # Field name made lowercase.
    classnum = models.CharField(db_column='classNum', max_length=20, blank=True) # Field name made lowercase.
    number_37_vs_26celsius = models.CharField(db_column='37_vs_26celsius', max_length=18, blank=True) # Field renamed because it wasn't a valid Python identifier.
    cold_shock = models.CharField(max_length=18, blank=True)
    heat_shock = models.CharField(max_length=18, blank=True)
    high_salt = models.CharField(max_length=18, blank=True)
    high_osmolarity = models.CharField(max_length=18, blank=True)
    ompr_mutant_hs = models.CharField(db_column='ompR_mutant_HS', max_length=18, blank=True) # Field name made lowercase.
    ompr_mutant_ho = models.CharField(db_column='ompR_mutant_HO', max_length=18, blank=True) # Field name made lowercase.
    h2o2 = models.CharField(db_column='H2O2', max_length=18, blank=True) # Field name made lowercase.
    oxyr = models.CharField(db_column='OxyR', max_length=18, blank=True) # Field name made lowercase.
    ph5point5 = models.CharField(db_column='pH5point5', max_length=18, blank=True) # Field name made lowercase.
    phop_ph5point5 = models.CharField(db_column='phoP_pH5point5', max_length=18, blank=True) # Field name made lowercase.
    fur_26celsius = models.CharField(max_length=18, blank=True)
    fur_37celsius = models.CharField(max_length=18, blank=True)
    fe2_26temp = models.CharField(db_column='Fe2_26temp', max_length=18, blank=True) # Field name made lowercase.
    fe2_37celsius = models.CharField(db_column='Fe2_37celsius', max_length=18, blank=True) # Field name made lowercase.
    low_mg2 = models.CharField(db_column='low_Mg2', max_length=18, blank=True) # Field name made lowercase.
    phop_mg2 = models.CharField(db_column='phoP_Mg2', max_length=18, blank=True) # Field name made lowercase.
    chloromycetin = models.CharField(max_length=18, blank=True)
    tetracycline = models.CharField(max_length=18, blank=True)
    streptomycin = models.CharField(max_length=18, blank=True)
    exponential_vs_stationary_phase_bhi = models.CharField(db_column='exponential_vs_stationary_phase_BHI', max_length=18, blank=True) # Field name made lowercase.
    exponential_vs_stationary_tmh = models.CharField(db_column='exponential_vs_stationary_TMH', max_length=18, blank=True) # Field name made lowercase.
    tmh_vs_bhi_exponential_phase = models.CharField(db_column='TMH_vs_BHI_exponential_phase', max_length=18, blank=True) # Field name made lowercase.
    tmh_vs_bhi_stationary_phase = models.CharField(db_column='TMH_vs_BHI_stationary_phase', max_length=18, blank=True) # Field name made lowercase.
    antibacterial_peptides = models.CharField(max_length=18, blank=True)
    source = models.CharField(max_length=100, blank=True)
    class Meta:
        managed = False
        db_table = 'expression_profile'