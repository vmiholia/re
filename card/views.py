from django.shortcuts import render, redirect, get_object_or_404
from .models import student_detail, student_marks, stclass, studentid, student_marks12, nalanda
from .forms import selectclass, selectclass2
def roman(num):
    if num=='1':
        return('I')
    elif num=='2':
        return('II')
    elif num=='3':
        return('III')
    elif num=='4':
        return('IV')
    elif num=='5':
        return('V')
    elif num=='6':
        return('VI')
    elif num=='7':
        return('VII')
    else:
        return('VIII')

def datecon(dt):
    dt=dt.split("/")
    ws=dt[1]+"-"+dt[0]+"-"+dt[2]
    return(ws)

def datecon1(dt):
    dt=dt.split("-")
    ws=dt[2]+"-"+dt[1]+"-"+dt[0]
    return(ws)

def puregrade(temp):
    a=temp.split('(')
    return(a[0])
def getdet(userid,flid):
    try:
        d = (student_detail.objects.filter(userid=userid).get(fieldid=flid)).data
    except student_detail.DoesNotExist:
        d = " "
    return(d)

def detail(cl,userid):#to return details of selected student
    attd = getdet(userid,10)
    rolln = getdet(userid,9)
    temp = stclass.objects.get(id=cl).classname
    temp = temp.split()
    if len(temp)>1:
        sect = temp[1]
    else:
        sect = " "
    cld = roman(temp[0])
    dob = getdet(userid,1)
    
    if "/" in dob:
        dob = datecon(dob)
    elif "-" in dob:
        dob = datecon1(dob)
    else:
        dob = " "

    try:
        name = (student_detail.objects.filter(userid=userid).get(fieldid='1')).firstname
    except student_detail.DoesNotExist:
        name = " "
    details={
            'name' : name,
            'dob' : dob,
            'fname' : getdet(userid,2),
            'mname' : getdet(userid,3),
            'admno' : getdet(userid,4),
            }
    details['rolln'] = rolln
    details['attd'] = attd
    details['cld'] = cld
    details['sect'] = sect
    return(details)

def getgrade(userid,sub,gradeitem):
    try:
        marks=(student_marks.objects.filter(userid=userid).filter(coursename=sub).get(gradebookitem=gradeitem)).grade
    except student_marks.DoesNotExist:
        marks=0
    if marks=='NULL':
        marks=0
    if marks is None:
        marks=0
    return(round(float(marks)))

def getPT1(userid,sub):
    ept1 = getgrade(userid,sub,'PT 1')
    ept2 = getgrade(userid,sub,'PT 2')
    ePT1 = round((max(int(ept1),int(ept2)))/2)
    return(ePT1)

def makegrade(cl,num):
    cl=int(cl)
    if cl>6 and cl<16:
        num=num*1.25
    if num>90:
        g="A1"
    elif num>80 and num<91:
        g="A2"
    elif num>70 and num<81:
        g="B1"
    elif num>60 and num<71:
        g="B2"
    else:
        g="C"
    return(g)

def getsub(userid,cl,sub):
    if int(cl)>=16:
        pt1 = getPT1(userid,sub) 
    else:
        pt1 = int(getgrade(userid,sub, 'PT'))
    pt3 = int(getgrade(userid,sub,'PT 3'))
    pt2 = round(pt3/2)
    ns1 = int(getgrade(userid,sub,'NS 1'))
    ns2 = int(getgrade(userid,sub,'NS 2'))
    sea1 = int(getgrade(userid,sub,'SEA 1'))
    sea2 = int(getgrade(userid,sub,'SEA 2'))
    mt = int(getgrade(userid,sub,'Half Yearly'))
    ann = int(getgrade(userid,sub, 'Annual'))
    mo1 = pt1+ns1+sea1+mt
    mo2 = pt2+ns2+sea2+ann
    t1 = round(mo1/2)
    t2 = round(mo2/2)
    total = t1+t2
    grade1 = makegrade(cl,mo1)
    grade2 = makegrade(cl,mo2)
    grade3 = makegrade(cl,total)
    data=[pt1,ns1,sea1,mt,mo1,grade1,pt2,ns2,sea2,ann,mo2,grade2,t1,t2,total,grade3]
    return(data)

