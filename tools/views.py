import csv
import random
import time
import json

from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.db.models import Q
from django.template import RequestContext
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.http import HttpResponse

from browse.models import *
from browse.commonVar import *
from ypga.settings import PKL_DIR
from tools.forms import blastForm
from ypga.settings import BLAST_DIR
from tools.models import *

#pkl
import os
import cPickle as pickle
import hashlib

#gearman
from blast.views import callBlast

from collections import defaultdict

# Create your views here.
def index(request):
    return render_to_response('tools/index.html')


def snp(request):
    return render_to_response('tools/snp.html', {'strainDic': strainDic})


def snpDownload(request):
    if request.method == 'POST':
        if 'selected[]' in request.POST:
            selected = request.POST.getlist('selected[]')

            result = Snp.objects.filter(id__in=selected).values()

            response = HttpResponse(content_type="text/csv")
            response.write('\xEF\xBB\xBF')
            response['Content-Disposition'] = 'attachment; filename=snp.csv'
            writer = csv.writer(response)

            # store row title description
            rowTitle = []
            for item in snpField:
                rowTitle.append(snpFieldDic[item])
            writer.writerow(rowTitle)

            #get data from database
            #data = allEHFPI.objects.values()
            for item in result:
                res = []
                for i in snpField:
                    # if type(item[i]) is types.UnicodeType:
                    #     res.append(item[i].encode('utf-8'))
                    # else:   #long type
                    #     res.append(item[i])
                    res.append(smart_str(item[i]))
                writer.writerow(res)
            return response

    return HttpResponseRedirect('/tools/snp/')


#given a string, return the list
def getList(geneListTmp):
    geneList = []
    if ',' in geneListTmp:
        geneList = geneListTmp.split(',')
    elif '\n' in geneListTmp:
        geneList = geneListTmp.split('\n')
    elif '\r\n' in geneListTmp:
        geneList = geneListTmp.split('\r\n')
    elif ';' in geneListTmp:
        geneList = geneListTmp.split(';')
    else:
        geneList.append(geneListTmp)
    result = []
    for item in geneList:
        result.append(item.strip())

    return result


#get type
# def getType(item):
#     if 'ref' in item:
#         type = 'id'
#     else:
#         type = 'locus'
#     return type


#get strain list
def getStrainAndId(geneList):
    q = Q(id__in=geneList) | Q(locus__in=geneList)
    result = NcbiGene.objects.filter(q)

    strainList = []
    strain = result.values_list('strain').distinct()
    for item in strain:
        strainList.append(item[0])

    idList = []
    id = result.values_list('id').distinct()
    for item in id:
        idList.append(item[0])

    return strainList, idList


