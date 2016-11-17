from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save

# Create your models here.

class Post(models.Model):
	author =  models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	def Publish(self):
		self.published_date = timezone.Now()
		self.save()

	def __str__(self):
		return self.title

def create_slug(instance, new_slug = None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()

	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post )