def getcom(userid,field):
    try:
        g=(student_marks.objects.filter(userid=userid).filter(coursename='Class').get(gradebookitem=field)).grade
    except student_marks.DoesNotExist:
        g=0
    if g=='NULL':
        g=0
    if g is None:
        g=0
    g=round(float(g))
    return(g)

def database(cl,userid):
    comhy = getgrade(userid,'Computer','Half Yearly')
    compt2 = getgrade(userid,'Computer','PT II')
    compra = getgrade(userid,'Computer','Practical')
    comann = getgrade(userid,'Computer','Annual')
    comT1 = comhy
    comT2 = int(compt2)+int(compra)+int(comann)
    comG1 = makegrade(cl,comT1*1.67)
    comG2 = makegrade(cl,comT2*1.67)
    com=[comG1,comG2]

    gkhy = getgrade(userid,'GK','Half Yearly')
    gkpt2 = getgrade(userid,'GK','PT II')
    gkann = getgrade(userid,'GK','Annual')  
    gkT1 = gkhy
    gkT2 = int(gkpt2)+int(gkann)
    gkG1 = makegrade(cl,gkT1*2.5)
    gkG2 = makegrade(cl,gkT2*2.5)
    gk=[gkG1,gkG2]

    drhy = getgrade(userid,'Drawing','Half Yearly')
    drpt2 = getgrade(userid,'Drawing','PT II')
    drann = getgrade(userid,'Drawing','Annual')  
    drT1 = drhy
    drT2 = int(drpt2)+int(drann)
    drG1 = makegrade(cl,drT1*2)
    drG2 = makegrade(cl,drT2*2)
    dr=[drG1,drG2]

    eng = getsub(userid,cl,'English')
    hi = getsub(userid,cl,'Hindi')
    math = getsub(userid,cl,'Maths')
    if int(cl)>=13:
        sans = getsub(userid,cl,'Sanskrit')
        soc = getsub(userid,cl,'Social')
        sci = getsub(userid,cl,'Science')
    else:
        evs = getsub(userid,cl,'EVS')

    we1 = getcom(userid,'Work Education')
    we2 = getcom(userid,'Work Education 2')
    weg1 = scale(we1)
    weg2 = scale(we2)
    we=[weg1,weg2]

    ae1 = getcom(userid,'Art Education')
    ae2 = getcom(userid,'Art Education 2')
    aeg1 = scale(ae1)
    aeg2 = scale(ae2)
    ae = [aeg1,aeg2]

    hap1 = getcom(userid,'Health and Physical Education')
    hap2 = getcom(userid,'Health and Physical Education 2')
    hapg1 = scale(hap1)
    hapg2 = scale(hap2)
    hap = [hapg1,hapg2]

    dis1 = getcom(userid,'Discipline')
    dis2 = getcom(userid,'Discipline 2')
    disg1 = scale(dis1)
    disg2 = scale(dis2)
    dis = [disg1,disg2]
    try:
        rem = (student_marks.objects.filter(userid=userid).filter(coursename='Class').get(gradebookitem='Remarks')).substring
    except student_marks.DoesNotExist:
        rem = " "
    try:
        partic = (student_marks.objects.filter(userid=userid).filter(coursename='Class').get(gradebookitem='Participation In')).substring
    except student_marks.DoesNotExist:
        try:
            partic = (student_marks.objects.filter(userid=userid).filter(coursename='Class').get(gradebookitem='Participation in')).substring
        except student_marks.DoesNotExist:
            partic = " "
    

    data = {
        'com' : com,
        'gk' : gk,
        'dr' : dr,
        'eng' : eng,
        'hin' : hi,
        'math' : math,
        'we' : we,
        'ae' : ae,
        'hap' : hap,
        'dis' : dis,
        'rem' : rem,
        'partic' : partic,
    }
    if int(cl)>=13:
        data['sans'] = sans
        data['soc'] = soc
        data['sci'] = sci
    else:
        data['evs'] = evs

    return(data)

def getgrade12(userid,sub,des,term):
    try:
        sub0 = student_marks12.objects.filter(userid=userid).filter(subject=sub).filter(description=des).filter(term=term)
    except student_marks12.DoesNotExist:
        return(" ")
    if len(sub0) == 0:
        return(" ")
    temp = []
    for su in sub0:
        ls=[]
        ls.append(su.modified)
        ls.append(su.id)
        temp.append(ls)
    temp.sort(reverse=True)
    grad = student_marks12.objects.get(id=temp[0][1]).grade
    grad = puregrade(grad)
    return(grad)