def snpResult(request):
    if request.method == 'GET':
        if 'geneList' in request.GET:
            geneListTmp = request.GET['geneList'].strip()

            #get strain list for filter
            strainList1 = []
            idList1 = []
            if len(geneListTmp):
                geneList = getList(geneListTmp)
                strainList1, idList1 = getStrainAndId(geneList)

            strainList2 = []
            if 'strain' in request.GET:
                strainList2 = request.GET.getlist('strain')
            strainList = list(set(strainList1) | set(strainList2))

            idList2 = []
            if len(strainList2):
                #pkl
                name = '-'.join(strainList2)
                name = 'snp-' + hashlib.md5(name).hexdigest()

                if os.path.isfile(PKL_DIR + '/' + name + '.pkl'):  #have pickle
                    file_out = file(PKL_DIR + '/' + name + '.pkl', 'rb')
                    idList2 = pickle.load(file_out)
                    file_out.close()
                else:
                    tmp = NcbiGene.objects.filter(strain__in=strainList2).values_list('id').distinct()
                    for item in tmp:
                        idList2.append(item[0])

                    #generate pickle
                    file_snp = file(PKL_DIR + '/' + name + '.pkl', 'wb')
                    pickle.dump(idList2, file_snp, True)
                    file_snp.close()

            idList = list(set(idList1) | set(idList2))

            type = request.GET['type']
            if type == 'snp':

                result = Snp.objects.filter(id1__in=idList)

                strainSelected = ','.join(strainList)
                strainSelectedNumber = len(strainList)

                #if column in the url, we filter the result
                # too complicated, add strain in gene or snp table
                if 'columns' in request.GET:
                    columns = request.GET['columns']
                    if len(columns.strip()) > 0:
                        columns = columns.split(',')
                        strainSelected = ','.join(columns)
                        strainSelectedNumber = len(columns)
                        # tmp = NcbiGene.objects.filter(strain__in=columns).values_list('id').distinct()
                        # idFilter = []
                        # for item in tmp:
                        #     idFilter.append(item[0])
                        result = result.filter(strain__in=columns)

                if (len(result)):
                    #sort the column
                    order = request.GET.get('order_by', 'id')
                    result = result.order_by(order)

                interactions = len(result)

                strainToDic = {}
                for item in strainList:
                    strainToDic[item] = strainDic[item]

                #ids for download
                ids = []
                idTmp = result.values_list('id')
                for item in idTmp:
                    ids.append(str(item[0]))

                return render_to_response('tools/snpResult.html',
                                          {'result': result, 'strain': strainToDic, 'strainSelected': strainSelected,
                                           'strainSelectedNumber': strainSelectedNumber, 'interactions': interactions,
                                           'ids': ','.join(ids)},
                                          context_instance=RequestContext(request))
            else:  #allele
                q = Q(id1__in=idList) & Q(id2__in=idList)
                result = Snp.objects.filter(q)

                if (len(result)):
                    #sort the column
                    order = request.GET.get('order_by', 'id')
                    result = result.order_by(order)

                interactions = len(result)

                #ids for download
                ids = []
                idTmp = result.values_list('id')
                for item in idTmp:
                    ids.append(str(item[0]))

                return render_to_response('tools/snpIntraResult.html',
                                          {'result': result, 'interactions': interactions, 'ids': ','.join(ids)},
                                          context_instance=RequestContext(request))

    return HttpResponseRedirect('/')


def snpView(request, id):
    result = Snp.objects.filter(id=id)[0]
    snpposlist = result.snpposlist.split(';')

    if '' in snpposlist:
        snpposlist.remove('')

    print snpposlist
    seq1 = NcbiGene.objects.filter(id=result.id1)[0].seq
    seq2 = NcbiGene.objects.filter(id=result.id2)[0].seq
    alignments = generateAlign(snpposlist, seq1, seq2)

    #generate snp allele
    allele1 = SnpAllele.objects.filter(id=result.id1)[0].allelelist
    allele2 = SnpAllele.objects.filter(id=result.id2)[0].allelelist
    posDict1= defaultdict()
    posDict2 = defaultdict()
    allele1List =  allele1.split(';')
    if '' in allele1List:
        allele1List.remove('')

    allele2List =  allele2.split(';')
    if '' in allele2List:
        allele2List.remove('')

    for item in allele1List:
        pos = int(item[0:item.index('_')])
        chars = item[item.index('_')+1:]
        posDict1[pos] = chars

    for item in allele2List:
        pos = int(item[0:item.index('_')])
        chars = item[item.index('_')+1:]
        posDict2[pos] = chars

    commonPos = set(posDict1.keys()) & set(posDict2.keys())
    allele1Dict = {}
    allele2Dict = {}
    posList = []
    for item in commonPos:
        posList.append(item)
        allele1Dict[item] = posDict1[item]
        allele2Dict[item] = posDict2[item]

    posList.sort()

    return render_to_response('tools/snpView.html', {'id': id, 'result': result, 'alignments': alignments,'posList':posList,'allele1Dict':allele1Dict,'allele2Dict':allele1Dict})


