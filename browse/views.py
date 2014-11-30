import csv

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.db.models import Q

from browse.models import *
from commonVar import *
from ypga.settings import GENOME_DIR


# Create your views here.

#the welcome page
def index(request):
    return render_to_response('browse/index.html', context_instance=RequestContext(request))


def genome(request, id):
    result = Genome.objects.filter(strain=id).order_by('genometype')
    publicationDict = {}
    for item in result:
        pubList = item.reference.split(';')
        pubList = list(set(pubList))
        if '' in pubList:
            pubList.remove('')
        publicationDict[item.genomerefno] = pubList

    return render_to_response('browse/genome.html',
                              {'result': result, 'strain': id, 'publicationDict': publicationDict,
                               'GENOME_DIR': GENOME_DIR},
                              context_instance=RequestContext(request))


def gene(request, id):
    result = Fragment.objects.filter(strain=id).order_by('locus')
    if (len(result)):
        #sort the column
        order = request.GET.get('order_by', 'locus')
        result = result.order_by(order)

    aaList = []
    for item in result:
        if item.locus not in aaList:
            aaList.append(item.locus)
    geneNumber = len(aaList)
    interactions = len(result)

    return render_to_response('browse/gene.html',
                              {'result': result, 'strain': id, 'geneNumber': geneNumber, 'interactions': interactions},
                              context_instance=RequestContext(request))


def geneAll(request):
    result = Fragment.objects.all().order_by('locus')

    tmp = Fragment.objects.all().values_list('strain')
    id = []
    for item in tmp:
        if item[0] not in id:
            id.append(item[0])

    if (len(result)):
        #sort the column
        order = request.GET.get('order_by', 'locus')
        result = result.order_by(order)

    geneNumber = len(result.values_list('locus').distinct())
    interactions = len(result)

    return render_to_response('browse/gene.html',
                              {'result': result, 'strain': ','.join(id), 'geneNumber': geneNumber,
                               'interactions': interactions},
                              context_instance=RequestContext(request))


def geneDownload(request):
    if request.method == 'GET':
        if 'type' in request.GET and 'selected' in request.GET:
            type = request.GET['type']
            selected = request.GET['selected']
            if type == 'all':
                result = Fragment.objects.filter(strain=selected).order_by('locus').values()
            else:
                selected = selected.split(',')
                result = Fragment.objects.filter(id__in=selected).values()

            response = HttpResponse(content_type="text/csv")
            response.write('\xEF\xBB\xBF')
            response['Content-Disposition'] = 'attachment; filename=gene.csv'
            writer = csv.writer(response)

            # store row title description
            rowTitle = []
            for item in geneField:
                rowTitle.append(geneFieldDic[item])
            writer.writerow(rowTitle)

            #get data from database
            #data = allEHFPI.objects.values()
            for item in result:
                res = []
                for i in geneField:
                    # if type(item[i]) is types.UnicodeType:
                    #     res.append(item[i].encode('utf-8'))
                    # else:   #long type
                    #     res.append(item[i])
                    res.append(smart_str(item[i]))
                writer.writerow(res)
            return response

    return HttpResponseRedirect('/browse')


def geneDetail(request, id):
    geneResult = Fragment.objects.filter(locus=id)
    for item in geneResult:
        genomerefno = item.genomerefno  #may have two for 91001 locus

    genomeResult = Genome.objects.filter(genomerefno=genomerefno)

    publicationDict = {}
    for item in genomeResult:
        pubList = item.reference.split(';')
        pubList = list(set(pubList))
        if '' in pubList:
            pubList.remove('')
        publicationDict[item.genomerefno] = pubList

    proteinResult = Protein.objects.filter(locus=id)  #may have two for 91001 locus

    reannoResult = Reanno.objects.filter(id_original=id)

    expResult = ExpressionProfile.objects.filter(locus=id)

    return render_to_response('browse/geneDetail.html', {
        'geneResult': geneResult,
        'genomeResult': genomeResult,
        'publicationDict': publicationDict,
        'proteinResult': proteinResult,
        'reannoResult': reannoResult,
        'expResult': expResult,
        'id': id,
    },context_instance=RequestContext(request))


