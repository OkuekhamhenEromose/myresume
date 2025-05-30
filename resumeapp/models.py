
from django.db import models

STATE_CHOICE = (
 ('Abia','Abia'),
 ('Adamawa','Adamawa'),
 ('Akwa Ibom','Akwa Ibom'),
 ('Anambra','Anambra'),
 ('Bauchi','Bauchi'),
 ('Bayelsa','Bayelsa'),
 ('Benue','Benue'),
 ('Borno','Borno'),
 ('Cross River','Cross River'),
 ('Delta','Delta'),
 ('Ebonyi','Ebonyi'),
 ('Edo','Edo'),
 ('Ekiti','Ekiti'),
 ('Enugu','Enugu'),
 ('Gombe','Gombe'),
 ('Imo','Imo'),
 ('Jigawa','Jigawa'),
 ('Kaduna','Kaduna'),
 ('Kano','Kano'),
 ('Katsina','Katsina'),
 ('Kebbi','Kebbi'),
 ('Kogi','Kogi'),
 ('Kwara','Kwara'),
 ('Lagos','Lagos'),
 ('Nasarawa','Nasarawa'),
 ('Niger','Niger'),
 ('Ogun','Ogun'),
 ('Ondo','Ondo'),
 ('Osun','Osun'),
 ('Oyo','Oyo'),
 ('Plateau','Plateau'),
 ('Rivers','Rivers'),
 ('Sokoto','Sokoto'),
 ('Taraba','Taraba'),
 ('Yobe','Yobe'),
 ('Zamfara','Zamfara'),
)

class Resume(models.Model):
 name = models.CharField(max_length=100)
 dob = models.DateField(auto_now=False, auto_now_add=False)
 gender = models.CharField(max_length=100)
 locality = models.CharField(max_length=100)
 city = models.CharField(max_length=100)
 pin = models.PositiveIntegerField()
 state = models.CharField(choices=STATE_CHOICE, max_length=50)
 mobile = models.PositiveIntegerField()
 email = models.EmailField()
 job_city = models.CharField(max_length=50)
 profile_image = models.ImageField(upload_to='profileimg', blank=True)
 my_file = models.FileField(upload_to='doc', blank=True)


