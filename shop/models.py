import os
from PIL import Image
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

        ordering = ['title']

    class Status(models.TextChoices):
        IN_STOCK = 'in_stock', _('in stock')
        ON_ORDER = 'on_order', _('on order')
        EXPECTED = 'expected', _('expected to arrive')
        OUT_OF_STOCK = 'out_of_stock', _('out of stock')
        NOT_PRODUCED = 'not_produced', _('not produced')

    title = models.CharField(_('title'), max_length=255)
    sku = models.CharField(_('sku'), max_length=255, unique=True)
    price = models.DecimalField(_('price'), max_digits=6, decimal_places=2, null=True)
    status = models.CharField(_('status'), max_length=20, choices=Status.choices,
                              default=Status.IN_STOCK)
    image = models.ImageField(_('image'), blank=True, upload_to='images/')

    def convert_to_webp(self):
        file_name = self.image.name.rsplit('.', 1)
        if file_name[-1] in ['jpg', 'png'] \
                and not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'images', self.image.name)):

            if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'images')):
                os.makedirs(os.path.join(settings.MEDIA_ROOT, 'images'))

            img = Image.open(self.image)
            webp_file_name = f'{file_name[0]}.webp'
            image_path = os.path.join(settings.MEDIA_ROOT, 'images', webp_file_name)
            img.save(image_path, 'webp')

    def save(self, *args, **kwargs):
        if self.image:
            self.convert_to_webp()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
