"""      Please refer to the license file for complete details. 
  *      Project: OpenPy
  *      Developer: Yash Lamba
  *      Institute: Indraprastha Institute of Information Technology, Delhi
  *      Advisor: Pandarasamy Arjunan, Dr. Pushpendra Singh
"""





#imports
from uuid import uuid4
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.middleware.csrf import get_token
from django.core.mail import send_mail
from django.conf import settings
from forms import RegistrationForm
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import dateutil.parser
import json, functions,os,fileinput,psutil,sys
from django.views.decorators.cache import cache_page
from multiprocessing import Process,Queue
from functions import URL
from django.template import Context

#Dictionary containing the apikeys of the registered users
apikeys={}

#Dictionary containing the uuid used in the confirmation mail sent
pending={}                                                                              


#last24hours profile details
profile24={}

#Global API details
#profile={'num_request':0,'exec_time':0.0, 'mem_info':0.0}


#Forking a new process for the given request
def fork(function_name, arguments):
        
        p=Process(target=function_name,args=arguments)
        p.start()
        ps1=psutil.Process(p.pid)
        cpu_time=ps1.get_cpu_times()
        memory_info=ps1.get_memory_info()
        p.join()
        return cpu_time,memory_info




#Using the decorator to exempt csrf checks on post requests
@csrf_exempt
@cache_page(10)
def main(request, url):

        APIRequest = URL(url)
        #bypassing apikey for user packages
        jump=False
        if APIRequest.category==settings.UNRESTRICTED_ACCESS:
                jump=True
                APIRequest.category=settings.PACKAGE_PATH
        elif APIRequest.category==settings.SHARED_TEMP_OBJECTS_LOCATION:
                jump=True
                APIRequest.category=settings.TEMP_OBJECTS_LOCATION
        #profile['num_request']= profile['num_request']+1
        if jump==False:
                key=''
                #Checking if the user is registered before every request
                try:
                        key=request.META[settings.APIKEY]                                               
                except:
                        return HttpResponse(settings.APIKEY_FIELD_MISSING)
                if(key not in apikeys.keys()):                                                      
                        return HttpResponse(settings.INVALID_USER)

        
                #Checking profile information to see if the user hasn't exceeded his quota
        
                if key in profile24.keys():
                        profile24[key]['num_request']=profile24[key]['num_request']+1
                        if profile24[key]['num_request']>functions.NUM_REQUESTS:
                                return HttpResponse(settings.LIMIT_REQUEST)
                else:
                        profile24[key]={'num_request':1,'exec_time':0.0, 'mem_info':0.0}

        
        #Processing a get request
        if request.method=="GET":
                #Checking if the request is for a package or a temporary object
                if(APIRequest.category==settings.PACKAGE_PATH):
                        result_queue = Queue()
                        out=fork(functions.package,(result_queue,APIRequest,request.method))
                        final=result_queue.get(0)
                        
                        if jump==False:
                                profile24[key]['exec_time']+=float(str(out[0][1]))#cpu_time[1]))
                                profile24[key]['mem_info']+=float(str(out[1][0]))/1024.0#memory_info[0]))/1024.0
                                functions.json_from_dict(settings.PROFILE,profile24)
                elif APIRequest.category==settings.TEMP_OBJECTS_LOCATION:
                        if jump==False:
                                result_queue = Queue()
                                out=fork(functions.temp_object,(result_queue,APIRequest,request.method,request.META[settings.APIKEY]))
                                final=result_queue.get(0)
                        else:
                                result_queue = Queue()
                                out=fork(functions.temp_object,(result_queue,APIRequest,request.method,settings.SHARED_FOLDER))
                                final=result_queue.get(0)
                elif APIRequest.category==settings.PROFILE_INFO:
                        if jump==False:
                                result_queue = Queue()
                                out=fork(functions.profile_info,(result_queue, profile24[key]))
                                final=result_queue.get(0)
                        else:
                                return HttpResponse(settings.INVALID_REQUEST)
                else:
                        return HttpResponse(settings.INVALID_REQUEST)

        #Processing a post request
        elif request.method=="POST":
                #Checking if the request is for a package or a temporary object
                if(APIRequest.category==settings.PACKAGE_PATH):                        
                        if jump==False:
                                #Gathering profile info
                                result_queue = Queue()
                                out=fork(functions.package,(result_queue,APIRequest,request.method,jump,request.META[settings.APIKEY],request.POST,apikeys.keys(),pending.keys()))
                                final=result_queue.get(0)
                                profile24[key]['exec_time']+=float(str(out[0][1]))#cpu_time[1]))
                                profile24[key]['mem_info']+=float(str(out[1][0]))/1024.0#memory_info[0]))/1024.0
                                functions.json_from_dict(settings.PROFILE,profile24)
                        else:
                                result_queue = Queue()
                                out=fork(functions.package,(result_queue,APIRequest,request.method,jump,None, request.POST,apikeys.keys(),pending.keys()))
                                final=result_queue.get(0)
                elif APIRequest.category==settings.TEMP_OBJECTS_LOCATION:
                        if jump==False:
                                result_queue = Queue()
                                out=fork(functions.temp_object,(result_queue,APIRequest,request.method,request.META[settings.APIKEY]))
                                final=result_queue.get(0)
                        else:
                                result_queue = Queue()
                                out=fork(functions.temp_object,(result_queue,APIRequest,request.method,settings.SHARED_FOLDER))
                                final=result_queue.get(0)
                elif APIRequest.category==settings.PROFILE_INFO:
                        if jump==False:
                                result_queue = Queue()
                                out=fork(functions.profile_info,(result_queue,profile24[key]))
                                final=result_queue.get(0)
                        else:
                                return HttpResponse(settings.INVALID_REQUEST)
                elif APIRequest.category==settings.UPLOAD:
                        if jump==False:
                                try:
                                        result_queue = Queue()
                                        out=fork(functions.upload_library,(result_queue,request.FILES))
                                        final=result_queue.get(0)
                                except:
                                        return HttpResponse(settings.INVALID_REQUEST)
                        else:
                                return HttpResponse(settings.APIKEY_FIELD_MISSING)
                else:
                        return HttpResponse(settings.INVALID_REQUEST)

        elif request.method=="DELETE":
                if jump==False:
                        result_queue = Queue()
                        out=fork(functions.temp_object(result_queue,APIRequest,request.method,request.META[settings.APIKEY]))
                        final=result_queue.get(0)              
                else:
                        result_queue = Queue()
                        out=fork(functions.temp_object,(result_queue,APIRequest,request.method,settings.SHARED_FOLDER))
                        final=result_queue.get(0)              
        else:
                return HttpResponse(settings.INVALID_REQUEST)
        
        #Returning the output in the requested format           
        try:    
                if(final['format']==settings.OUTPUT_FORMATS[0]):
                        return HttpResponse(json.dumps(final['resp']),content_type='application/json')
                elif(final['format']==settings.OUTPUT_FORMATS[1]):
                        return HttpResponse(final['resp'])
        except Exception, e:    
                return HttpResponse(str(e))




