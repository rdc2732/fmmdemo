# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Function(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Feature(models.Model):
    CHOICE = u'CHO'
    SELECTION = u'SEL'
    RULE_TYPES = ((CHOICE, u'choice'), (SELECTION, u'selection'))
    function = models.ForeignKey(Function, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    selection_name = models.CharField(max_length=100, blank=True)
    rule_type = models.CharField(max_length=15, blank=True, choices=RULE_TYPES)
    option_min = models.IntegerField(blank=True, null=True)
    option_max = models.IntegerField(blank=True, null=True)
    enabled = models.NullBooleanField(default=False)
    selected = models.NullBooleanField(default=False)

    def __str__(self):
        return self.name


class Dependency(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class FeatureForm(ModelForm):
    class Meta:
        model = Feature
        fields = ['name','enabled','selected']


class TestFeature(models.Model):
    # 0-Group, 1-Function, 2-Feature_Name, 3-Feature='name', 4-Dependency, 5-Rule, 6-Min, 7-Max
    CHOICE = u'CHO'
    SELECTION = u'SEL'
    RULE_TYPES = ((CHOICE, u'choice'), (SELECTION, u'selection'))
    group = models.CharField(max_length=50, blank=True)
    function = models.CharField(max_length=50, blank=True)
    feature_name = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=50, blank=True) # keyword or feature
    dependency = models.CharField(max_length=100, blank=True)
    rule_type = models.CharField(max_length=15, blank=True, choices=RULE_TYPES)
    option_min = models.IntegerField(blank=True, null=True)
    option_max = models.IntegerField(blank=True, null=True)
    enabled = models.NullBooleanField(default=False)
    selected = models.NullBooleanField(default=False)

    def __str__(self):
        return self.name


class TestFeature2(models.Model):
    # 0-Group, 1-Function, 2-Feature_Name, 3-Feature='name', 4-Dependency, 5-Rule, 6-Min, 7-Max
    CHOICE = u'CHO'
    SELECTION = u'SEL'
    RULE_TYPES = ((CHOICE, u'choice'), (SELECTION, u'selection'))
    group = models.CharField(max_length=50, blank=True)
    function = models.CharField(max_length=50, blank=True)
    feature_name = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=50, blank=True) # keyword or feature
    rule_type = models.CharField(max_length=15, blank=True, choices=RULE_TYPES)
    option_min = models.IntegerField(blank=True, null=True)
    option_max = models.IntegerField(blank=True, null=True)
    enabled = models.NullBooleanField(default=False)
    selected = models.NullBooleanField(default=False)

    def __str__(self):
        return self.name


class TestDependency2(models.Model):
    name = models.CharField(max_length=100, blank=True)
    feature = models.ForeignKey(TestFeature2, on_delete=models.CASCADE)
