from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from schedule.models.calendars import Calendar
from schedule.models.events import Event
# Create your models here.
#_____________________________________________________________________________

# def upload_location(instance, filename):
#     GuideModel = instance.__class__
#     new_id = GuideModel.objects.order_by("pk").last().pk
#     #new_id = GuideModel.objects.order_by("guide_name").last().slug + 1
#     return "%s/%s" %(new_id, filename)

CHOICE_FIELDS = [('English', 'English'), ('Spanish','Spanish'), ('Russian', 'Russian'), ('Italian', 'Italian'),]

NUMBER_FIELDS = [(1, 1), (2,2), (3, 3), (4, 4), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]


class Guide(models.Model):
    #guide_name      = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
#_____________________IN THE WORKS________________________________________________________
    guide_name      = models.ForeignKey(settings.AUTH_USER_MODEL)
#_____________________IN THE WORKS________________________________________________________
    first_name      = models.CharField(max_length=1000)
    last_name       = models.CharField(max_length=1000)
    tourSize       = models.IntegerField(null=True, blank=True, choices=NUMBER_FIELDS)
    tour_description= models.TextField(max_length=1000)
    remember        = models.TextField(max_length=1000, null=True, blank=True)
    living          = models.CharField(max_length=100, null=True, blank=True)
    secondary_language = models.CharField(max_length=100, null=True, blank=True, choices=CHOICE_FIELDS)
    #Use the Google Maps Location Finder to always have this found. This may work for now.
    meet_up_point   = models.CharField(max_length=1000, null=True, blank=True)
    # events          = models.ManyToManyField(Event,
    #         limit_choices_to={'creator_id': True},
    #         blank=True,
    #         null=True,
    #         verbose_name=("events"),
    #         related_name=('events'),)

    #vacation       = models.BooleanField(default=False)
    #image           = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width_field", height_field="height_field")
    height_field    = models.IntegerField(default=100)
    width_field     = models.IntegerField(default=80)
    language        = models.CharField(max_length=20, choices=CHOICE_FIELDS)
    updated         = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)
    slug            = models.SlugField(unique=True)
    
    def __str__(self):
        name = str(self.first_name)
        return name


    def get_absolute_url(self):
        return reverse("tour:guide_detail", kwargs={"pk": self.pk})

    def get_image_url(self):
        img = self.guideimage_set.first()
        if img:
            return img.image.url
        return img #None


    # def get_absolute_url(self):
    #     return reverse("tour:guide_profile", kwargs={"slug": self.slug})



def create_slug(instance, new_slug=None):
    slug = slugify(instance.guide_name)
    if new_slug is not None:
        slug = new_slug
    qs = Guide.objects.filter(slug=slug).order_by("-pk")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().pk)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Guide)

#_____________________IN THE WORKS________________________________________________________
def image_upload_to(instance, filename):
    title = instance.guide.guide_name
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
    return "guides/%s/%s" %(slug, new_filename)


class GuideImage(models.Model):
    guide = models.ForeignKey(Guide)
    image = models.ImageField(upload_to=image_upload_to)

    def __str__(self):
        return self.guide.first_name
#_____________________IN THE WORKS________________________________________________________