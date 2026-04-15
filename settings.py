# الكود 1: إعدادات النواة - إعدادات المشروع (settings.py)

import os

# "ثوابت البيئة" (نواة المشروع)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'physics_in_design_super_secret_key' # مفتاح الطاقة المشفر

# "تحديد الأجسام" (التطبيقات التي تحمل المادة)
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'student_core', # تطبيق الطلاب الأساسي
    'feed_dynamics', # تطبيق ديناميكا المنشورات
    'groups_structure', # تطبيق المجموعات
    'patent_innovations', # تطبيق الاختراعات
]
# الكود 2: هيكلية القوى - نموذج بيانات الطالب (models_user.py)

from django.db import models
from django.utils import timezone

class StudentProfile(models.Model):
    # 'مفتاح الهوية' (تفرد الطالب)
    username = models.CharField(max_length=50, unique=True)
    
    # 'ملامح الجسم' (البيانات البصرية من image_4.png)
    full_name_ar = models.CharField(max_length=100)
    profile_pic_url = models.URLField(blank=True)
    
    # حقول إضافية للمؤسس (email, bio_ar)
    email = models.EmailField(unique=True)
    creation_date = models.DateTimeField(default=timezone.now)
    bio_ar = models.TextField(blank=True)

    def __str__(self):
        return self.full_name_ar
# الكود 3: التوثيق - نظام التوثيق البرمجي (auth_engine.py)

from django.contrib.auth import authenticate, login
from .models_user import StudentProfile

# "قوة الجذب" لتوثيق الطالب
def authenticate_student(request, username, password):
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        # إرجاع "الملف الشخصي" المرتبط
        return StudentProfile.objects.get(username=user.username)
    return None
# الكود 4: ديناميكا المحتوى - نظام المنشورات والتفاعل (models_content.py)

from django.db import models
from django.utils import timezone
from student_core.models_user import StudentProfile

class Post(models.Model):
    # 'قانون الجذب' لصاحب المنشور
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='posts')
    
    # 'ملامح الجسم' (المحتوى والزمن والنوع)
    content_text = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    post_type = models.CharField(max_length=20) # درس، مذكرات مصورة، تحديث

class Comment(models.Model):
    # 'قانون الحركة الثالث' لربط التعليق
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    comment_text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

class Like(models.Model):
    # 'قوة الجذب' للإعجاب
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('post', 'student') # تفرد الإعجاب
# الكود 5: قوانين التصفية - دوال التصفية (views_feed.py)

from .models_content import Post

# "نظام التصفية" (Filtering logic من image_18.png)
def filtered_feed(request):
    all_posts = Post.objects.all().order_by('-timestamp')
    post_type_filter = request.GET.get('type', 'all')
    
    # تطبيق "قوة التصفية" بناءً على طلب الطالب
    if post_type_filter == 'lesson':
        return all_posts.filter(post_type='lesson')
    elif post_type_filter == 'visual_memory':
        return all_posts.filter(post_type='visual_memory')
    else:
        return all_posts
# الكود 6: هيكلية التجمعات - نظام المجموعات والعضوية (models_groups.py)

from django.db import models
from django.utils import timezone
from student_core.models_user import StudentProfile

class StudyGroup(models.Model):
    # 'مفتاح الهوية' للمجموعة
    group_name_ar = models.CharField(max_length=100)
    description_ar = models.TextField(blank=True)
    cover_pic_url = models.URLField(blank=True)
    creator = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='created_groups')
    creation_date = models.DateTimeField(default=timezone.now)

class GroupMembership(models.Model):
    # 'قانون الحركة الثالث' لربط العضوية
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='members')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    role_ar = models.CharField(max_length=20) # مدير، عضو
    join_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('group', 'student') # تفرد العضوية
# الكود 7: التفاعل الكلي - دوال عرض البيانات (views_integration.py)

from feed_dynamics.models_content import Post
from groups_structure.models_groups import StudyGroup

# "دوائر التدفق" لعرض الصفحة الرئيسية (الـ Feed من image_4.png)
def home_feed(request):
    # استرجاع المنشورات كـ "أجسام متساقطة" (حسب الزمن)
    posts = Post.objects.all().order_by('-timestamp')
    
    # "حساب الطاقة" لكل منشور ديناميكياً
    feed_data = []
    for post in posts:
        feed_data.append({
            'post': post,
            'like_count': post.likes.count(), # حساب الإعجابات
            'comments': post.comments.all() # جلب التعليقات
        })
    
    # "تجسيد" الواجهة بناءً على البيانات
    return render(request, 'dashboard.html', {'feed_data': feed_data})
# الكود 8: براءات الاختراع - نظام الاختراعات (models_patents.py)

from django.db import models
from django.utils import timezone
from student_core.models_user import StudentProfile

class Patent(models.Model):
    # 'قانون الجذب' لصاحب الاختراع
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='patents')
    
    # 'ملامح الجسم' (العنوان والنبذة والزمن)
    title_ar = models.CharField(max_length=200)
    abstract_ar = models.TextField()
    submission_date = models.DateTimeField(default=timezone.now)
    status_ar = models.CharField(max_length=50) # قيد المراجعة، مصدقة

    class Meta:
        ordering = ['-submission_date'] # الأحدث يظهر أولاً
# الكود 9: هيكلية التجمعات - نظام المجموعات والعضوية (models_groups.py)

from django.db import models
from django.utils import timezone
from student_core.models_user import StudentProfile

class StudyGroup(models.Model):
    # 'مفتاح الهوية' للمجموعة (اسم فريد)
    group_name_ar = models.CharField(max_length=100, unique=True)
    
    # 'ملامح الجسم' البصرية والنصية
    description_ar = models.TextField(blank=True)
    cover_pic_url = models.URLField(blank=True) # رابط صورة الغلاف
    
    # 'قانون الجذب' لصاحب المجموعة (المنشئ)
    creator = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='created_groups')
    
    # 'صفات الحركة' (الزمن)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.group_name_ar

class GroupMembership(models.Model):
    # 'قانون الحركة الثالث' لربط العضوية بالمجموعة وصاحبها
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='members')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    
    # ملامح الجسم (الدور والزمن)
    role_ar = models.CharField(max_length=20, default='member') # مدير، عضو، الخ
    join_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('group', 'student') # تفرد العضوية: لا يمكن للطالب الانضمام مرتين لنفس المجموعة

    def __str__(self):
        return f"Membership of {self.student.username} in {self.group.group_name_ar}"