def srnaDetail(request, id):
    srnaResult = Srna.objects.filter(id=id)
    return render_to_response('browse/srnaDetail.html', {
        'srnaResult': srnaResult, 'id': id}, context_instance=RequestContext(request))


def srna(request, id):
    #change columns?
    if 'columns' in request.GET:
        selectedColumns_tmp = request.GET['columns']
        selectedColumns = selectedColumns_tmp.split(',')
        request.session['has_changed_srna'] = True  # set the session, not change
        request.session['srnaColumns'] = selectedColumns  #store the columns

    if 'has_changed_srna' not in request.session:
        defaultColumns = ['id', 'idsrna', 'name', 'type', 'upstreamgenelocus', 'downstreamgenelocus']
        request.session['srnaColumns'] = defaultColumns  #store the columns

    genomeRes = Genome.objects.filter(strain=id).values_list('genomerefno')
    refList = []
    for item in genomeRes:
        refList.append(item[0])

    #columns to display start!

    displayColumns = request.session['srnaColumns']
    if displayColumns == '':
        displayColumns = ['id', 'idsrna', 'name', 'type', 'upstreamgenelocus', 'downstreamgenelocus']
    displayColumnsDic = []
    for item in displayColumns:
        displayColumnsDic.append([item, srnaFieldDic[item]])
    #columns to display end

    result = Srna.objects.filter(genomerefno__in=refList).order_by('id')
    if (len(result)):
        #sort the column
        order = request.GET.get('order_by', 'id')
        result = result.order_by(order)

    interactions = len(result)

    #custom display columns start!
    columns = []
    for i in range(0, len(srnaField), 1):
        columns.append([srnaField[i], srnaFieldDic[srnaField[i]]])
    #custom display columns end

    print columns

    return render_to_response('browse/srna.html',
                              {'result': result, 'strain': id, 'interactions': interactions, 'columns': columns,
                               'displayColumnsDic': displayColumnsDic},
                              context_instance=RequestContext(request))


def srnaAll(request):
    result = Srna.objects.all().order_by('id')
    tmp = result.values_list('strain')
    id = []
    for item in tmp:
        if item[0] not in id:
            id.append(item[0])

    if (len(result)):
        #sort the column
        order = request.GET.get('order_by', 'id')
        result = result.order_by(order)

    interactions = len(result)

    return render_to_response('browse/srna.html',
                              {'result': result, 'strain': ','.join(id), 'interactions': interactions},
                              context_instance=RequestContext(request))


def srnaDownload(request):
    if request.method == 'GET':
        if 'type' in request.GET and 'selected' in request.GET:
            type = request.GET['type']
            selected = request.GET['selected']
            if type == 'all':
                selected = selected.split(',')
                genomeRes = Genome.objects.filter(strain__in=selected).values_list('genomerefno')
                refList = []
                for item in genomeRes:
                    refList.append(item[0])
                result = Srna.objects.filter(genomerefno__in=refList).order_by('id').values()
            else:
                selected = selected.split(',')
                result = Srna.objects.filter(id__in=selected).values()

            response = HttpResponse(content_type="text/csv")
            response.write('\xEF\xBB\xBF')
            response['Content-Disposition'] = 'attachment; filename=srna.csv'
            writer = csv.writer(response)

            # store row title description
            rowTitle = []
            for item in srnaField:
                rowTitle.append(srnaFieldDic[item])
            writer.writerow(rowTitle)

            #get data from database
            #data = allEHFPI.objects.values()
            for item in result:
                res = []
                for i in srnaField:
                    # if type(item[i]) is types.UnicodeType:
                    #     res.append(item[i].encode('utf-8'))
                    # else:   #long type
                    #     res.append(item[i])
                    res.append(smart_str(item[i]))
                writer.writerow(res)
            return response

    return HttpResponseRedirect('/browse')


