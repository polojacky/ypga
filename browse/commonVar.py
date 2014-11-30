#common var used in the project
geneField = ['id', 'type', 'genomerefno', 'strain','geneid', 'locus', 'genename', 'startpos', 'endpos', 'strand', 'length',
             'pid', 'cogno', 'product', 'source', 'seq', 'other']

geneFieldDic = {
    'id': 'ID',
    'type': 'Type',
    'genomerefno': 'Genome Ref no',
    'strain':'strain',
    'geneid': 'Gene ID',
    'locus': 'Locus',
    'genename': 'Gene Name',
    'startpos': 'Start Pos',
    'endpos': 'End Pos',
    'strand': 'Strand',
    'length': 'Length',
    'pid': 'pid',
    'cogno': 'COG no',
    'product': 'Product',
    'source': 'Source',
    'seq': 'seq',
    'other': 'Other'
}

srnaField = ['id', 'idsrna', 'name', 'genomerefno', 'genomelocation', 'strain', 'strand', 'start', 'end', 'length',
             'type', 'annovalidatetype', 'id_koo', 'samples', 'bhi_rpkm', 'tmh_rpkm', 'lung_rpkm', 'spleen_rpkm',
             'antisensegenelocus', 'upstreamgenelocus', 'downstreamgenelocus', 'source', 'other']

srnaFieldDic = {
    'id': 'id',
    'idsrna': 'idsrna',
    'name': 'name',
    'genomerefno': 'genomerefno',
    'genomelocation': 'genomelocation',
    'strain': 'strain',
    'strand': 'strand',
    'start': 'start',
    'end': 'end',
    'length': 'length',
    'type': 'type',
    'annovalidatetype': 'annovalidatetype',
    'id_koo': 'id_koo',
    'samples': 'samples',
    'bhi_rpkm': 'bhi_rpkm',
    'tmh_rpkm': 'tmh_rpkm',
    'lung_rpkm': 'lung_rpkm',
    'spleen_rpkm': 'spleen_rpkm',
    'antisensegenelocus': 'antisensegenelocus',
    'upstreamgenelocus': 'upstreamgenelocus',
    'downstreamgenelocus': 'downstreamgenelocus',
    'source': 'source',
    'other': 'other'

}

expField = ['locus', 'genomerefno', 'genename', 'classnum', 'number_37_vs_26celsius', 'cold_shock', 'heat_shock',
            'high_salt', 'high_osmolarity', 'ompr_mutant_hs', 'ompr_mutant_ho', 'h2o2', 'oxyr', 'ph5point5',
            'phop_ph5point5', 'fur_26celsius', 'fur_37celsius', 'fe2_26temp', 'fe2_37celsius', 'low_mg2', 'phop_mg2',
            'chloromycetin', 'tetracycline', 'streptomycin', 'exponential_vs_stationary_phase_bhi',
            'exponential_vs_stationary_tmh', 'tmh_vs_bhi_exponential_phase', 'tmh_vs_bhi_stationary_phase',
            'antibacterial_peptides', 'source', 'other']

expFieldDic = {
    'locus': 'locus',
    'genomerefno': 'genomerefno',
    'genename': 'genename',
    'classnum': 'classnum',
    'number_37_vs_26celsius': 'number_37_vs_26celsius',
    'cold_shock': 'cold_shock',
    'heat_shock': 'heat_shock',
    'high_salt': 'high_salt',
    'high_osmolarity': 'high_osmolarity',
    'ompr_mutant_hs': 'ompr_mutant_hs',
    'ompr_mutant_ho': 'ompr_mutant_ho',
    'h2o2': 'h2o2',
    'oxyr': 'oxyr',
    'ph5point5': 'ph5point5',
    'phop_ph5point5': 'phop_ph5point5',
    'fur_26celsius': 'fur_26celsius',
    'fur_37celsius': 'fur_37celsius',
    'fe2_26temp': 'fe2_26temp',
    'fe2_37celsius': 'fe2_37celsius',
    'low_mg2': 'low_mg2',
    'phop_mg2': 'phop_mg2',
    'chloromycetin': 'chloromycetin',
    'tetracycline': 'tetracycline',
    'streptomycin': 'streptomycin',
    'exponential_vs_stationary_phase_bhi': 'exponential_vs_stationary_phase_bhi',
    'exponential_vs_stationary_tmh': 'exponential_vs_stationary_tmh',
    'tmh_vs_bhi_exponential_phase': 'tmh_vs_bhi_exponential_phase',
    'tmh_vs_bhi_stationary_phase': 'tmh_vs_bhi_stationary_phase',
    'antibacterial_peptides': 'antibacterial_peptides',
    'source': 'source',
    'other': 'other'

}

proteinField = ['pid', 'refseqno', 'genomerefno', 'length', 'cogno', 'product', 'seq', 'source', 'other']
proteinFieldDic = {
    'pid': 'pid',
    'refseqno': 'refseqno',
    'genomerefno': 'genomerefno',
    'length': 'length',
    'cogno': 'cogno',
    'product': 'product',
    'seq': 'seq',
    'source': 'source',
    'other': 'other'

}

snpField = ['id', 'id1', 'id2', 'snpposlist', 'listnum','source', 'other']
snpFieldDic = {
    'id': 'id',
    'id1': 'id1',
    'id2': 'id2',
    'snpposlist': 'snpposlist',
    'listnum':'listnum',
    'source': 'source',
    'other': 'other'

}

correspondField = ['id', 'type', 'idcorrespondlist','listnum', 'coreidentitythreshold', 'corecoveragethreshold', 'source',
                   'other']
correspondFieldDic = {
    'id': 'id',
    'type': 'type',
    'idcorrespondlist': 'idcorrespondlist',
    'listnum':'listnum',
    'coreidentitythreshold': 'coreidentitythreshold',
    'corecoveragethreshold': 'corecoveragethreshold',
    'source': 'source',
    'other': 'other'

}

strainDic = {
    'CO92': 'CO92',
    '91001': '91001',
    'Nepal516': 'Nepal516',
    'Angola': 'Angola',
    'Antiqua': 'Antiqua',
    'KIM': 'KIM',
    'PestoidesF': 'Pestoides F',
    'A1122': 'A1122',
    'Harbin35': 'Harbin35',
    'D106004': 'D106004',
    'D182038': 'D182038',
    'Z176003': 'Z176003'
}

homologyField = ['id', 'type', 'idcorrespondlist', 'coreidentitythreshold', 'corecoveragethreshold', 'source', 'other']
homologyFieldDic = {
    'id': 'id',
    'type': 'type',
    'idcorrespondlist': 'idcorrespondlist',
    'coreidentitythreshold': 'coreidentitythreshold',
    'corecoveragethreshold': 'corecoveragethreshold',
    'source': 'source',
    'other': 'other',
}

intergenicField = ['idintergenic','genomerefno','strand','startpos','endpos','length','seq','upstreamgeneid','downstreamgeneid','source','other']
intergenicFieldDic = {
    'idintergenic':'idintergenic',
    'genomerefno':'genomerefno',
    'strand':'strand',
    'startpos':'startpos',
    'endpos':'endpos',
    'length':'length',
    'seq':'seq',
    'upstreamgeneid':'upstreamgeneid',
    'downstreamgeneid':'downstreamgeneid',
    'source':'source',
    'other':'other',
}