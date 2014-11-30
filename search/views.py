from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.db.models import *
import csv

from browse.models import *
from browse.commonVar import *


def queryDb(query, type):
    if type == 'genome':
        q = Q(genomerefno=query) | Q(genometype=query) | Q(gino=query) | Q(uidno=query) | Q(genomename=query) | Q(
            definition__icontains=query) | Q(biovar=query) | Q(strain=query)
        result = Genome.objects.filter(q)

    elif type == 'gene':
        q = Q(id=query) | Q(type=query) | Q(genomerefno=query) | Q(geneid=query) | Q(locus=query) | Q(
            genename=query) | Q(pid=query) | Q(cogno=query) | Q(product=query)
        result = Fragment.objects.filter(q)

    elif type == 'protein':
        q = Q(pid=query) | Q(refseqno=query) | Q(genomerefno=query) | Q(locus=query)
        result = Protein.objects.filter(q)

    else:#exp
        q = Q(locus=query) | Q(genomerefno=query) | Q(genename=query)
        result = ExpressionProfile.objects.filter(q)

    return result

# preview page
def preview(request):
    if request.method == 'GET':
        if 'query' in request.GET:
            query = request.GET['query']
            if query.strip() != '':
                genomeNum = len(queryDb(query, 'genome'))
                geneNum = len(queryDb(query, 'gene'))
                proteinNum = len(queryDb(query, 'protein'))
                expNum = len(queryDb(query, 'exp'))
                total = genomeNum + geneNum + proteinNum + expNum

                return render_to_response('search/preview.html',
                                          {'query': query, 'genomeNum': genomeNum, 'geneNum': geneNum,
                                           'proteinNum': proteinNum, 'expNum': expNum,'total':total},
                                           context_instance=RequestContext(request))

        return HttpResponseRedirect('/')

def geneDownload(request):
    if request.method == 'GET':
        if 'type' in request.GET and 'selected' in request.GET:
            type = request.GET['type']
            selected = request.GET['selected']
            if type == 'all':
                result = queryDb(selected,'gene')
                result = result.order_by('locus').values()
            else:
                selected = selected.split(',')
                result = NcbiGene.objects.filter(id__in=selected).values()

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

    return HttpResponseRedirect('/')

def srnaDownload(request):
    if request.method == 'GET':
        if 'type' in request.GET and 'selected' in request.GET:
            type = request.GET['type']
            selected = request.GET['selected']
            if type == 'all':
                result = queryDb(selected,'srna')
                result = result.order_by('id').values()
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

    return HttpResponseRedirect('/')

def expDownload(request):
    if request.method == 'GET':
        if 'type' in request.GET and 'selected' in request.GET:
            type = request.GET['type']
            selected = request.GET['selected']
            if type == 'all':
                result = queryDb(selected,'exp')
                result = result.order_by('locus').values()
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

    return HttpResponseRedirect('/')

def proteinDownload(request):
    if request.method == 'GET':
        if 'type' in request.GET and 'selected' in request.GET:
            type = request.GET['type']
            selected = request.GET['selected']
            if type == 'all':
                result = queryDb(selected,'protein')
                result = result.order_by('pid').values()
            else:
                selected = selected.split(',')
                result = NcbiProtein.objects.filter(pid__in=selected).values()

            response = HttpResponse(content_type="text/csv")
            response.write('\xEF\xBB\xBF')
            response['Content-Disposition'] = 'attachment; filename=protein.csv'
            writer = csv.writer(response)

            # store row title description
            rowTitle = []
            for item in proteinField:
                rowTitle.append(proteinFieldDic[item])
            writer.writerow(rowTitle)

            #get data from database
            #data = allEHFPI.objects.values()
            for item in result:
                res = []
                for i in proteinField:
                    # if type(item[i]) is types.UnicodeType:
                    #     res.append(item[i].encode('utf-8'))
                    # else:   #long type
                    #     res.append(item[i])
                    res.append(smart_str(item[i]))
                writer.writerow(res)
            return response

    return HttpResponseRedirect('/')

