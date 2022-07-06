from django.db import models

# Create your models here.
class Tourguide(models.Model):

    name = models.CharField(max_length =30)
    images = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name

    def save_tourguide(self):
        self.save()



class Image(models.Model):
    name = models.CharField(max_length =60)
    description = models.TextField()
    tourguide = models.ForeignKey(Tourguide,on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to = 'images/')

    def __str__(self):
        return self.name

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    @classmethod
    def my_images(self):
        all_images = Image.objects.all()
        return all_images 