#Explorer Page
def explorer(request):
        c = Context({'ip':functions.HOST_IP,'port':functions.PORT_NUMBER})
        return render(request,"explorer.html",c)





#Documentation Page
def documentation(request):
        return render(request,"documentation.html")





#initialising apikey dictionarys
def init():
        global apikeys  
        global pending
        global profile
        if(len(apikeys)==0):
                apikeys=functions.dict_from_json(settings.REGISTERED_APIKEYS)
        if(len(pending)==0):
                pending=functions.dict_from_json(settings.UNCONFIRMED_USERKEYS)
        if(len(profile24)==0):
                profile=functions.dict_from_json(settings.PROFILE)
        sys.path.append(os.getcwd()+'/'+settings.USER_PACKAGE+'/')




                
#signup page            
def signup(request):
        global apikeys  
        global pending  

        #Checking if the form is valid
        if request.method == 'POST':
                form = RegistrationForm(request.POST)
                if form.is_valid():
                        #If the user has a pending confirmation
                        if(request.POST['email'] in pending.values()):
                                return HttpResponse(settings.PENDING_CONFIRMATION)
                                
                        #Sign up procedure 
                        if request.POST['button']==settings.SIGNUP_BUTTON:

                                #If the user is already registered    
                                if request.POST['email'] in apikeys.values():
                                        return HttpResponse(settings.ALREADY_REGISTERED)

                                #generating a unique confirmation pending key    
                                client_key=str(uuid4())
                                while(client_key in pending.keys() or client_key in apikeys.keys()):
                                        client_key=str(uuid4())

                                #Mailing the confirmation link
                                check="http://"+functions.HOST_IP+":"+functions.PORT_NUMBER+"/"+settings.SIGNUP_CONFIRM+"/"+client_key
                                message= settings.ACCOUNT_CONFIRMATION %check
                                send_mail(settings.ACCOUNT_CONFIRMATION_SUBJECT, message, functions.EMAIL_HOST_USER,[request.POST['email']], fail_silently=False)

                                #Adding the pending apikey to the pending dictionary and writing the dictionary to the disk
                                pending[client_key]=[request.POST['email'],datetime.now().isoformat()]
                                functions.json_from_dict(settings.UNCONFIRMED_USERKEYS,pending)             
                                return HttpResponse(settings.THANKS_MESSAGE)

                        #Recovery Procedure    
                        elif request.POST['button']==settings.RECOVERY_BUTTON:
                                if request.POST['email'] in apikeys.values():
                                        #Searching for the user's apikey in the database and mailing it to him
                                        for temp  in apikeys.keys():
                                                if apikeys[temp]==request.POST['email']:
                                                        message= settings.APIKEY_RECOVERY_EMAIL %temp
                                                        send_mail(settings.APIKEY_RECOVERY_EMAIL_SUBJECT, message, functions.EMAIL_HOST_USER,[request.POST['email']], fail_silently=False)
                                                        return HttpResponse(settings.APIKEY_EMAIL_DELIVERY_CONFIRMATION)
                                else:
                                        return HttpResponse(settings.INCORRECT_RECOVERY_REQUEST)
        else:
                form = RegistrationForm()
        return render(request, "signup.html",{ "form" : form })





