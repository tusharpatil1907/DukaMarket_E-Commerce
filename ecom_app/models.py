from django.db import models
from django.dispatch import receiver
from tinymce.models import HTMLField
from django.utils.text import slugify
from django.db.models.signals import pre_save


class Main_Category(models.Model):
    Category_name = models.CharField(max_length=50)
    cat_logo = models.ImageField(upload_to='media/Category/categoty_main/Category_logo')
    Image = models.ImageField(upload_to='media/Category/categoty_main/Category_img')

    def __str__(self):
        return self.Category_name


class Category(models.Model):
    Category_name = models.CharField(max_length=100)
    # Category_Description = models.TextField()
    Image = models.ImageField(upload_to='media/Category/Category_img')
    Main_cat = models.ForeignKey(Main_Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.Main_cat.Category_name + '---' + self.Category_name


class Sub_Category(models.Model):
    Category_name = models.CharField(max_length=100)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.Category.Main_cat.Category_name + '-----' + self.Category.Category_name + '----  --' + self.Category_name


class Banner(models.Model):
    DISCOUNT_DEALS = (
        ('HOT DEALS', 'HOT DEALS'),
        ('NEW ARRAIVAL', 'NEW ARRAIVAL'),
    )

    Featured_cat = models.ForeignKey(Main_Category, on_delete=models.CASCADE, related_name='featuredcat')
    Discount_Offer = models.CharField(max_length=100)
    Deal = models.CharField(max_length=100, choices=DISCOUNT_DEALS)
    Discount_percent = models.IntegerField()
    Banner = models.ImageField(upload_to='media/Category/Featured_banners')

    def __str__(self):
        return self.Featured_cat.Category_name


class Section(models.Model):
    Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


class Product(models.Model):
    Total_qty = models.IntegerField()
    Availablity = models.IntegerField()
    Featured_image = models.CharField(max_length=100)
    Product_name = models.CharField(max_length=100)
    Price = models.IntegerField()
    Discount = models.IntegerField()
    Product_Information = HTMLField()
    Model_name = models.CharField(max_length=100)
    Categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    Tags = models.CharField(max_length=100)
    Description = HTMLField()
    Section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def __str__(self):
        return self.Product_name

    # Creating a slug field( auto generating it from title)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('Product_details', kwargs={'slug': self.slug})

    class Meta:
        db_table = 'ecom_app_Product'


def create_slug(instance, new_slug=None):
    slug = slugify(instance.Product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Product)
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


class Product_image(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Image_url = models.CharField(max_length=200)


class Aditional_details(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Specification = models.CharField(max_length=100)
    Details = models.CharField(max_length=100)


