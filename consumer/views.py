from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from . models import products,customer,comments,records,cart
from django.urls import reverse
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout,get_user_model
from datetime import datetime,timezone,timedelta
import time
from django.core.mail import send_mail
import random
from django.contrib import messages

#myfunctions
status = 'LOG IN'
l= '/c_login_form/'
previous = '/main/'
sk=''
typeu=''
lt = ''
idx=''
fl=''
cat=''
contextfp={}
contextpr={}
s=""
uemail=""
ddd={}
listcolor = ['#f02828','#ff8f00','#2ab746','#2dc5cc','#2d6bcc','#482dcc','#a22dcc','#cc2d78']


def list_gen(type_cat):
    m = set({})
    pr = products.objects.filter(p_category=type_cat).values()
    val=[]
    for a in pr:
        val.append(a['id'])
    while len(m)<8:
        m.add(random.randint(0, len(val)-1))
    lx=list(m)
    random.shuffle(lx)
    z=[]
    for x in lx:
        z.append(val[x])
    zz=[]
    for x in z:
        zz.append((products.objects.get(id=x)))
    return zz

#category_data
def category_data(request):
    global previous,sk,cat
    previous = '/category_data/'
    try:cat =request.GET["cat"]
    except: pass
    sk = cat
    flx = products.objects.filter(p_category=cat).values()
       
    seller_data = products.objects.values()
    template = loader.get_template('item.html')
    context = {'seller_data':flx,'status':status,'l':l,'sk':'Category: '+sk,'typeu' : typeu,'lt': lt,'randcolor':randcolor}
    return HttpResponse(template.render(context,request))


# Create your views here.
def index(request):
    page = loader.get_template('index.html')
    return HttpResponse(page.render({},request))
    
#MAIN PAGE
def main(request):
    global status,l,previous,sk,typeu,lt,randcolor
    data1  = list_gen('laptops')
    data2  = list_gen('tv')
    data3  = list_gen('mobiles')
    data4  = list_gen('ac')
    data5  = list_gen('camera')
    data6  = list_gen('washing machine')
    data7  = list_gen('oven')
    data8  = list_gen('refrigerator')
    data9  = list_gen('chimney')
    data10  = list_gen('gaming display')
    data11  = list_gen('water purifier')
    data12  = list_gen('tablet')

    randcolor=listcolor[random.randint(0, len(listcolor)-1)]

    previous = '/main/'
    sk = ''
    if request.user.is_authenticated:
        status = 'LOG OUT'
        l = '/c_logout/'
    if request.user.groups.filter(name='seller').exists():
        typeu = 'Sell'
        lt  = '/form/'
    else:
        typeu = 'Become a Seller'
        lt = '/s_signup_form/'
    context={
        'status':status,
        'l':l,
        'sk': sk,
        'typeu' : typeu,
        'lt': lt,
        'data1':data1,
        'data2':data2,
        'data3':data3,
        'data4':data4,
        'data5':data5,
        'data6':data6,
        'data7':data7,
        'data8':data8,
        'data9':data9,
        'data10':data10,
        'data11':data11,
        'data12':data12,
        'randcolor':randcolor,
    }

    page = loader.get_template('main.html')
    return HttpResponse(page.render(context,request))

#DATABASE:SELLER PRODUCT ENTRY FORM
def add_seller_record(request):
    a1 = request.POST['p_name_short']
    a = request.POST['p_name']
    b = request.FILES['p_image']    #new
    print(b)
    c = request.POST['p_price']
    q = request.POST['p_quantity']
    d = request.POST['p_specifications']
    e = request.POST['p_seller_name']
    cat = request.POST['p_category']
    h1 = request.POST['h1']
    h2 = request.POST['h2']
    h3 = request.POST['h3']
    h4 = request.POST['h4']
    h5 = request.POST['h5']
    tag = request.POST['c_tags']
    t = products(p_name_short=a1,p_name=a,c_tags=tag,p_quantity=q,p_category=cat,p_image=b,p_price=c,p_specifications=d,p_seller_name=e,h1=h1,h2=h2,h3=h3,h4=h4,h5=h5)
    t.save()
    return HttpResponseRedirect("/thankyou_s")

#SELLER PRODUCT ENTRY FORM
def form(request):
    if request.user.groups.filter(name='seller').exists():
        template = loader.get_template('seller_form.html')
        return HttpResponse(template.render({},request))
    else:
        return HttpResponseRedirect('/main/')