def getterm(userid,sub,des):
    pt1 = getgrade12(userid,sub,des,'PT1')
    pt2 = getgrade12(userid,sub,des,'PT2')
    pt3 = getgrade12(userid,sub,des,'PT3')
    pt4 = getgrade12(userid,sub,des,'PT4')
    pt5 = getgrade12(userid,sub,des,'Annual')
    return([pt1,pt2,pt3,pt4,pt5])

def getpers(userid,sub,des,term):
    ann1 = getgrade12(userid,sub,des,term)
    term = term + " 2"
    ann2 = getgrade12(userid, sub, des, term)
    return([ann1,ann2])

def get12enghin(userid,sub):
    sub0 = getterm(userid, sub ,'READING SKILLS - PRONUNCIATION & FLUENCY')
    sub1 = getterm(userid, sub, 'READING SKILLS - COMPREHENSION')
    sub2 = getterm(userid, sub, 'WRITING SKILLS - LITERATURE')
    sub3 = getterm(userid, sub, 'WRITING SKILLS - GRAMMAR')
    sub4 = getterm(userid, sub, 'WRITING SKILLS - DICTIONARY/VOCABULARY')
    sub5 = getterm(userid, sub, 'WRITING SKILLS - HAND WRITING & ASSIGNMENTS')
    sub6 = getterm(userid, sub, 'SPEAKING SKILLS - RECITATION/STORY TELLING')
    sub7 = getterm(userid, sub, 'SPEAKING SKILLS - CONVERSATION')
    sub8 = getterm(userid, sub, 'LISTENING SKILLS - COMPREHENSION')
    return([sub0,sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8])

def getextra(userid,des,term):
    try:
        sub0 = student_marks12.objects.filter(userid=userid).filter(subject='Class').filter(description=des).filter(term=term)
    except student_marks12.DoesNotExist:
        return(" ")
    if len(sub0) == 0:
        return(" ")
    temp = []
    for su in sub0:
        ls=[]
        ls.append(su.modified)
        ls.append(su.id)
        temp.append(ls)
    temp.sort(reverse=True)
    grad = student_marks12.objects.get(id=temp[0][1]).remark
    return(grad)

