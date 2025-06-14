import uuid
from django.db import models
from myapp.models import Profile

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
GENDER =(
    ('M', 'Male'),
    ('F', 'Female')
)
JOB_CITY_CHOICE = [
 ('Delhi', 'Delhi'),
 ('Pune', 'Pune'),
 ('Ranchi', 'Ranchi'),
 ('Mumbai', 'Mumbai'),
 ('Dhanbad', 'Dhanbad'),
 ('Banglore', 'Banglore')
]

class Resume(models.Model):
 name = models.CharField(max_length=100)
 dob = models.DateField(auto_now=False, auto_now_add=False)
 gender = models.CharField(choices=GENDER, max_length=50)
 locality = models.CharField(max_length=100)
 city = models.CharField(max_length=100)
 pin = models.PositiveIntegerField()
 state = models.CharField(choices=STATE_CHOICE, max_length=50)
 mobile = models.PositiveIntegerField()
 email = models.EmailField()
 listing_id = models.UUIDField(unique=True,default=uuid.uuid4)
 job_city = models.CharField(max_length=50)
 profile_image = models.ImageField(upload_to='listing', blank=True)
 my_file = models.FileField(upload_to='listing', blank=True)

# This is the user listing, it contains the total of all listings a user has
# and the profile of the user
class UserListing(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
    total = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{str(self.total)}'
# This is the single listing, it contains the listing and the quantity of that listing
# in the user listing. It is used to calculate the total of the user listing
class SingleListing(models.Model):
    userlisting = models.ForeignKey(UserListing, on_delete=models.CASCADE)
    listing = models.ForeignKey(Resume, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    # subtotal = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'UserListing Listing - {self.userlisting.id} -{self.quantity}'

