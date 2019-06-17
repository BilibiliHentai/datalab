from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as f_login, logout as f_logout
from django.contrib.auth.decorators import login_required


from openpyxl import load_workbook
from io import BytesIO

from DTItool.forms import LoginForm, RegisterForm, UploadExcelForm
from DTItool.mongo_model import db
from utils import export, excel_append

GLOBAL_ENTRIES = {}
# Create your views here.
@login_required(login_url='/DTItool/login')
def index(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel = request.FILES['file']
            buffered_stream = BytesIO(excel.read())
            workbook = load_workbook(filename=buffered_stream)
            buffered_stream.close()
            excel_append.append_score(workbook)
            
            workbook.close()
            return HttpResponse('upload succeed')
        else:
            return render(request, 'DTItool/index.html', context={'form': form})
    else:
        f_logout(request)
        form = UploadExcelForm()
    return render(request, 'DTItool/index.html', context={'form': form})


@login_required(login_url='/DTItool/login')
def startup(request):
    f_logout(request)
    return render(request, 'DTItool/startup.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                f_login(request, user)
                return redirect('DTItool:startup')
            else:
                return render(request, 'DTItool/login.html', context={'form': form})
    else:
        form = LoginForm()
    return render(request, 'DTItool/login.html', context={'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            f_login(request, user)
            return redirect('DTItool:startup')
    else:
        form = RegisterForm()
    return render(request, 'DTItool/register.html', context={'form': form})


def logout(request):
    f_logout(request)
    return HttpResponse('Log out successfully.')

def search_for_drug(request, drug_name):
    result = {
        "ok": False,
        "content": {
            "DTInet": "",
            "NeoDTI": ""
        }
    }
    dtinet_score_entries = db.get_score_entries(drug_name, 'DTInet')
    neodti_score_entries = db.get_score_entries(drug_name, 'NeoDTI')
    if dtinet_score_entries is None or neodti_score_entries is None:
        return JsonResponse(result)
    else:
        result["ok"] = True

    result["content"]['DTInet'] = dtinet_score_entries
    result['content']['NeoDTI'] = neodti_score_entries

    return JsonResponse(result)


def search_for_protein(request, protein_name):
    result = {
        "ok": True,
        "content": "shit"
    }
    result['content'] = db.get_drug_entries(protein_name)
    global GLOBAL_ENTRIES
    GLOBAL_ENTRIES = {
        'protein_name': protein_name,
        'score_entries': result['content']
    }
    return JsonResponse(result)


def drug_excel(request, drug_name):
    dtinet_score_entries = db.get_score_entries(drug_name, 'DTInet')
    neodti_score_entries = db.get_score_entries(drug_name, 'NeoDTI')
    content = export.excel_both(drug_name, dtinet_score_entries, neodti_score_entries)
    response = HttpResponse(content, content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = "attachment; filename={}.xlsx".format(drug_name)

    return response


def excel_for_protein(request, protein_name):
    if GLOBAL_ENTRIES.get('protein_name') != protein_name:
        name = protein_name
        score_entries = db.get_drug_entries(protein_name)
        titles = score_entries[0].keys()
        content = export.common_singlesheet_excel(score_entries, titles, 'scores')
    else:
        name = GLOBAL_ENTRIES['protein_name']
        titles = GLOBAL_ENTRIES['score_entries'][0].keys()
        content = export.common_singlesheet_excel(GLOBAL_ENTRIES['score_entries'], titles, 'scores')
    response = HttpResponse(content, content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = "attachment; filename={} .xlsx".format('protein ' + name)
    
    return response


def drug_excel_dtinet(request, drug_name):
    dtinet_score_entries = db.get_score_entries(drug_name, 'DTInet')
    content = export.excel_dtinet(dtinet_score_entries)
    response = HttpResponse(content, content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = "attachment; filename={} DTInet.xlsx".format(drug_name)
    
    return response


def drug_excel_neodti(request, drug_name):
    neodti_score_entries = db.get_score_entries(drug_name, 'NeoDTI')
    content = export.excel_neodti(neodti_score_entries)
    response = HttpResponse(content, content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = "attachment; filename={} NeoDTI.xlsx".format(drug_name)
    
    return response


def condition_for_drug(request, drug_name, dtinet_upper_limit, dtinet_lower_limit, neodti_upper_limit, neodti_lower_limit):
    result = {
        'ok': False,
        'content': ''
    }
    dtinet_upper_limit = float(dtinet_upper_limit)
    dtinet_lower_limit = float(dtinet_lower_limit)
    neodti_upper_limit = float(neodti_upper_limit)
    neodti_lower_limit = float(neodti_lower_limit)

    dtinet_score_entries = db.get_score_entries_by_condition('DTInet', drug_name, dtinet_upper_limit, dtinet_lower_limit)
    neodti_score_entries = db.get_score_entries_by_condition('NeoDTI', drug_name, neodti_upper_limit, neodti_lower_limit)
    if dtinet_score_entries is None or neodti_score_entries is None:
        return JsonResponse(result)
    else:
        result['ok'] = True
    for dtinet in dtinet_score_entries:
        for neodti in neodti_score_entries:
            if dtinet['protein_id'] == neodti['protein_id']:
                dtinet['NeoDTI_score'] = neodti['NeoDTI_score']
            else:
                dtinet['NeoDTI_score'] = ''
    result['content'] = dtinet_score_entries
    return JsonResponse(result)


def ranking_for_drug(request, drug_name, dtinet_upper_ranking, dtinet_lower_ranking, neodti_upper_ranking, neodti_lower_ranking):
    result = {
        'ok': False,
        'content': ''
    }
    dtinet_score_entries = db.get_score_entries_by_ranking('DTInet', drug_name, dtinet_upper_ranking, dtinet_lower_ranking)
    neodti_score_entries = db.get_score_entries_by_ranking('NeoDTI', drug_name, neodti_upper_ranking, neodti_lower_ranking)

    if dtinet_score_entries is None or neodti_score_entries is None:
        return JsonResponse(result)
    else:
        result['ok'] = True
    for dtinet in dtinet_score_entries:
        for neodti in neodti_score_entries:
            if dtinet['protein_id'] == neodti['protein_id']:
                dtinet['NeoDTI_ranking'] = neodti['NeoDTI_ranking']
            else:
                dtinet['NeoDTI_ranking'] = ''
    result['content'] = dtinet_score_entries
    return JsonResponse(result)


def excel_condition(request, drug_name, dtinet_upper_limit, dtinet_lower_limit, neodti_upper_limit, neodti_lower_limit):
    dtinet_upper_limit = float(dtinet_upper_limit)
    dtinet_lower_limit = float(dtinet_lower_limit)
    neodti_upper_limit = float(neodti_upper_limit)
    neodti_lower_limit = float(neodti_lower_limit)

    dtinet_score_entries = db.get_score_entries_by_condition('DTInet', drug_name, dtinet_upper_limit, dtinet_lower_limit)
    neodti_score_entries = db.get_score_entries_by_condition('NeoDTI', drug_name, neodti_upper_limit, neodti_lower_limit)
    for dtinet in dtinet_score_entries:
        for neodti in neodti_score_entries:
            if dtinet['protein_id'] == neodti['protein_id']:
                dtinet['NeoDTI_score'] = neodti['NeoDTI_score']
            else:
                dtinet['NeoDTI_score'] = ''

    titles = dtinet_score_entries[0].keys()
    content = export.common_singlesheet_excel(dtinet_score_entries, titles, 'scores')
    response = HttpResponse(content, content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = "attachment; filename={} DTInet.xlsx".format(drug_name + ' scores advanced')
    
    return response


def excel_ranking(request, drug_name, dtinet_upper_ranking, dtinet_lower_ranking, neodti_upper_ranking, neodti_lower_ranking):
    dtinet_score_entries = db.get_score_entries_by_ranking('DTInet', drug_name, dtinet_upper_ranking, dtinet_lower_ranking)
    neodti_score_entries = db.get_score_entries_by_ranking('NeoDTI', drug_name, neodti_upper_ranking, neodti_lower_ranking)

    for dtinet in dtinet_score_entries:
        for neodti in neodti_score_entries:
            if dtinet['protein_id'] == neodti['protein_id']:
                dtinet['NeoDTI_ranking'] = neodti['NeoDTI_ranking']
            else:
                dtinet['NeoDTI_ranking'] = ''
    
    titles = dtinet_score_entries[0].keys()
    content = export.common_singlesheet_excel(dtinet_score_entries, titles, 'rankings')
    response = HttpResponse(content, content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = "attachment; filename={} DTInet.xlsx".format(drug_name + ' rankings advanced')
    
    return response