#given a snppos and related seq, return the aligned result
def generateAlign(snpposlist, seq1, seq2):
    pos1List = []
    pos2List = []
    char1List = []
    char2List = []
    for item in snpposlist:
        pos = item.split(':')
        pos1List.append(pos[0].split('_')[0])
        char1List.append(pos[0].split('_')[1])
        pos2List.append(pos[1].split('_')[0])
        char2List.append(pos[1].split('_')[1])
    alignments1 = ''
    alignments_middle = ''
    alignments2 = ''

    for i in range(0, len(pos1List)):
        alignments1 = alignments1 + char1List[i]
        alignments_middle = alignments_middle + '|'
        alignments2 = alignments2 + char2List[i]
        #append five char before and after

        #more than two
        if len(pos1List) > 1:

            if i == 0:  #first one
                #left for pos1List and middle
                if int(pos1List[i]) > 4:
                    alignments1 = seq1[int(pos1List[i]) - 6:int(pos1List[i]) - 1] + alignments1
                    alignments_middle = '     ' + alignments_middle
                else:
                    alignments1 = seq1[0:int(pos1List[i])] + alignments1

                    space = ''
                    for tt in range(0, int(pos1List[i])):
                        space += ' '
                    alignments_middle = space + alignments_middle

                #left for pos2List
                if int(pos2List[i]) > 4:
                    alignments2 = seq2[int(pos2List[i]) - 6:int(pos2List[i]) - 1] + alignments2
                else:
                    alignments2 = seq2[0:int(pos2List[i])] + alignments2


                #right for pos1List
                if int(pos1List[i + 1]) - int(pos1List[i]) > 10:
                    alignments1 = alignments1 + seq1[int(pos1List[i]) + 1:int(pos1List[i]) + 6] + '  ' + seq1[int(
                        pos1List[i + 1]) - 6:int(pos1List[i + 1]) - 1]
                    space = ''
                    for tt in range(0, 5):
                        space += ' '
                    for tt in range(0, 2):
                        space += '.'
                    for tt in range(0, 5):
                        space += ' '
                    alignments_middle = alignments_middle + space

                else:
                    alignments1 = alignments1 + seq1[int(pos1List[i]):int(pos1List[i + 1]) - 1]
                    space = ''
                    for tt in range(0, int(pos1List[i + 1]) - int(pos1List[i]) - 1):
                        space += ' '
                    alignments_middle = alignments_middle + space

                #right for pos2List
                if int(pos2List[i + 1]) - int(pos2List[i]) > 10:
                    alignments2 = alignments2 + seq2[int(pos2List[i]) + 1:int(pos2List[i]) + 6] + '  ' + seq2[int(
                        pos2List[i + 1]) - 6:int(pos2List[i + 1]) - 1]

                else:
                    alignments2 = alignments2 + seq2[int(pos2List[i]):int(pos2List[i + 1]) - 1]

            elif i == len(pos1List) - 1:  #the last one
                #left no need
                #right for pos1List
                if len(seq1) - int(pos1List[i]) > 5:
                    alignments1 = alignments1 + seq1[int(pos1List[i]) - 1:int(pos1List[i]) + 4]
                    space = ''
                    for tt in range(0, 5):
                        space += ' '
                    alignments_middle = alignments_middle + space

                else:
                    alignments1 = alignments1 + seq1[int(pos1List[i]) + 1:len(seq1)]
                    space = ''
                    for tt in range(0, len(seq1) - int(pos1List[i]) - 1):
                        space += ' '
                    alignments_middle = alignments_middle + space

                #right for pos2List
                if len(seq1) - int(pos2List[i]) > 5:
                    alignments2 = alignments2 + seq2[int(pos2List[i]):int(pos2List[i]) + 5]

                else:
                    alignments2 = alignments2 + seq2[int(pos2List[i]) + 1:len(seq1)]

            else:  #middle one
                #right for pos1List
                if int(pos1List[i + 1]) - int(pos1List[i]) > 10:
                    print '##' + seq1[int(pos1List[i + 1]) - 6:int(pos1List[i + 1]) - 1]
                    alignments1 = alignments1 + seq1[int(pos1List[i]):int(pos1List[i]) + 5] + '  ' + seq1[int(
                        pos1List[i + 1]) - 6:int(pos1List[i + 1]) - 1]
                    space = ''
                    for tt in range(0, 5):
                        space += ' '
                    for tt in range(0, 2):
                        space += '.'
                    for tt in range(0, 5):
                        space += ' '
                    alignments_middle = alignments_middle + space

                else:
                    alignments1 = alignments1 + seq1[int(pos1List[i]) + 1:int(pos1List[i + 1])]
                    space = ''
                    for tt in range(0, int(pos1List[i + 1]) - int(pos1List[i]) - 1):
                        space += ' '
                    alignments_middle = alignments_middle + space

                #right for pos2List
                if int(pos2List[i + 1]) - int(pos2List[i]) > 10:
                    alignments2 = alignments2 + seq2[int(pos2List[i]):int(pos2List[i]) + 5] + '  ' + seq2[int(
                        pos2List[i + 1]) - 6:int(pos2List[i + 1]) - 1]

                else:
                    alignments2 = alignments2 + seq2[int(pos2List[i]) + 1:int(pos2List[i + 1])]


        else:  #only one pos
            #left for pos1List
            if int(pos1List[i]) > 4:
                alignments1 = seq1[int(pos1List[i]) - 6:int(pos1List[i]) - 1] + alignments1
                space = ''
                for tt in range(0, 5):
                    space += ' '
                alignments_middle = space + alignments_middle

            else:
                alignments1 = seq1[0:int(pos1List[i])] + alignments1
                space = ''
                for tt in range(0, int(pos1List[i])):
                    space += ' '
                alignments_middle = space + alignments_middle

            #left for pos2List
            if int(pos2List[i]) > 4:
                alignments2 = seq2[int(pos2List[i]) - 6:int(pos2List[i]) - 1] + alignments2
            else:
                alignments2 = seq2[0:int(pos2List[i])] + alignments2

            #right for pos1List
            if len(seq1) - int(pos1List[i]) > 5:
                alignments1 = alignments1 + seq1[int(pos1List[i]):int(pos1List[i]) + 5]
                space = ''
                for tt in range(0, 5):
                    space += ' '
                alignments_middle = alignments_middle + space

            else:
                alignments1 = alignments1 + seq1[int(pos1List[i]) + 1:len(seq1)]
                space = ''
                for tt in range(0, len(seq1) - int(pos1List[i]) - 1):
                    space += ' '
                alignments_middle = alignments_middle + space

            #right for pos2List
            if len(seq1) - int(pos2List[i]) > 5:
                alignments2 = alignments2 + seq2[int(pos2List[i]):int(pos2List[i]) + 5]

            else:
                alignments2 = alignments2 + seq2[int(pos2List[i]) + 1:len(seq1)]

    alignments = alignments1 + '\r\n' + alignments_middle + '\r\n' + alignments2
    return alignments


