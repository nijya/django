from django.http import HttpResponse
from ratesys.models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User


@csrf_exempt
def register(request):
    info = json.loads(request.body.decode('utf-8'))
    user = info['username']
    email = info['email']
    pwd = info['password']
    User.objects.create_user(user, email, pwd)
    status = {'info': 'Successful!'}
    return HttpResponse(json.dumps(status))

@csrf_exempt
def login(request):
    info = json.loads(request.body.decode('utf-8'))
    user = info['username']
    pwd = info['password']
    user = authenticate(username=user, password=pwd)
    if user is not None:
        auth_login(request, user)
        status = {'status': 1}
    else:
        status = {'status': 0}
    return HttpResponse(json.dumps(status))

@csrf_exempt
def logout(request):
    auth_logout(request)
    info = {'status': "Successfully logged out!"}
    return HttpResponse(json.dumps(info))

def listall(request):
    modules = Module.objects.all()
    prof = {}
    for m in modules:
        profwm = Professor.objects.filter(m_id=m.m_id).all()
        for union in profwm:
            if union.m_id_id not in prof:
                prof[union.m_id_id] = set()
            prof[union.m_id_id].add(union)
    listall = []
    for m in modules:
        cur = [m.m_code, m.m_name, m.ac_year, m.semester]
        for p in prof[m.m_id]:
            cur += [p.p_code, p.p_name]
        listall.append(cur)
    dic = {}
    for i in range(len(listall)):
        dic.update({i: listall[i]})
    return HttpResponse(json.dumps(dic))


def rateall(request):
    profs = Professor.objects.all()
    li = []
    dic = {}
    for p in profs:
        ratewp = Rate.objects.filter(p_id_id=p.p_id).all().values('p_id__p_code').annotate(rate=Avg("rate"))
        for i in ratewp:
            li.append(i)
    for x in li:
        if x['p_id__p_code'] not in dic:
            dic[x['p_id__p_code']] = []
        dic[x["p_id__p_code"]].append(x["rate"])
    avg_l = []
    for i in dic.items():
        a = round(sum(list(i[1]))/len(list(i[1])))
        avg_l.append([i[0], a])
    d = {}
    for i in avg_l:
        profn = Professor.objects.filter(p_code=i[0]).all().values('p_name')
        d.update({i[0]: [profn.values()[0]['p_name'], i[1]]})
    # print(d)
    # for i in d.items():
    #     print("The rating of Professor %s (%s) is %s" % (i[1][0], i[0], i[1][1]))
    return HttpResponse(json.dumps(d))


def rateone(request):
    # http://127.0.0.1:8000/rateone/?pcode=JE1&mcode=CD1
    pcode = request.GET['pcode']
    mcode = request.GET['mcode']
    ids = Professor.objects.filter(p_code__iexact=pcode, m_id__m_code=mcode).all().values('p_id', 'm_id_id')
    pname = Professor.objects.filter(p_code=pcode).values('p_name')
    mname = Module.objects.filter(m_code=mcode).values('m_name')
    for i in pname:
        pname = i['p_name']
        break
    for i in mname:
        mname = i['m_name']
        break
    sum = 0
    flag = 0
    for id in ids:
        rates = Rate.objects.filter(p_id_id=id['p_id'], m_id_id=id['m_id_id']).all().values('rate')
        for i in rates:
            flag += 1
            sum += i['rate']
    avg = round(sum / flag)
    dic = {'pname': pname,
           'pcode': pcode,
           'mname': mname,
           'mcode': mcode,
           'avg': avg}
    print("The rating of Professor %s (%s) in module %s (%s) is %s" %(dic['pname'], dic['pcode'],
                                                                      dic['mname'], dic['mcode'],dic['avg']))
    return HttpResponse(json.dumps(dic))


def giverate(request):
    # http://127.0.0.1:8000/giverate/?pcode=JE1&mcode=CD1&year=2018&sem=2&rate=4.5
    pcode = request.GET['pcode']
    mcode = request.GET['mcode']
    year = request.GET['year']
    semester = request.GET['sem']
    rate = request.GET['rate']
    info = Professor.objects.filter(p_code__iexact=pcode, m_id__m_code=mcode,
                                   m_id__ac_year=year, m_id__semester=semester).all().values('p_id', 'm_id_id')
    p_id = 0
    m_id = 0
    for i in info:
        p_id = i['p_id']
        m_id = i['m_id_id']
    r1 = Rate(m_id_id=m_id, p_id_id=p_id, rate=rate)
    print(r1)
    r1.save()
    print("saved!")
    return HttpResponse(r1)
