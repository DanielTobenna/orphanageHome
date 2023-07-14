from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
	user= models.OneToOneField(User, on_delete= models.CASCADE)
	bio= models.TextField(blank= True)
	first_name= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	last_name= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	email_address= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	country= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	home_address= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	code= models.CharField(max_length=12, blank=True)
	recommended_by= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')
	updated= models.DateTimeField(auto_now= True)
	created= models.DateTimeField(auto_now_add= True)
	deposit= models.FloatField(default=0, null=True)
	balance= models.FloatField(default=0,null=True)
	withdrawal= models.FloatField(default=0,null=True)
	profit= models.FloatField(default=0,null=True)
	roi= models.FloatField(default=0.015, null=True)
	running_days= models.IntegerField(default=0, null=True)
	wallet_address= models.CharField(max_length=400, default='update your account', null=True)
	profile_pic= models.ImageField(null=True, blank=True)

	def __str__(self):
		return f'{self.user.username}-{self.code}'

	@property
	def profile_picUrl(self):
		try:
			url= self.profile_pic.url
		except:
			url=''
		return url

	def get_recommended_profiles(self):
		query= Client.objects.all()
		my_recs= []
		for i in query:
			if i.recommended_by== self.user:
				my_recs.append(i)
		return my_recs


	def save(self, *args, **kwargs):
		if self.code=='':
			code= generate_ref_code()
			self.code= code
		super().save(*args, **kwargs)