def intergenic(request):
    strainDic = defaultdict(list)
    result = NcbiGenome.objects.all().values_list('strain', 'genomerefno')
    for strain, genome in result:
        strainDic[strain].append(genome)

    strainDic = dict(strainDic)

    return render_to_response('tools/intergenic.html', {'strainDic': strainDic},
                              context_instance=RequestContext(request))


def intergenicResult(request):
    if request.method == 'GET':
        print request.session.get('POST')
        if request.session.get('POST'):
            request.POST = request.session['POST']

    request.session['POST'] = request.POST  #store post data in session

    if 'geneList' in request.POST:
        geneList = request.POST['geneList']
        if geneList.strip() != '':
            #geneList is considered first
            geneList = getList(geneList.strip())
            intergenicListTmp = IntergenicBlastResult.objects.filter(idgene__in=geneList).values_list('idintergenic1')
            intergenicList = []
            for item in intergenicListTmp:
                intergenicList.append(item[0])

            result = Intergenic.objects.filter(idintergenic__in=intergenicList)

        else:
            if 'genome' in request.POST:
                genome = request.POST.get('genome').split(',')
                result = Intergenic.objects.filter(genomerefno__in=genome)

        if (len(result)):
            #sort the column
            order = request.GET.get('order_by', 'idintergenic')
            result = result.order_by(order)

        interactions = len(result)

        ids = []
        idTmp = result.values_list('idintergenic')
        for item in idTmp:
            ids.append(str(item[0]))

        return render_to_response('tools/intergenicResult.html',
                                  {'result': result, 'interactions': interactions, 'ids': ','.join(ids)},
                                  context_instance=RequestContext(request))

    return HttpResponseRedirect('/tools/intergenic')