def exp(request, id):
    #change columns?
    if 'columns' in request.GET:
        selectedColumns_tmp = request.GET['columns']
        selectedColumns = selectedColumns_tmp.split(',')
        request.session['has_changed_exp'] = True  # set the session, not change
        request.session['expColumns'] = selectedColumns  #store the columns

    if 'has_changed_exp' not in request.session:
        defaultColumns = ['locus', 'genename', 'classnum', 'number_37_vs_26celsius', 'cold_shock', 'heat_shock']
        request.session['expColumns'] = defaultColumns  #store the columns

    genomeRes = Genome.objects.filter(strain=id).values_list('genomerefno')
    refList = []
    for item in genomeRes:
        refList.append(item[0])

        #columns to display start!

    displayColumns = request.session['expColumns']
    if displayColumns == '':
        displayColumns = ['locus', 'genename', 'classnum', 'number_37_vs_26celsius', 'cold_shock', 'heat_shock']
    displayColumnsDic = []
    for item in displayColumns:
        displayColumnsDic.append([item, expFieldDic[item]])
    #columns to display end

    result = ExpressionProfile.objects.filter(genomerefno__in=refList).order_by('locus')
    if (len(result)):
        #sort the column
        order = request.GET.get('order_by', 'locus')
        result = result.order_by(order)

    interactions = len(result)

    #custom display columns start!
    columns = []
    for i in range(0, len(expField), 1):
        columns.append([expField[i], expFieldDic[expField[i]]])
    #custom display columns end

    return render_to_response('browse/exp.html',
                              {'result': result, 'strain': id, 'interactions': interactions, 'columns': columns,
                               'displayColumnsDic': displayColumnsDic},
                              context_instance=RequestContext(request))


def expAll(request):
    result = ExpressionProfile.objects.all().order_by('locus')
    tmp = result.values_list('genomerefno')
    id = []
    for item in tmp:
        if item[0] not in id:
            id.append(item[0])

    tmp = Genome.objects.filter(genomerefno__in=id).values_list('strain')
    id = []
    for item in tmp:
        if item[0] not in id:
            id.append(item[0])

    if (len(result)):
        #sort the column
        order = request.GET.get('order_by', 'locus')
        result = result.order_by(order)

    interactions = len(result)

    return render_to_response('browse/exp.html',
                              {'result': result, 'strain': ','.join(id), 'interactions': interactions},
                              context_instance=RequestContext(request))


def expDownload(request):
    if request.method == 'GET':
        if 'type' in request.GET and 'selected' in request.GET:
            type = request.GET['type']
            selected = request.GET['selected']
            if type == 'all':
                selected = selected.split(',')
                genomeRes = Genome.objects.filter(strain__in=selected).values_list('genomerefno')
                refList = []
                for item in genomeRes:
                    refList.append(item[0])
                result = ExpressionProfile.objects.filter(genomerefno__in=refList).order_by('locus').values()
            else:
                selected = selected.split(',')
                result = ExpressionProfile.objects.filter(locus__in=selected).values()

            response = HttpResponse(content_type="text/csv")
            response.write('\xEF\xBB\xBF')
            response['Content-Disposition'] = 'attachment; filename=exp.csv'
            writer = csv.writer(response)

            # store row title description
            rowTitle = []
            for item in expField:
                rowTitle.append(expFieldDic[item])
            writer.writerow(rowTitle)

            #get data from database
            #data = allEHFPI.objects.values()
            for item in result:
                res = []
                for i in expField:
                    # if type(item[i]) is types.UnicodeType:
                    #     res.append(item[i].encode('utf-8'))
                    # else:   #long type
                    #     res.append(item[i])
                    res.append(smart_str(item[i]))
                writer.writerow(res)
            return response

    return HttpResponseRedirect('/browse')


#expression profile detail
def expDetail(request, id):
    expResult = ExpressionProfile.objects.filter(locus=id)
    return render_to_response('browse/expDetail.html', {
        'expResult': expResult, 'id': id}, context_instance=RequestContext(request))