#SEARCH
def search(request):
    global previous,sk,fl
    previous = '/search/'
    if request.method == "POST":
        e = request.POST['search_key']
        if(e == ""):
            return HttpResponseRedirect('/main/')
        sk = e
        e = set(e.casefold().split(' '))
        product_list=products.objects.values()
        result_ids={}
        for x in product_list:
            tag_set = set(x['c_tags'].casefold().split(','))
            intersection = e.intersection(tag_set)
            if len(intersection)!=0:
                result_ids.update({x['id']:len(intersection)})
        result_ids = sorted(result_ids.items(),key=lambda x:x[1])
        lp=[]
        for x in result_ids:
            lp.append(x[0])
        fl=[]
        lp.reverse()
        for x in lp:
            fl.append((products.objects.get(id=x))) 
        
    
    return HttpResponseRedirect('/search_result/')

def search_result(request):
    template = loader.get_template('item.html')
    context = {'seller_data':fl,'status':status,'l':l,'sk':sk,'typeu' : typeu,'lt': lt,'randcolor':randcolor}
    return HttpResponse(template.render(context,request))


#ITEM_DETAILED VIEW
def item_detailed(request):
    global previous,sk,idx
    sk =''
    try: idx =request.GET["id"];previous = '/item_detailed/?id='+str(idx) #enhance: sending previous through link
    except: pass
    username = request.user.username
    if(request.user.is_authenticated):
        if  cart.objects.filter(cart_item=idx,username_cart=username).exists():  
                p ="REMOVE FROM CART"
                pl ="/remove_cart/"
        else:
                p = "ADD TO CART"
                pl = "/cart/"
        
    else:
        p = "ADD TO CART"
        pl = "/cart/"
    seller_data = products.objects.filter(id=idx)
    all_comments = comments.objects.filter(p_id=idx).order_by('-id')
    template = loader.get_template('item_detailed.html')
    context = {'seller_data':seller_data,'status':status,'comments':all_comments,'l':l,'sk':sk,'typeu' : typeu,'lt': lt,'p':p,'pl':pl,'randcolor':randcolor}
    return HttpResponse(template.render(context,request))

#BUY
def buy_form(request):
    
    if request.user.is_authenticated:
        username = request.user.username
        template = loader.get_template('buy.html')
        x=customer.objects.get(c_name=username)
        maxq =  products.objects.get(id = idx)
        maxq = maxq.p_quantity
        context={ 'email':x.c_email,'address':x.c_address,'maxq':maxq}
        return HttpResponse(template.render(context,request))
    else :
        return HttpResponseRedirect('/c_login_form')

def buy(request):
    username = request.user.username
    product = idx
    quanity  = request.POST['quantity']
    c_datetime = datetime.now()
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    payment_method = request.POST['payment_method']
    address = request.POST['address']

    t=records(username=username,product=product,quanity=quanity,c_datetime=c_datetime,name=name,email=email,phone=phone,payment_method=payment_method,address=address)
    t.save()
    data = products.objects.get(id=product)
    data.p_quantity = data.p_quantity - int(quanity)
    data.save()
    send_mail('Order', f'Hi {name},\n\nOrder succsessfully placed @{c_datetime.strftime("%d/%b/%Y, %H:%M:%S")}\n\nYour order will be delievered by {(datetime.now() +timedelta(5)).strftime("%d/%b/%Y") } \n\n Thank you for shopping with Flipkart\n\n\nOrder:\n\n{data.p_name}\n', 'asianman78607@gmail.com', [email])
    if(data.p_quantity)==0:
        data.delete()
    return HttpResponseRedirect("/thankyou_c")

#Forgotpassword
def forgot_password_form(request):
    return render(request,"forgot_password.html")

def forgot_password(request):
    global uemail
    uemail = request.POST['email']
    emails = get_user_model()
    if emails.objects.filter(email=uemail).exists():
        global s
        while len(s)<7:
            s=str(random.randint(0, 9))+ s

        send_mail('Password Reset', f'Code for password reset: {s}', 'asianman78607@gmail.com', [uemail])
    else:
        time.sleep(5)
    return HttpResponseRedirect('/password_reset/')

def password_reset(request):
    template = loader.get_template('password_reset.html')
    return HttpResponse(template.render(contextpr,request))
def new_password(request):
    code = request.POST['code']
    if code==s:
        return HttpResponseRedirect('/set_new_password/')
    else:
        global contextpr
        contextpr = {'line':'Invalid Code !'}
        return HttpResponseRedirect('/password_reset/')

def set_new_password(request):
    return render(request,"set_new_password.html")

def update_new_password(request):
    global contextfp
    password = request.POST['password']
    u = User.objects.get(email=uemail)
    u.set_password(password)
    u.save()
    contextfp={}
    if u.groups.filter(name='seller').exists():
        return HttpResponseRedirect('/s_login_form/')
    else:
        return HttpResponseRedirect('/c_login_form/')


#thank
def thankyou_c(request):
    return render(request,"thankyou_c.html")

