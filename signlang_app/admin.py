from django.contrib import admin

from signlang_app.models import *

# Register your models here.
admin.site.register(LoginTable)
admin.site.register(UserTable)
admin.site.register(ComplaintTable)
admin.site.register(FeedbackTable)