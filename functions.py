"""      Please refer to the license file for complete details. 
  *      Project: OpenPy
  *      Developer: Yash Lamba
  *      Institute: Indraprastha Institute of Information Technology, Delhi
  *      Advisor: Pandarasamy Arjunan, Dr. Pushpendra Singh
"""





#imports
from pkgutil import iter_modules			#Module to iterate over the installed python packages
import inspect,__builtin__,os,sys,uuid,json,ast		#Other modules
from django.conf import settings
import cPickle
import ConfigParser

#Global Config Parameters
HOST_IP=settings.HOST_IP
PORT_NUMBER=settings.PORT_NUMBER
EMAIL_HOST=""
EMAIL_HOST_USER=""
EMAIL_HOST_PASSWORD=""
EMAIL_PORT=""
EMAIL_USE_TLS=""
NUM_REQUESTS=100



#URL Class
class URL(object):
        def __init__(self, url):
                #Splitting complete url into components
                url_parts = url.split(r'/')
                self.length=len(url_parts)
                self.category = url_parts[0]
                try:
                        self.package_name=url_parts[1]
                        self.temp_object_name=url_parts[1]        
                        self.function_name=url_parts[2]
                        self.temp_object_output_format=url_parts[2]
                        self.output_format=url_parts[3]
                except:
                        pass

        def getlength(self):
                return self.length





#Name for uploaded files Class
class file_name(object):
        def __init__(self,name):
                #Splitting complete url into components
                name = name.split('.')
                self.length=len(name)
                self.file_name = name[0]
                self.file_extension = name[1]
               
        def getlength(self):
                return self.length




#Loading a given object from json
def dict_from_json(filename):
        try:
                f=open(filename)
                obj=json.load(f)
                f.close()
                return obj
        except:
                return {}





#Dumping a given object to json	
def json_from_dict(filename,obj):
        try:
                f=open(filename,'w')
                json.dump(obj,f)
                f.close()
        except:
                pass





#Packaging output. Takes as input the response to be set and the index of the output format to be used
def output(response,output_type):
        return {'resp':response,'format':settings.OUTPUT_FORMATS[output_type]}


		

		
def LoadConfig():
        Config = ConfigParser.ConfigParser()
        Config.read("config.ini")
        try:
                HOST_IP= Config.get("Network",'host_ip')
                PORT_NUMBER= Config.get("Network",'port')
                EMAIL_HOST= Config.get("Email",'email_host')
                EMAIL_HOST_USER= Config.get("Email",'email_host_user')
                EMAIL_HOST_PASSWORD= Config.get("Email",'email_host_password')
                EMAIL_PORT= Config.get("Email",'email_port')
                EMAIL_USE_TLS= Config.get("Email",'email_use_tls')
                NUM_REQUESTS= Config.get("Limits",'num_requests')
        except:
                return HttpResponse(settings.REGISTRATION_FAILURE_MESSAGE,1)




#Function to generate list of installed python packages
def list_installed_pkg(result):
        #Iterator over the list of modules
	iterator=iter_modules()						
	installed_pkg=[]
	
	#Iterating over the list and appending the package name to the output list
	for package in iterator: 
    		installed_pkg.append(package[1])

        #Adding user packages
        files=user_package()
        for f in files:
                installed_pkg.append(f)
    	installed_pkg.sort()
	result.put(output(installed_pkg,0))
        return

        
	
#Function to load modules
def load_package(package_name):
        module=__import__ (package_name)
        return module
        




#Listing all functions in a package
def func_in_package(result,APIRequest):
        #Loading the package
        try:
                module=load_package(APIRequest.package_name)
        except:
                return output(settings.INVALID_PACKAGE,1)        
        #Getting list of all function in the requested package
        all_functions=inspect.getmembers(module,inspect.isroutine)
	func_list=[]		
	for i in all_functions:
		func_list.append(i[0])
	func_list.sort()
	result.put(output(func_list,0))
        return




#Returns list of user_installed files
def user_package():
        package = os.getcwd()+"/"+settings.USER_PACKAGE+"/"	
	files = [ f.split('.')[0] for f in os.listdir(package) if os.path.isfile(os.path.join(package,f)) ]
	return files



#Returning documentation of a valid function
def documentation_of_func(result,APIRequest):
        #Loading the package
        try:
                module=load_package(APIRequest.package_name)
        except:
                result.put(output(settings.INVALID_PACKAGE,1))
                return        

        #Getting the documentation of the requested funnction
        try:
                requested_function=getattr(module,APIRequest.function_name)
                method_documentation={'documentation':inspect.getdoc(requested_function),'arguments specification':inspect.getargspec(requested_function)}
                result.put(output(method_documentation,0))
                return 	                        
        except:
                if(inspect.getmembers(module,inspect.isbuiltin)):
                        result.put(output(settings.BUILTIN_METHOD,1))
                        return 
                else:
                        result.put(output(settings.INVALID_METHOD,1))
                        return 
                