def thankyou_s(request):
    return render(request,"thankyou_s.html")

#LOG SYSTEM
def c_login_form(request):
    template = loader.get_template('customer_login.html')
    return HttpResponse(template.render(contextfp,request))

def s_login_form(request):
    template = loader.get_template('seller_login.html')
    return HttpResponse(template.render(contextfp,request))

def c_signup_form(request):
    try:
        global contextfp,ddd
        contextfp ={}
        template = loader.get_template('customer_signup.html')
        return HttpResponse(template.render(ddd,request))
    finally: ddd={}

def s_signup_form(request):
    try:
        global contextfp,ddd
        contextfp ={}
        template = loader.get_template('seller_signup.html')
        return HttpResponse(template.render(ddd,request))
    finally: ddd={}

def s_signup(request):
    global ddd
    a = request.POST['s_name']
    b = request.POST['s_email']
    d = request.POST['s_address']
    if User.objects.filter(username=a).exists():
        ddd={'gg': "Username alreagy taken! Try another",'a':a,'b':b,'c':d}
        return HttpResponseRedirect('/s_signup_form/')
    if User.objects.filter(email=b).exists():
        ddd={'gg': f"Account with email: {b} already exists!",'a':a,'b':b,'c':d}
        return HttpResponseRedirect('/s_signup_form/')
    c = request.POST['s_password']

    t = customer(c_name=a,c_email=b,c_address=d)
    t.save()
    user = User.objects.create_user(a,b,c)
    user.save()
    g = Group.objects.get(name='seller')
    g.user_set.add(user)
    return HttpResponseRedirect('/s_login_form/')

def c_signup(request):
    global ddd
    a = request.POST['c_name']
    b = request.POST['c_email']
    d = request.POST['c_address']

    if User.objects.filter(username=a).exists():
        ddd={'gg': "Username alreagy taken! Try another",'a':a,'b':b,'c':d}
        return HttpResponseRedirect('/c_signup_form/') 
    if User.objects.filter(email=b).exists():
        ddd={'gg': f"Account with email: {b} already exists!",'a':a,'b':b,'c':d}
        return HttpResponseRedirect('/c_signup_form/')
    c = request.POST['c_password']

    t = customer(c_name=a,c_email=b,c_address=d)
    t.save()
    user = User.objects.create_user(a,b,c)
    user.save()
    return HttpResponseRedirect('/c_login_form/')

def c_login(request):
    global l,status,typeu,lt,contextfp
    b = request.POST['username']
    c = request.POST['c_password']
    user = authenticate(username=b, password=c)
    if user is not None:
        status = 'LOG OUT'
        l = '/c_logout/'
        if user.groups.filter(name='seller').exists():
            typeu = 'Sell'
            lt  = '/form/'
        login(request,user)
        contextfp ={}
        return HttpResponseRedirect(previous)
        
        
    else:
        contextfp={'m':'/forgot_password_form/','lf':'Forgot password ?'}
        return HttpResponseRedirect('/c_login_form/')
        

#LOGOUT
def c_logout(request):
    logout(request)
    global status,l
    status = 'LOG IN'
    l= '/c_login_form/'
    return HttpResponseRedirect('/main/')

def add_comment(request):
    if request.user.is_authenticated:
        a = request.POST['comment']
        b = request.user.username
        c = datetime.now()
        t = comments(comment=a,username_comment=b,c_datetime=c,p_id=idx)
        
        t.save()
        return HttpResponseRedirect(previous)
    else:
        return HttpResponseRedirect('/c_login_form')

def showcart(request):
    if request.user.is_authenticated:
        username = request.user.username
        template = loader.get_template('cart.html')

        data = cart.objects.filter(username_cart=username).values()
        ll=[]
        for x in data:
            ll.append(x['cart_item'])

        data = products.objects.filter(id__in=ll)
        context = {'seller_data':data,'status':status,'l':l,'sk':sk,'typeu' : typeu,'lt': lt,'randcolor':randcolor,}
        return HttpResponse(template.render(context,request))
    else :
        return HttpResponseRedirect('/c_login_form')

def add_cart(request):
    username = request.user.username
    if  cart.objects.filter(cart_item=idx,username_cart=username).exists():
        return HttpResponseRedirect('/item_detailed')

    if request.user.is_authenticated:
        c = datetime.now()
        q = cart(cart_item=idx,username_cart=username,c_datetime=c)
        q.save()
        return HttpResponseRedirect('/item_detailed')
    else :
        return HttpResponseRedirect('/c_login_form')

def remove_cart(request):
    cart.objects.filter(username_cart = request.user.username,cart_item=idx).delete()
    return HttpResponseRedirect(previous)

