import re
from django.core.urlresolvers import reverse
from django.db.models import permalink
from django.db import models
from django.utils.encoding import force_unicode
import mptt

class Category(models.Model):
    parent = models.ForeignKey('self', 
        blank=True, 
        null=True, 
        related_name="children", 
        help_text="Leave this blank for an Category Tree", 
        verbose_name='Parent')
    name = models.CharField(max_length=100)
    description = models.CharField(blank=True, null=True, max_length=255)
    order = models.IntegerField(blank=True, null=True)
    slug = models.SlugField()
    
    def get_absolute_url(self):
        """Return a path"""
        prefix = reverse('categories_tree_list')
        ancestors = list(self.get_ancestors()) + [self,]
        return prefix + '/'.join([force_unicode(i.slug) for i in ancestors]) + '/'
        
    class Meta:
        verbose_name_plural = 'categories'
        unique_together = ('parent', 'name')
        ordering = ('tree_id','lft')

    def __unicode__(self):
        ancestors = self.get_ancestors()
        return ' > '.join([force_unicode(i.name) for i in ancestors]+[self.name,])

mptt.register(Category, order_insertion_by=['name'])