def intergenicDownload(request):
    if request.method == 'POST':
        if 'selected[]' in request.POST:
            selected = request.POST.getlist('selected[]')

            result = Intergenic.objects.filter(idintergenic__in=selected).values()

            response = HttpResponse(content_type="text/csv")
            response.write('\xEF\xBB\xBF')
            response['Content-Disposition'] = 'attachment; filename=intergenic.csv'
            writer = csv.writer(response)

            # store row title description
            rowTitle = []
            for item in intergenicField:
                rowTitle.append(intergenicFieldDic[item])
            writer.writerow(rowTitle)

            #get data from database
            for item in result:
                res = []
                for i in intergenicField:
                    # if type(item[i]) is types.UnicodeType:
                    #     res.append(item[i].encode('utf-8'))
                    # else:   #long type
                    #     res.append(item[i])
                    res.append(smart_str(item[i]))
                writer.writerow(res)
            return response

    return HttpResponseRedirect('/tools/intergenic/')


#the loading page
def intergenicView(request, id):
    result = Intergenic.objects.filter(idintergenic=id)[0]
    return render_to_response('tools/intergenicView.html', {'result': result})


def homology(request):
    return render_to_response('tools/homology.html', context_instance=RequestContext(request))


def homologyDownload(request):
    if request.method == 'POST':
        if 'selected[]' in request.POST:
            selected = request.POST.getlist('selected[]')

            result = GeneCorrespond.objects.filter(id__in=selected).values()

            response = HttpResponse(content_type="text/csv")
            response.write('\xEF\xBB\xBF')
            response['Content-Disposition'] = 'attachment; filename=homology.csv'
            writer = csv.writer(response)

            # store row title description
            rowTitle = []
            for item in homologyField:
                rowTitle.append(homologyFieldDic[item])
            writer.writerow(rowTitle)

            #get data from database
            for item in result:
                res = []
                for i in homologyField:
                    # if type(item[i]) is types.UnicodeType:
                    #     res.append(item[i].encode('utf-8'))
                    # else:   #long type
                    #     res.append(item[i])
                    res.append(smart_str(item[i]))
                writer.writerow(res)
            return response

    return HttpResponseRedirect('/tools/homology/')


def homologyResult(request):
    if request.method == 'GET':
        print request.session.get('POST')
        if request.session.get('POST'):
            request.POST = request.session['POST']

    request.session['POST'] = request.POST  #store post data in session
    if 'geneList' in request.POST:
        geneListTmp = request.POST['geneList'].strip()

        #get strain list for filter
        strainList = []
        idList = []
        if len(geneListTmp):
            geneList = getList(geneListTmp)
            strainList, idList = getStrainAndId(geneList)

            result = GeneCorrespond.objects.filter(id__in=idList)
            if (len(result)):
                #sort the column
                order = request.GET.get('order_by', 'id')
                result = result.order_by(order)

            #type list
            typeList = []
            tmp = result.values_list('type')
            for item in tmp:
                if item[0] not in typeList:
                    typeList.append(item[0])

            #strain
            strainDict = {}
            for item in strainList:
                strainDict[item] = strainDic[item]

            q1 = Q()
            q2 = Q()
            types = ''
            strains = ''
            if 'types' in request.GET:
                types = request.GET.get('types').split(',')
                q1 = Q(type__in=types)
            if 'strains' in request.GET:
                strains = request.GET.get('strains').split(',')
                q2 = Q(strain__in=strains)

            result = result.filter(q1 & q2)

            interactions = len(result)
            strainNumber = len(strainList)

            tmp = result.values_list('listnum').distinct()
            sum = 0
            for item in tmp:
                sum = sum + int(item[0])

            ids = []
            for item in result:
                ids.append(item.id)

            return render_to_response('tools/homologyResult.html',
                                      {'strain': ','.join(strainList), 'strainDict': strainDict,
                                       'strainNumber': strainNumber,
                                       'type': typeList, 'result': result, 'sum': sum,
                                       'interactions': interactions, 'geneList': ','.join(ids),
                                       'types': ','.join(types), 'strains': ','.join(strains)},
                                      context_instance=RequestContext(request))

    return HttpResponseRedirect('/tools/homology')


