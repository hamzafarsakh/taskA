from django.http import JsonResponse, HttpRequest
from django.shortcuts import render

from django.shortcuts import render,redirect
from .models import *
import bcrypt
from django.contrib import messages


# --------------------------------
def index(request):
    if request.session:
        x= request.session
        x.delete()
    request.session['id']=-1
    return render(request,'index.html')

# def show_login_page(request):
#     return render(request, "login.html ")

def dashboard(request):
    if  request.session['id'] < 0 :
        return redirect('/')
    else:
        context={
            'customers': Customer.objects.all(),
            'theUser': User.objects.get(id = request.session['id']),
            'services': Service.objects.all(),
        }
        return render(request,'dashboard.html',context)





# ----------------------------- login register page start
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0 :
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pwd_hash = bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(fname=fname,lname=lname,email=email,pwd_hash=pwd_hash)
        request.session['id'] = user.id
        request.session['fname'] = fname
        return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        email = request.POST['email']
        user = User.objects.filter(email=email)
        request.session['fname'] = user[0].fname
        request.session['id'] = user[0].id
        return redirect('/dashboard')
# def login(request):
#     if request.method == "POST":
#         user = User.objects.filter(email=request.POST["email"]).first()
#         if user:
#             if bcrypt.checkpw(
#                 request.POST["pwd"].encode(), user.pwd_hash.encode()
#             ):
#                 request.session["newUser"] = user.id
#                 return JsonResponse({"success": True})
#             else:
#                 return JsonResponse(
#                     {"success": False, "errors": ["Invalid email or password"]}
#                 )
#         else:
#             return JsonResponse(
#                 {"success": False, "errors": ["Invalid email or password"]}
#             )
#     return JsonResponse({"success": False, "errors": ["please try again"]})
# ------------------------------------login register page end









# -----------------------------------Customer Page start
def addCustomerPage(request):
    if  request.session['id'] < 0 :
        return redirect('/')
    else:
        context={
            
            'theUser': User.objects.get(id = request.session['id']),
        }
        return render(request,'newCustomer.html',context)


def addCustomer(request):
    errors = Customer.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/addCustomerPage')
    else:
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        user = User.objects.get(id = request.session['id'])
        
        Customer.objects.create(fname = fname, lname = lname,
                                 email = email, phone = phone,
                                   address = address, user = user)
    return redirect('/dashboard')


def updateCustomerPage(request, custId):
    if  request.session['id'] < 0 :
        return redirect('/')
    else:
        myActives1 =  Active.objects.filter(customer = Customer.objects.get(id = custId))
        myActives = []
        myActives2 = []
        for active in myActives1:
            myActives.append(active.service)
            myActives2.append(active)
            

        context={
            'theCustomer': Customer.objects.get(id = custId),
            'services': Service.objects.all(),
            'myActives': myActives,
            'custId': custId,
            'myActives2': myActives2,
        }

        return render(request,'editCustomer.html',context)


def updateCustomer(request, custId):
    errors = Customer.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/updateCustomerPage')
    else:
        # if request.POST['service']:
        #     return redirect('/updateCustomerPage/' + str(custId))
        print("123"*30)
        # print(request.POST['service'])
        # service = Service.objects.get(id = int(request.POST['service']))
        customer = Customer.objects.get(id = custId)

        # active = Active.objects.create(isActive = True, 
        #                                service = service,
        #                                customer = customer)

        customer.fname = request.POST['fname']
        customer.lname = request.POST['lname']
        customer.email = request.POST['email']
        customer.phone = request.POST['phone']
        customer.address = request.POST['address']
        
        user = User.objects.get(id = request.session['id'])
        customer.save()
        
    return redirect('/updateCustomerPage/' + str(custId))

def deleteCustomer(request, custId):
    customer = Customer.objects.get(id = custId)
    customer.delete()
    return redirect("/dashboard")
# --------------------------------------------------------Customer Page end



# -----------------------------------Service  start
def addServicePage(request):
    if  request.session['id'] < 0 :
        return redirect('/')
    else:
        context={
            
            'theUser': User.objects.get(id = request.session['id']),
        }
        return render(request,'newService.html',context)


def addService(request):
    errors = Service.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/addServicePage')
    else:
        name = request.POST['name']
        desc = request.POST['desc']
        price = request.POST['price']
        isactive = request.POST['isActive']
        if isactive == 't':
            isActive = True
        elif isactive == 'f':
            isActive = False

        user = User.objects.get(id = request.session['id'])
        
        Service.objects.create(name = name, desc = desc,
                                 price = price, isActive = isActive,
                                     user = user)
    return redirect('/dashboard')

def activation(request, ActiveID, custId):
    myActive =  Active.objects.get(id = ActiveID)
    # print(myActive)
    # print("*5"*50)

    if myActive.isActive == True:
        myActive.isActive = False
        myActive.save()
    else:
        myActive.isActive = True
        myActive.save()
    return redirect("/updateCustomerPage/" + str(custId))

def addServiceToCus(request, servId, custId):

    service = Service.objects.get(id = int(servId))
    customer = Customer.objects.get(id = custId)
    active = Active.objects.create(isActive = True, 
                                service = service,
                                customer = customer)
    return redirect("/updateCustomerPage/" + str(custId))

# ------------------------------------Service  end


# ---------------------search Customer start
def search(request):
    request.session['se'] = request.GET['q']
    return redirect('/result')



def result(request):
    se = request.session['se']
    re1 = Customer.objects.filter(fname = se)
    re2 = Customer.objects.filter(lname = se)
    re3 = Customer.objects.filter(email = se)
    re4 = re1.union(re2)
    re5 = re4.union(re3)
    re6 = []

    for i in re5:
        if i not in re6:
            re6.append(i)

    if re1 or re2 or re3:
        te = 1
    else:
        te = 0
    context = {
        're1':re1,
        're2':re2,
        're3':re3,
        're6':re6,
        'te':te,
    }
    return render(request,'result.html',context)
# --------------------------------end Customer search




# --------------------------------------------------------Service Page end


# def delete(request,paintingId):
#     painting = Painting.objects.get(id = paintingId)
#     painting.delete()
#     return redirect('/paintings')

# -------------------------------------

def logout(request):
    if request.session:
        x= request.session
        x.delete()
    return redirect('/')