def database12(cl,userid):
    eng=get12enghin(userid,'English')
    hin=get12enghin(userid,'Hindi')
    mat0=getterm(userid,'Maths','CONCEPT')
    mat1=getterm(userid,'Maths','ACTIVITY')
    mat2=getterm(userid,'Maths','TABLE')
    mat3=getterm(userid,'Maths','CLASS & HOME ASSIGNMENTS')
    mat=[mat0,mat1,mat2,mat3]
    evs=getterm(userid,'Other','EVS')
    act=getterm(userid,'Other','Activity/Project')
    gk=getterm(userid,'Other','GK')
    com=getterm(userid,'Other','Computer')
    dra=getterm(userid,'Other','Drawing')
    ved=getterm(userid,'Other','Value Education')

    mus0=getextra(userid,'MUSIC/DANCE','Co-Curricular Activities')
    mus1=getextra(userid,'MUSIC/DANCE','Co-Curricular Activities 2')
    art0=getextra(userid,'ART & CRAFT','Co-Curricular Activities')
    art1=getextra(userid,'ART & CRAFT','Co-Curricular Activities 2')
    spo0=getextra(userid,'SPORTS','Co-Curricular Activities')
    spo1=getextra(userid,'SPORTS','Co-Curricular Activities 2')
    mus=[mus0,mus1]
    art=[art0,art1]
    spo=[spo0,spo1]

    court=getpers(userid,'Class','COURTEOUSNESS','Personal and Social Traits')
    conf=getpers(userid,'Class','CONFIDENCE', 'Personal and Social Traits')
    care=getpers(userid,'Class','CARE OF BELONGINGS', 'Personal and Social Traits')
    neat=getpers(userid,'Class','NEATNESS', 'Personal and Social Traits')
    regu=getpers(userid,'Class','REGULARITY(Attendance)', 'Personal and Social Traits')
    neat=getpers(userid,'Class','NEATNESS', 'Personal and Social Traits')
    shar=getpers(userid,'Class','SHARING & CARING', 'Personal and Social Traits')
    res=getpers(userid,'Class','CARE OF OTHERS PROPERTY','Personal and Social Traits')
    disip=getpers(userid,'Class','DISCIPLINE','Personal and Social Traits')

    try:
        partic0 = (student_marks.objects.filter(userid=userid).filter(coursename='Class').get(gradebookitem='Specific Participation')).substring
    except student_marks.DoesNotExist:
        partic0 = " "
    
    try:
        partic1 = (student_marks.objects.filter(userid=userid).filter(coursename='Class').get(gradebookitem='Specific Participation 2')).substring
    except student_marks.DoesNotExist:
        partic1 = " "
    part=[partic0,partic1]
    try:
        grem0 = (student_marks.objects.filter(userid=userid).filter(coursename='Class').get(gradebookitem='General Remarks')).substring
    except student_marks.DoesNotExist:
        grem0 = " "
    
    try:
        grem1 = (student_marks.objects.filter(userid=userid).filter(coursename='Class').get(gradebookitem='General Remarks 2')).substring
    except student_marks.DoesNotExist:
        grem1 = " "

    grem=[grem0,grem1]

    data = {
        'eng' : eng,
        'hin' : hin,
        'mat' : mat,
        'evs' : evs,
        'act' : act,
        'gk' : gk,
        'com' : com,
        'dra' : dra,
        'ved' : ved,
        'mus' : mus,
        'art' : art,
        'spo' : spo,
        'court' : court,
        'conf' : conf,
        'care' : care,
        'neat' : neat,
        'regu' : regu,
        'shar' : shar,
        'res' : res,
        'disip' : disip,
        'part' : part,
        'grem' : grem,
    }
    return(data)
    
    

def stlist(cl): #to return students in a class 'cl'
    studlist=studentid.objects.filter(sclass_id=cl)
    return(studlist)

def home(request):
    form = selectclass(request.POST or None)
    if form.is_valid():
        cl=form.cleaned_data.get('Class')
        cl="/"+cl + '/0/2/'
        return redirect(cl)
    return render(request,'basicpage.html',{'form':form})

def reportcard(request,cl,start, end ):
    studlist=stlist(cl)
    total=len(studlist)
    lst=[]
    start= int(start)
    end = int(end)
    #print("Wait!")
    #studlist = [1662, 1664, 1665]
    for stud in studlist[start:end]:
        st=[]
        userid=stud.userid
        #userid=stud
        studet=detail(cl,userid)
        if int(cl)<7:
            data=database12(int(cl),userid)
        else:    
            data=database(cl,userid)
        st=[userid,studet,data]
        lst.append(st)

    context = {
        'total' : total,
        'lst' : lst,
    }   
    
    #print("Query Completed.")

    '''print("student------",lst[0])
    print("userid------",lst[0][0])
    print("detdic-------",lst[0][1])
    print("inside detdic-------",lst[0][1]['name'])
    print("data------",lst[0][2])
    print("inside data-----",lst[0][2]['eng'])
    print("inside subject-----",lst[0][2]['eng'][0])'''

    if int(cl)>=16:
        return render(request,'89.html',context)
    elif int(cl)<16 and int(cl)>=13:
        return render(request,'5.html',context)
    elif int(cl)<13 and int(cl)>=7:
        return render(request,'34.html',context)
    else:
        return render(request,'12.html',context)

def getmarks(userid,sub,gbooki):
    try:
        sub0 = nalanda.objects.filter(userid=userid).filter(subject=sub).filter(gradebookitem=gbooki)
    except nalanda.DoesNotExist:
        return(0)
    if len(sub0) == 0:
        return(0)
    temp = []
    for su in sub0:
        ls=[]
        ls.append(su.modified)
        ls.append(su.id)
        temp.append(ls)
    temp.sort(reverse=True)
    grad = nalanda.objects.get(id=temp[0][1]).grade
    if grad=="NULL":
        grad=0
    if grad is None:
        grad=0
    return(round(float(grad)/2))

