from django.shortcuts import render
from SmarterBarter.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from SmarterBarter.models import Book, UserProfile
from SmarterBarter.models import ApproveRequests, ApprovedRequests
from django.template import RequestContext


from SmarterBarter.forms import UserForm, UserProfileForm
temp=0
l=[]
k=0

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
           
            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print("invalid form")

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )




def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/admin/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: ")
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html', {})


def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/login')

def all_books(request):
    if request.user.is_authenticated():
        SAP=request.user
        test=request.user.username

        if(test=='admin'):
            superuser=1
    
        else:

            details=UserProfile.objects.get(user=SAP)
            superuser=int(details.superuser)
            
        query_results=Book.objects.all()
        return render(request,'allbooks.html',{'query_results':query_results,'superuser':superuser})
    else:
         return HttpResponseRedirect('/login/')

def issue(request):
    send=str(request.path)
    send1=send[8:]
    to_send=Book.objects.get(id=send1)
    SAP=None
    if request.user.is_authenticated():
        SAP=request.user.username
        new=ApproveRequests.objects.create(bookName=to_send.bookName,requested_by=str(SAP),issued=0,bookId=send1)
        new.save()
        return render(request,'issue_request.html',{'lolmax':to_send,'request':request,'new':new})
    else:
        return HttpResponseRedirect('/login/')


def approve(request):
    
    query_results=ApproveRequests.objects.all()
    
    return render(request,'approve_request.html',{'query_results':query_results,'Book':Book})

def approved(request):
    if(request.user.is_authenticated()):
        send=str(request.path)
        send1=send[10:]
        send2=int(send1)
        to_delete=ApproveRequests.objects.get(id=send2)
        book=Book.objects.get(id=to_delete.bookId)

        if book.copiesLeft >0 :
            
            new=ApprovedRequests.objects.create(bookName=to_delete.bookName,requested_by=to_delete.requested_by,bookId=to_delete.bookId)
            bookId=Book.objects.get(id=int(to_delete.bookId))
            copiesLeft=bookId.copiesLeft
            copiesLeft=copiesLeft-1
            bookId.copiesLeft=copiesLeft
            bookId.save()
            new.save()
            ApproveRequests.objects.get(id=send2).delete()
            
            return render(request,'approved_request.html',{'send1':send1})
        else:
            return render(request,'request_declined.html',{})
    else:
        return HttpResponseRedirect('/login/')

def home(request):
    if(request.user.is_authenticated()):
        SAP=str(request.user.username)
        query_results=ApprovedRequests.objects.filter(requested_by=SAP)
        return render(request,'home.html',{'query_results':query_results})
    else:
        return HttpResponseRedirect('/login/')
def addBooks(request):
    if(request.user.is_authenticated()):
        if request.method == 'POST':
        
            bookName=request.POST.get('bookName')
            subject=request.POST.get('subject')
            semester=request.POST.get('semester')
            copiesLeft=request.POST.get('copiesLeft')
            new_book=Book.objects.create(bookName=bookName,subject=subject,semester=semester,copiesLeft=copiesLeft)
            new_book.save()

         
        return render(request,'add_books.html',{} )
    else:
        return HttpResponseRedirect('/login/')


def deleteBook(request):
    if(request.user.is_authenticated):
        SAP=request.user
        test=request.user.username
       
        if(test=='admin'):
            superuser=1
    
        else:

            details=UserProfile.objects.get(user=SAP)
            superuser=int(details.superuser)

        if superuser==1:
            send=str(request.path)
            send1=send[8:]
            send2=int(send1)    
            Book.objects.get(id=send2).delete()
            return render(request,'delete.html',{'id':send2} )

        else:
            HttpResponseRedirect('/allbooks/')
    else:
        HttpResponseRedirect('/login/')


def deleteCopy(request):
    if(request.user.is_authenticated):
        SAP=request.user
        test=request.user.username
        

        if(test=='admin'):
            superuser=1
    
        else:

            details=UserProfile.objects.get(user=SAP)
            superuser=int(details.superuser)

        if superuser==1:
            send=str(request.path)
            send1=send[8:]
            send2=int(send1)    
            bookId=Book.objects.get(id=send2)
            if bookId.copiesLeft >0 :
            
            
                
                copiesLeft=bookId.copiesLeft
                copiesLeft=copiesLeft-1
                bookId.copiesLeft=copiesLeft
                bookId.save()
                
                
                
                return render(request,'copy_deleted.html',{'send2':send2})
            else:
                return render(request,'request_declined.html',{})

        else:
            HttpResponseRedirect('/allbooks/')
    else:
        HttpResponseRedirect('/login/')

def all_issued(request):
    if(request.user.is_authenticated):
        SAP=request.user
        test=request.user.username
       
        if(test=='admin'):
            superuser=1
    
        else:

            details=UserProfile.objects.get(user=SAP)
            superuser=int(details.superuser)
            





            










    