#the loading page
def homologyView(request):
    if request.method == "POST":
        if 'geneList' in request.POST:
            geneList = request.POST['geneList']

            return render_to_response('tools/homologyViewOthers.html', {'geneList': geneList},
                                      context_instance=RequestContext(request))

    return HttpResponseRedirect('/tools/homology')


#given a list of ids, generate the network
def homologyViewNetwork(request):
    if request.method == 'POST':
        if 'text' in request.POST:
            geneList = request.POST['text'].split(',')
            result = GeneCorrespond.objects.filter(id__in=geneList).order_by('id')

            #locus and product dict, should be in the gene correspond table, use in the network
            corListAll = []
            for item in result:
                corListAll = corListAll + item.orthologylist.strip().split(
                    ';')  #change idcorrespondlist to orthologylist
            corListAll = corListAll + geneList

            #the linked node, we also display, use different color. remove the submitted node first
            otherList = (set(corListAll) - set(geneList))
            otherResult = GeneCorrespond.objects.filter(id__in=otherList).order_by('id')

            locusDict = {}
            productDict = {}
            strainDict = {}
            geneResult = NcbiGene.objects.filter(id__in=corListAll)
            for item in geneResult:
                locusDict[item.id] = item.locus
                productDict[item.id] = item.product
                strainDict[item.id] = item.strain

            # generate interaction network start
            jsonRes = []  # a list

            # generate json file
            for item in result:
                node = {}
                node['name'] = locusDict.get(item.id, item.id)  # name attr
                node['id'] = locusDict.get(item.id, item.id)  #id attr

                data = {}  #data attr

                data['$color'] = '#800080'

                if item.type == 'perfectCore' or item.type == 'notPerfectCore':  #core gene
                    data['$type'] = 'triangle'
                elif item.type == 'notCore':  #not core gene
                    data['$type'] = 'circle'
                elif item.type == 'unique':  #unique gene
                    data['$type'] = 'star'
                else:
                    data['$type'] = 'circle'  #

                data['nodeType'] = item.type
                data['nodeAttr'] = 'submitted'
                data['strain'] = strainDict.get(item.id, item.id)  #the strain of the gene
                data['des'] = productDict.get(item.id, item.id)  #protein name, use as tips
                node['data'] = data

                # set adjacencies attr
                adjacencies = []

                corList = item.idcorrespondlist.strip().split(';')
                if '' in corList:
                    corList.remove('')
                if '\n' in corList:
                    corList.remove('\n')

                for adj in corList:  # generate connected gene
                    relation = {}
                    relation['nodeFrom'] = node['id']
                    relation['nodeTo'] = locusDict.get(adj, adj)
                    nodeData = {}  # can overwrite, edge attribute(display linked gene)
                    nodeData["$color"] = "#23A4FF"
                    nodeData['identity'] = item.coreidentitythreshold
                    relation['data'] = nodeData
                    adjacencies.append(relation)
                    #adjacenciesNumber = adjacenciesNumber + 1  #calculate common and specific gene

                node['adjacencies'] = adjacencies
                jsonRes.append(node)

            for item in otherResult:  #other node
                node = {}
                node['name'] = locusDict.get(item.id, item.id)  # name attr
                node['id'] = locusDict.get(item.id, item.id)  #id attr

                data = {}  #data attr

                data['$color'] = '#416D9C'

                if item.type == 'perfectCore' or item.type == 'notPerfectCore':  #core gene
                    data['$type'] = 'triangle'
                elif item.type == 'notCore':  #not core gene
                    data['$type'] = 'circle'
                elif item.type == 'unique':  #unique gene
                    data['$type'] = 'star'
                else:
                    data['$type'] = 'circle'  #

                data['nodeType'] = item.type
                data['nodeAttr'] = 'other'
                data['strain'] = strainDict.get(item.id, item.id)  #the strain of the gene
                data['des'] = productDict.get(item.id, item.id)  #protein name, use as tips
                node['data'] = data
                #remove adjacencies
                jsonRes.append(node)

            toJson = json.dumps(jsonRes)
            # generate interaction map end

            return render_to_response('tools/displayNetwork.js',
                                      {'toJson': toJson})

    return HttpResponseRedirect('/tools/homology')


