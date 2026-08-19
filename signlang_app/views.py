from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse

from .forms import *
from signlang_app.models import *


# Create your views here.
class Login(View):
    def get (self,request):
        return render(request,'login.html')
    
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        print("---------------", username, password)
        try:
            obj=LoginTable.objects.get(username=username, password=password)
            print(obj)
            request.session['userid']=obj.id

            if obj.usertype == 'admin':
                return HttpResponse(
                    '''<script>alert("login successfull");window.location='/Adminhome'</script>'''
                )
            elif obj.usertype == 'user':
                return HttpResponse(
                    '''<script>alert("login successfull");window.location='/Userhomepage'</script>'''
                )
            else:
                return HttpResponse(
                    '''<script>alert("Login Unsuccessful");window.location='/'</script>'''
                )
        except LoginTable.DoesNotExist:
                return HttpResponse('''<script>alert("Invalid credentials");window.location='/'</script>''')
class Adminhome(View):
    def get (self,request):
        c=UserTable.objects.all().count()
        d=ComplaintTable.objects.all().count()
        e=FeedbackTable.objects.all().count()
        return render(request,'administration/admin_home.html',{'user_count':c,'complaint_count':d,'feedback_count':e})
    
class Manageuser(View):
    def get (self,request):
        c=UserTable.objects.all()
        return render(request,'administration/manage_user.html',{'user':c})    
    
class Viewcomplaints(View):
    def get (self,request):
        c=ComplaintTable.objects.all()
        return render(request,'administration/view_complaints.html',{'complaint':c})   

class Viewfeedback(View):
    def get (self,request):
        c=FeedbackTable.objects.all()
        return render(request,'administration/view_feedback.html',{'feedback':c})
    
class Adduser(View):

    def get (self,request):
        return render(request,'administration/add_user.html')
    
    def post(self,request):
        c=UserForm(request.POST)
        print("====================", request.POST)
        if c.is_valid():
            print("-----------------")
            reg=c.save(commit=False)
            user=LoginTable.objects.create(username=reg.name, password=request.POST["password"],usertype="user")
            reg.LOGINID=user
            reg.save()
            return redirect('/')

      


class Userhomepage(View):
    def get (self,request):
        return render(request,'user/user_home.html')   

class sendcomplaints(View):

    def get(self, request):
        c=ComplaintTable.objects.filter(USERID__LOGINID_id=request.session['userid'])
        return render(request,'user/send_complaint.html',{'complaint':c})

    def post(self, request):
        d = ComplaintForm(request.POST)        
        if d.is_valid():
            reg=d.save(commit=False)
            user=UserTable.objects.get(LOGINID__id=request.session['userid'])
            print(user)
            reg.USERID=user
            reg.save()
            return HttpResponse('''<script>alert("complaint sent successfully");window.location='/sendcomplaints'</script>''')
         
class sendfeedback(View):
    def get (self,request):
        return render(request,'user/send_feedback.html')      

    def post(self, request):
        d = FeedbackForm(request.POST)        
        if d.is_valid():
            reg=d.save(commit=False)
            user=UserTable.objects.get(LOGINID__id=request.session['userid'])
            print(user)
            reg.USERID=user
            # force correct rating value
            print("-----------------", int(request.POST.get("rating")))
            reg.rating = int(request.POST.get("rating"))
            reg.save() 
            return HttpResponse('''<script>alert("feedback sent successfully");window.location='/sendfeedback'</script>''')

class Deleteuser(View):
    def get(self, request, id):
        try:
            d = UserTable.objects.get(id=id) 
            d.delete()
            return HttpResponse('''<script>alert("user deleted successfully");window.location='/Manageuser'</script>''')
        except UserTable.DoesNotExist: 
            return HttpResponse('''<script>alert("user not found");window.location='/Manageuser'</script>''')   
    
class Deletecomplaint(View):
    def get(self, request, id):
        try:
            d = ComplaintTable.objects.get(id=id) 
            d.delete()
            return HttpResponse('''<script>alert("complaint deleted successfully");window.location='/Viewcomplaints'</script>''')
        except ComplaintTable.DoesNotExist: 
            return HttpResponse('''<script>alert("complaint not found");window.location='/Viewcomplaints'</script>''')  
        
class Deletefeedback(View):
    def get(self, request, id):
        try:
            d = FeedbackTable.objects.get(id=id) 
            d.delete()
            return HttpResponse('''<script>alert("feedback deleted successfully");window.location='/Viewfeedback'</script>''')
        except FeedbackTable.DoesNotExist: 
            return HttpResponse('''<script>alert("feedback not found");window.location='/Viewfeedback'</script>''')  
        
class ReplyView(View): 
    def post(self,request,id): 
        c= ComplaintTable.objects.get(id=id) 
        d=ReplyForm(request.POST,instance=c)
        if d.is_valid():
            d.save() 
            return redirect('/Viewcomplaints')


from django.shortcuts import render
from django.http import StreamingHttpResponse
from signlang_app.camera import generate_frames


class isl_page(View):
    def get(self,request):
        return render(request, 'user/isl_live.html')

class video_feed(View):
    def get(self,request):
        return StreamingHttpResponse(
            generate_frames(),
            content_type='multipart/x-mixed-replace; boundary=frame'
        )
    
    
import subprocess
from django.http import JsonResponse

from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
import subprocess
import socket
import time

class StartSignAnimationView(View):
    def get(self, request):
        print("Starting sign animation frontend...")

        project_path = r"D:\signbridge\sign_language\sign_animation"
        frontend_url = "http://localhost:4200/"

        try:
            # Step 1: Check if frontend already running
            if self.is_port_in_use(4200):
                print("Frontend already running.")
                return HttpResponseRedirect(frontend_url)
 
            # Step 2: Start frontend in background
            subprocess.Popen(
                "npm start",
                cwd=project_path,
                shell=True
            )

            # Step 3: Wait for the server to come up (max 45 sec)
            print("Waiting for Angular server to start...")
            for i in range(45):
                if self.is_port_in_use(4200):
                    print("Angular server is up!")
                    return HttpResponseRedirect(frontend_url)
                time.sleep(1)

            # Step 4: Timeout
            print("Timeout: Angular did not start in time.")
            return JsonResponse({
                "status": "starting",
                "message": "Frontend is starting... Try refreshing after a few seconds."
            })

        except Exception as e:
            print("Error starting frontend:", e)
            return JsonResponse({"status": "error", "message": str(e)})

    @staticmethod
    def is_port_in_use(port):
        """Check if a given TCP port is in use (localhost)."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("localhost", port)) == 0



