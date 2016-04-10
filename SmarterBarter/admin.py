from django.contrib import admin
from .models import Book
from .models import UserProfile
from .models import ApproveRequests
from .models import ApprovedRequests
admin.site.register(Book)
admin.site.register(UserProfile)
#admin.site.register(Teacher)
admin.site.register(ApproveRequests)
admin.site.register(ApprovedRequests)