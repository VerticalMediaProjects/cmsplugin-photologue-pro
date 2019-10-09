from datetime import datetime
from django import template
from django.utils import formats
from photologue import models

register = template.Library()


def get_exif_data(photo, attr):
    value = photo.EXIF.get(attr)
    if value is None:
        return
    if attr == 'EXIF DateTimeOriginal':
        dt = datetime.strptime(str(value), '%Y:%m:%d %H:%M:%S')
        value = formats.date_format(dt, 'DATETIME_FORMAT', True)
    elif attr == 'EXIF DateOriginal':
        value = photo.EXIF.get('EXIF DateTimeOriginal')
        if value is None:
            return
        dt = datetime.strptime(str(value), '%Y:%m:%d %H:%M:%S')
        value = formats.date_format(dt, 'DATE_FORMAT', True)
    elif attr == 'EXIF ApertureValue':
        f = value.split('/')
        if len(f) == 1:
            try:
                aperture = float(f[0])
            except ValueError:
                return '-'
        else:
            aperture = float(f[0]) / float(f[1])
        value = 'f/%.1f' % aperture
    return value


@register.inclusion_tag('cmsplugin_photologue_pro/polaroid.html')
def polaroid_thumbnail(photo, photosize=None, counter=''):
    if not photosize:
        photosize = models.PhotoSize.objects.get(name='thumbnail')
    photo.create_size(photosize)
    return {
        'url': photo.get_thumbnail_url,
        'title': photo.title,
        'counter': counter,
    }


@register.simple_tag
def exif(photo, attr):
    return get_exif_data(photo, attr)


@register.simple_tag
def get_exif(photo, attr):
    return get_exif_data(photo, attr)