def snpDownload(request):
    if request.method == 'GET':
        if 'type' in request.GET and 'selected' in request.GET:
            type = request.GET['type']
            selected = request.GET['selected']
            if type == 'all':
                result = queryDb(selected,'snp')
                result = result.order_by('id').values()
            else:
                selected = selected.split(',')
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

    return HttpResponseRedirect('/')

def correspondDownload(request):
    if request.method == 'GET':
        if 'type' in request.GET and 'selected' in request.GET:
            type = request.GET['type']
            selected = request.GET['selected']
            if type == 'all':
                result = queryDb(selected,'correspond')
                result = result.order_by('id').values()
            else:
                selected = selected.split(',')
                result = GeneCorrespond.objects.filter(id__in=selected).values()

            response = HttpResponse(content_type="text/csv")
            response.write('\xEF\xBB\xBF')
            response['Content-Disposition'] = 'attachment; filename=correspond.csv'
            writer = csv.writer(response)

            # store row title description
            rowTitle = []
            for item in correspondField:
                rowTitle.append(correspondFieldDic[item])
            writer.writerow(rowTitle)

            #get data from database
            #data = allEHFPI.objects.values()
            for item in result:
                res = []
                for i in correspondField:
                    # if type(item[i]) is types.UnicodeType:
                    #     res.append(item[i].encode('utf-8'))
                    # else:   #long type
                    #     res.append(item[i])
                    res.append(smart_str(item[i]))
                writer.writerow(res)
            return response

    return HttpResponseRedirect('/')

#quick search page
def quick(request):
    if request.method == 'GET':
        if 'type' in request.GET and 'query' in request.GET:
            type = request.GET['type']
            query = request.GET['query']
            result = queryDb(query, type)
            if type == 'genome':
                result = result.order_by('genometype')
                publicationDict = {}
                for item in result:
                    pubList = item.reference.split('\n')


                    if '' in pubList:
                        pubList.remove('')
                    publicationDict[item.genomerefno] = pubList

                return render_to_response('search/genome.html',
                                          {'result': result, 'query': query, 'publicationDict': publicationDict},
                                          context_instance=RequestContext(request))
            elif type == 'gene':
                result = result.order_by('locus')
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

                return render_to_response('search/gene.html',
                                          {'result': result, 'query': query, 'geneNumber': geneNumber, 'interactions': interactions},
                                          context_instance=RequestContext(request))
            elif type == 'protein':
                result = result.order_by('pid')
                if (len(result)):
                    #sort the column
                    order = request.GET.get('order_by', 'pid')
                    result = result.order_by(order)
                interactions = len(result)
                return render_to_response('search/protein.html',
                                          {'result': result, 'query': query, 'interactions': interactions},
                                          context_instance=RequestContext(request))

            elif type == 'srna':
                result = result.order_by('id')
                if (len(result)):
                    #sort the column
                    order = request.GET.get('order_by', 'id')
                    result = result.order_by(order)

                interactions = len(result)

                return render_to_response('search/srna.html',
                                          {'result': result, 'query': query, 'interactions': interactions},
                                          context_instance=RequestContext(request))
            elif type == 'exp':
                result = result.order_by('locus')
                if (len(result)):
                    #sort the column
                    order = request.GET.get('order_by', 'locus')
                    result = result.order_by(order)

                interactions = len(result)

                return render_to_response('search/exp.html',
                                          {'result': result, 'query': query, 'interactions': interactions},
                                          context_instance=RequestContext(request))
            elif type == 'snp':
                result = result.order_by('id')
                if (len(result)):
                    #sort the column
                    order = request.GET.get('order_by', 'id')
                    result = result.order_by(order)
                interactions = len(result)
                return render_to_response('search/snp.html',
                                          {'result': result, 'query': query, 'interactions': interactions},
                                          context_instance=RequestContext(request))

            elif type == 'correspond':
                result = result.order_by('id')
                if (len(result)):
                    #sort the column
                    order = request.GET.get('order_by', 'id')
                    result = result.order_by(order)
                interactions = len(result)
                return render_to_response('search/correspond.html',
                                          {'result': result, 'query': query, 'interactions': interactions},
                                          context_instance=RequestContext(request))
            else:
                print ''