#Searching for the given handle in the saved objects folder
def search_object(handle,dir_name):
        #Getting the list of all objects in the directory 
        files = [ f.split('.')[0] for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name,f)) ]

        #looking for the object with the given handle
        if handle in files:
                obj_name=open(dir_name+handle,'rb') 
                result=cPickle.load(obj_name)
                return result
        else:
                return handle




#Searching for the given handle in the saved objects folder
def delete_object(handle,dir_name):
        #Getting the list of all objects in the directory 
        files = [ f.split('.')[0] for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name,f)) ]

        #looking for the object with the given handle
        if handle in files:
                os.remove(dir_name+handle)
                return 0
        else:
                return 1




#saving result as temporary object
def save_result(result,function_arguments):
        #Getting the name of the directory for the current user
        if function_arguments[0]==False:
                dir_name=os.getcwd()+"/"+settings.TEMP_OBJECTS_LOCATION+"/"+function_arguments[1]+"/"
        else:
                dir_name=os.getcwd()+"/"+settings.TEMP_OBJECTS_LOCATION+"/"+settings.SHARED_FOLDER+"/"

        #Creating a directory if the user is saving a temporary object for the first time
        if not os.path.exists(dir_name):
                os.makedirs(dir_name)

        #Getting the list of all objects in the directory 
        files = [ f.split('.')[0] for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name,f)) ]

        #generating a handle for the object
        file_hash=str(uuid.uuid4())
        while(file_hash in function_arguments[3] or file_hash in function_arguments[4] or file_hash in files):
                file_hash=str(uuid.uuid4())
                
        cPickle.dump(result,open(dir_name+file_hash,'w'))
        return file_hash




#Processing Input Arguments from string to original data types
def process_input_arguments(requested_function,builtin,function_arguments):
        args=[]	
	error_counter=0
	error=""
	function_flag=0
	argspec=[]
	try:
                argspec=inspect.getargspec(requested_function)[0]
        except:
                if builtin:
                        #Argument Preparation for built in functions
                        for arg in function_arguments[2]:
                                try:
                                        temp=ast.literal_eval(function_arguments[2][arg])
                                        if(type(temp)==str):
                                                if(len(temp)==36):
                                                        #Getting the name of the directory for the current user
                                                        if(function_arguments[0]==False):
                                                                dir_name=os.getcwd()+"/"+settings.TEMP_OBJECTS_LOCATION+"/"+function_arguments[1]+"/"
                                                                args.append(search_object(temp,dir_name))
                                                        else:
                                                                dir_name=os.getcwd()+"/"+settings.TEMP_OBJECTS_LOCATION+"/"+settings.SHARED_FOLDER+"/"
                                                                args.append(search_object(temp,dir_name))
                                                elif len(temp)==4:
                                                        if temp=="None":
                                                                args.append(None)
                                                        elif temp=="True":
                                                                args.append(True)
                                                        elif temp=="False":
                                                                args.append(False)
                                                else:
                                                        args.append(temp)
                                        else:
                                                args.append(temp)
                                except Exception,e:
                                        pass
                        return args
                                
        #Checking if the passed arguments are the ones that have been requested and compiling them together if true
	for arg in argspec:
                try:
                        temp=ast.literal_eval(function_arguments[2][arg])
                        if(type(temp)==str):
                                if(len(temp)==36):
                                        #Getting the name of the directory for the current user
                                        if(function_arguments[0]==False):
                                                dir_name=os.getcwd()+"/"+settings.TEMP_OBJECTS_LOCATION+"/"+function_arguments[1]+"/"
                                                args.append(search_object(temp,dir_name))
                                        else:
                                                dir_name=os.getcwd()+"/"+settings.TEMP_OBJECTS_LOCATION+"/"+settings.SHARED_FOLDER+"/"
                                                args.append(search_object(temp,dir_name))
                                elif len(temp)==4:
                                        if temp=="None":
                                                args.append(None)
                                        elif temp=="True":
                                                args.append(True)
                                        elif temp=="False":
                                                args.append(False)
                                else:
                                        args.append(temp)
                        else:
                                args.append(temp)
                except Exception,e:
                        pass
        return args