#the index page of blast tool
def blastIndex(request):
    return render_to_response('tools/blastIndex.html', context_instance=RequestContext(request))


def blast(request):
    if request.method == 'POST':
        form = blastForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            #parse parameter
            database = request.POST['database']
            num_alignments = request.POST['num_alignments']
            num_descriptions = request.POST['num_descriptions']
            max_target_seqs = request.POST['max_target_seqs']
            expect = request.POST['expect']
            filterQuery = 0
            if 'filterQuery' in request.POST:
                filterQuery = 1
            querySeq = form.cleaned_data['querySeq'].strip()
            queryFile = form.cleaned_data['queryFile']
            if len(querySeq) or (queryFile is not None):
                pre = str(int(time.time())) + str(random.randrange(0, 100))  #also the job id
                file = BLAST_DIR + r'/queryFiles/query_' + pre + r'.fasta'
                if len(querySeq):
                    #write seq to file
                    file_in = open(file, 'w')
                    file_in.write(querySeq)
                    file_in.close()
                else:
                    os.rename(BLAST_DIR + r'/queryFiles/' + str(queryFile), file)

                resultFile = BLAST_DIR + r'/result/result_' + pre + r'.txt'
                #test add a task
                callBlast(file, database, resultFile, num_alignments, num_descriptions, expect, max_target_seqs, pre)

                return render_to_response('tools/blastResult.html', {'jobId': pre},
                                          context_instance=RequestContext(request))
                #no need to convert it to text, use file
                #handle_uploaded_file(queryFile)

                # form = blastForm(
                #     initial={
                #     'database':'genome',
                #     'alignments':'50',
                #     'expect':'10',
                #     'matrix':'BLOSUM62'
                # })

    form = blastForm()
    return render_to_response('tools/blast.html', {'form': form}, context_instance=RequestContext(request))


#given a job id, return state and msg
def queryState(jobId):
    result = blastResultModel.objects.filter(jobId=jobId)
    msg = ''
    state = ''
    if len(result):
        item = result[0]
        state = item.status
        if state == 'FAILED':
            msg = 'You submission has been failed, try to submit it again!'
        elif state == 'COMPLETE':
            resultFile = open(BLAST_DIR + r'/result/result_' + jobId + r'.txt', 'r')
            for line in resultFile:
                msg = msg + line + '<br/>'
            resultFile.close()

            if msg.strip() == '':  #empty result
                msg = 'No hits found!'

        else:
            msg = 'Your job is in the queue, please wait!!'
    else:
        msg = 'The Job doesn\'t exist, please submit the right job id!'

    return state, msg


#display the blast reuslt
def blastResult(request):
    if request.method == 'GET':
        if 'jobId' in request.GET:
            jobId = request.GET['jobId']
            state, msg = queryState(jobId)

            return render_to_response('tools/queryBlastResult.html', {'jobId': jobId, 'msg': msg},
                                      context_instance=RequestContext(request))

    return HttpResponseRedirect('/tools/blastIndex')


#ajax query state
def ajaxQueryState(request):
    if request.method == 'GET':
        if 'jobId' in request.GET:
            jobId = request.GET['jobId']
            state, msg = queryState(jobId)
            jsonDict = {}
            jsonDict['state'] = state
            jsonDict['msg'] = msg

            return HttpResponse(json.dumps(jsonDict))

    return HttpResponseRedirect('/tools/blastIndex')


#this function process the file and return the gene symbol list
def handle_uploaded_file(uploadFile):
    fasta = ''
    if uploadFile is not None:
        for chunk in uploadFile.chunks():
            fasta += chunk
        fasta = fasta.strip()
    return fasta