#View to confirm the user's registration
def confirm(request,pending_apikey):
        global apikeys  
        global pending
        pending_apikey=pending_apikey.split('/')[1]

        if(pending_apikey in pending.keys()):
                #Checking if the link was generated by the system
                #Checking if the link has not expired
                if(datetime.now()-dateutil.parser.parse(pending[pending_apikey][1])).seconds<86400:             

                        #Generating a unique client apikey
                        client_key=str(uuid4())                                                                 
                        while(client_key in apikeys.keys()):
                                client_key=str(uuid4())

                        #Mailing the apikey to the user
                        client_email=[pending[pending_apikey][0]]
                        message= settings.APIKEY_DELIVERY_EMAIL %client_key
                        send_mail(settings.APIKEY_DELIVERY_EMAIL_SUBJECT, message, functions.EMAIL_HOST_USER,client_email, fail_silently=False)

                        #Adding the user's apikey to the list of registered apikeys and writing it back to the disk
                        apikeys[client_key]=pending[pending_apikey][0]
                        functions.json_from_dict(settings.REGISTERED_APIKEYS,apikeys)

                        #Removing the user from the pending list
                        del pending[pending_apikey]
                        functions.json_from_dict(settings.UNCONFIRMED_USERKEYS,pending)
                        return HttpResponse(settings.APIKEY_DELIVERY)
                else:
                        #Removing the link from database if the link was sent more than 24 hrs back.
                        del pending[pending_apikey]
                        functions.json_from_dict(settings.UNCONFIRMED_USERKEYS,pending)
                        return HttpResponse(settings.LINK_EXPIRY)
        else:
                return HttpResponse(settings.LINK_EXPIRY)