#Executing the requested function
def execute(result,APIRequest,request_method,function_arguments):
        #Defining error_counter to be used if the user is attempting to save the result as a temporary object
        error_counter=0

        #Executing the function if the request is post
        if request_method=="POST":
                #Returing an error if the output format requested is invalid
                if APIRequest.output_format not in settings.OUTPUT_FORMATS:
                        result.put(output(settings.INVALID_OUTPUT_FORMAT,1))
                        return

                else:
                        #Loading the requested module
                        try:
                                module=load_package(APIRequest.package_name)
                        except:
                                result.put(output(settings.INVALID_PACKAGE,1))
                                return 

                        #Getting the list of attributes required by the requested function
                        try:
                                #if hasattr(module,url_parts[1]):
                                requested_function=getattr(module,APIRequest.function_name)
                        except:
                                result.put(output(settings.INVALID_METHOD,1))
                                return 

                        #Preparing the method arguments from the parameters in the post request
                        args=[]
                        arguments=process_input_arguments(requested_function,inspect.getmembers(module,inspect.isbuiltin),function_arguments)
                        
                        #Executing the function
                        try:				
                                res=getattr(module,APIRequest.function_name)(*tuple(arguments))
                        except Exception,e: 
                                res=str(e)
                                error_counter=1
                        #Returning the result in the relevant format
                        if APIRequest.output_format==settings.OUTPUT_FORMATS[1]:
                                result.put(output(res,1))
                                return 
                        elif APIRequest.output_format==settings.OUTPUT_FORMATS[0]:
                                result.put(output(res,0))
                                return
                        elif APIRequest.output_format==settings.OUTPUT_FORMATS[2]:
                                if error_counter==0:
                                        result.put(output(save_result(res,function_arguments),0))
                                        return 
                                else:
                                        result.put(output(res,1))
                                        return 
                        else:
                                result.put(output(settings.INVALID_OUTPUT_FORMAT,1))
                                return 
                                
        #If the request is GET then returning the documentation of the function
        elif request_method=="GET":
                documentation_of_func(result,APIRequest)
                return 
        
        #Returning Invalid request is the type is neither GET nor POST
        else:
                result.put(output(settings.INVALID_REQUEST,1))
                return 






#Handling requests to /python/package
def package(result, APIRequest,request_type, *varargs):

        #Loading the passed parameters into globally accessible variables for convenience 
        request_method=request_type
        function_arguments=varargs

        #Getting the length of the url passed by the user
        if(APIRequest.getlength()>4):
                return output(settings.INVALID_REQUEST,1)
        #Fulfilling the request
        if APIRequest.getlength()-1==0:
                return list_installed_pkg(result)
        elif APIRequest.getlength()-1==1:
                return func_in_package(result,APIRequest)
        elif APIRequest.getlength()-1==2:
                return documentation_of_func(result,APIRequest)
        elif APIRequest.getlength()-1==3:
                return execute(result,APIRequest,request_type,function_arguments)
		






#Handling Temporary Files Stored on server i.e. request to /python/tmp
def temp_object(result,APIRequest,request_type,apikey):
	package = os.getcwd()+"/"+settings.TEMP_OBJECTS_LOCATION+"/"+apikey+"/"	
	if APIRequest.getlength()-1==0:	
		files = [ f.split('.')[0] for f in os.listdir(package) if os.path.isfile(os.path.join(package,f)) ]
                result.put(output(str(files),0))
		return 
	elif APIRequest.getlength()-1==2:
                if request_type=="DELETE":
                        if delete_object(APIRequest.temp_object_name,package)==0:
                                result.put(output(settings.SUCCESS,1))
                                return 
                        else:
                                result.put(output(settings.FILE_NOT_FOUND,1))
                                return 
                handle=search_object(APIRequest.temp_object_name,package)
                if(handle==APIRequest.temp_object_name):
                        result.put(output(settings.INVALID_OBJECT,1))
                        return 
                else:
                        #Returning the result in the relevant format
                        if APIRequest.temp_object_output_format==settings.OUTPUT_FORMATS[1]:
                                result.put(output(handle,1))
                                return 
                        elif APIRequest.temp_object_output_format==settings.OUTPUT_FORMATS[0]:
                                result.put(output(handle,0))
                                return 
                        else:
                                result.put(output(settings.INVALID_OUTPUT_FORMAT,1))
                                return 
                
	else:
                result.put(output(settings.INVALID_REQUEST,1)   )
                return 





#Viewing profile statistics i.e. request to /python/profile
def profile_info(result,identity):
        result.put(output(str(identity),0))
	return 




#Uploading libraries i.e. request to /python/upload
def upload_library(result,FILES):
        #Checking the file type
        name=file_name(FILES['file'].name)
        if name.getlength()!=2:
                result.put(output(settings.INVALID_FILE_NAME,1))
                return 
        if name.file_extension!='py':
                result.put(output(settings.INVALID_FILE_TYPE,1))
                return         
                
        path= os.getcwd()+'/user_packages/'
        destination = open(path+name.file_name, 'wb+')
        for chunk in FILES['file'].chunks():
                destination.write(chunk)
        destination.close()
        result.put(output(settings.SUCCESS,1))
        return 
