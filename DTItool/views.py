from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


from .mongo_model import DB


db = DB()
# Create your views here.
def index(request):
    return render(request, 'DTItool/index.html')


def startup(request):
    return render(request, 'DTItool/startup.html')


def search_for_drug(request, drug_name):
    result = {
        "ok": False,
        "content": ""
    }
    dtinet_score_entries = db.get_score_entries(drug_name, 'DTInet')
    neodti_score_entries = db.get_score_entries(drug_name, 'NeoDTI')
    if dtinet_score_entries is None or neodti_score_entries is None:
        return JsonResponse(result)
    else:
        result["ok"] = True

    # temp = {'protein_id': 'O43399', 'NeoDTI_score': 0.0806670596533, 'protein_name': 'TPD52L2', 'NeoDTI_ranking': 1}
    # neodti_score_entries[0] = temp
    
    for i in dtinet_score_entries:
        for j in neodti_score_entries:
            if i['protein_id'] == j['protein_id']:
                i['NeoDTI_score'] = j['NeoDTI_score']
                i['NeoDTI_ranking'] = j['NeoDTI_ranking']
                neodti_score_entries.remove(j)
                break
            else:
                i['NeoDTI_score'] = ""
                i['NeoDTI_ranking'] = ""
    for i in neodti_score_entries:
        i['DTInet_score'] = ""
        i['DTInet_ranking'] = ""

    dtinet_score_entries += neodti_score_entries
    result["content"] = dtinet_score_entries
    print('length: ', len(dtinet_score_entries))

    return JsonResponse(result)

    
def search_for_protein(request, protein_name):
    pass