def getmarks1(userid,sub,gbooki):
    try:
        sub0 = nalanda.objects.filter(userid=userid).filter(subject=sub).filter(gradebookitem=gbooki)
    except nalanda.DoesNotExist:
        return(0)
    if len(sub0) == 0:
        return(0)
    temp = []
    for su in sub0:
        ls=[]
        ls.append(su.modified)
        ls.append(su.id)
        temp.append(ls)
    temp.sort(reverse=True)
    grad = nalanda.objects.get(id=temp[0][1]).grade
    if grad=="NULL":
        grad=0
    if grad is None:
        grad=0
    return(round(float(grad)))

def makegradenal(num):
    if num>90:
        g="A1"
    elif num>80 and num<91:
        g="A2"
    elif num>70 and num<81:
        g="B1"
    elif num>60 and num<71:
        g="B2"
    else:
        g="C"
    return(g)

def getsubnal(userid,sub):
    ut1 = getmarks(userid,sub,'Unit Test 1')
    ut2 = getmarks(userid,sub,'Unit Test 2')
    ut3 = getmarks(userid,sub,'Unit Test 3')
    ut4 = getmarks(userid,sub,'Unit Test 4')
    mt = getmarks(userid,sub,'Mid Term')
    et = getmarks(userid,sub,'End Term')
    mo = ut1+ut2+ut3+ut4+mt+et
    gr = makegradenal(mo)
    return([ut1,ut2,mt,ut3,ut4,et,mo,gr])

def scale(num):
    if num==1:
        return('A')
    elif num==2:
        return('B')
    elif num==3:
        return('C')
    else:
        return(' ')

def getscholdis(userid,gbki):
    t1 = getmarks1(userid,'Class',gbki)
    gbki = gbki + " 2"
    t2 = getmarks1(userid,'Class',gbki)
    gr1 = scale(t1)
    gr2 = scale(t2)
    return([gr1,gr2])


def databasenal(cl,userid):
    eng=getsubnal(userid,'English')
    hin=getsubnal(userid,'Hindi')
    san=getsubnal(userid,'Sanskrit')
    mat=getsubnal(userid,'Maths')
    sci=getsubnal(userid,'Science')
    soc=getsubnal(userid,'Social')
    gk=getsubnal(userid,'General')
    dra=getsubnal(userid,'Drawing')
    com=getsubnal(userid,'Computer')
    we=getscholdis(userid,'Work Education')
    ae=getscholdis(userid,'Art Education')
    hp=getscholdis(userid,'Health & Physical Education')
    dis=getscholdis(userid,'Discipline')
    nea=getscholdis(userid,'Neatness')
    cond=getscholdis(userid,'Conduct')
    hw=getscholdis(userid,'Home Work')
    try:
        partic = (nalanda.objects.filter(userid=userid).filter(subject='Class').get(gradebookitem='Participation In')).substring
    except nalanda.DoesNotExist:
        partic = " "
    try:
        rema = (nalanda.objects.filter(userid=userid).filter(subject='Class').get(gradebookitem='Remarks')).substring
    except nalanda.DoesNotExist:
        rema = " "
    data = {
        'eng' : eng,
        'hin' : hin,
        'mat' : mat,
        'san' : san,
        'sci' : sci,
        'soc' : soc,
        'gk' : gk,
        'com' : com,
        'dra' : dra,
        'we' : we,
        'ae' : ae,
        'hp' : hp,
        'cond' : cond,
        'hw' : hw,
        'nea' : nea,
        'dis' : dis,
        'partic' : partic,
        'rema' : rema,
    }
    return(data)

def home2(request):
    form = selectclass2(request.POST or None)
    if form.is_valid():
        cl=form.cleaned_data.get('Class')
        cl="/nalanda/"+cl
        return redirect(cl)
    return render(request,'basicpage.html',{'form':form})

def viewnalanda(request,cl):
    studlist=stlist(cl)
    total=len(studlist)
    lst=[]
    cl=int(cl)
    #print("Wait!")
    #studlist = [3577,3578]
    for stud in studlist:
        st=[]
        userid=stud.userid
        #userid=stud
        studet=detail(cl,userid)
        data=databasenal(int(cl),userid)
        st=[userid,studet,data]
        lst.append(st)

    context = {
        'total' : total,
        'lst' : lst,
    }   
    
    #print("Query Completed.")
    return render(request,'nalanda.html',context)
