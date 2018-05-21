# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from .models import Group, Function, Feature, Dependency
from django.views.generic import ListView
from django.shortcuts import get_object_or_404

class GroupList(ListView):
    model = Group


class FunctionList(ListView):
    model = Function


class FeatureList(ListView):
    queryset = Feature.objects.select_related(u'function', u'function__group').all()


class GroupFunctionList(ListView):
    template_name = u'fmm/function_by_group.html'
    context_object_name = u'group'

    def get_queryset(self):
        self.group_number = get_object_or_404(Group, pk=int(self.kwargs[u'group_number']))
        return Function.objects.filter(group=self.group_number)

    def get_context_data(self, **kwargs):
        context = super(GroupFunctionList, self).get_context_data(**kwargs)
        context[u'group_name'] = Group.objects.get(pk=int(self.kwargs[u'group_number']))
        return context


class FunctionFeatureList(ListView):
    template_name = u'fmmgui/feature_by_function.html'
    context_object_name = u'function'

    def get_queryset(self):
        self.group_pk = int(self.kwargs[u'group_number'])
        self.function_pk = int(self.kwargs[u'function_number'])
        return Feature.objects.filter(function=self.function_pk)

    def get_context_data(self, **kwargs):
        context = super(FunctionFeatureList, self).get_context_data(**kwargs)
        group_name = Group.objects.get(pk=self.group_pk).name
        function_name = Function.objects.get(pk=self.function_pk).name
        context[u'group_name'] = group_name
        context[u'function_name'] = function_name
        return context


def detail(request, feature_id):
    return HttpResponse(u"You're looking at feature %s." % feature_id)


def index(request):
    return HttpResponse(u"You're looking at fmmgui home page.")


def loadfmm(request):
    fmm = open(u'FMM.txt', u'r')
    line_count = 0
    if Group.objects.count() > 0:
        Group.objects.all().delete()
    for line in fmm:
        line_data = line.rstrip().split(u',')
        group_name = line_data[0]
        function_name = line_data[1]
        feature_name = line_data[2]
        selection_name = line_data[3]
        dependencies = line_data[4].split(u';')
        rule_type = line_data[5]
        option_min = line_data[6]
        option_max = line_data[7]
        groups = Group.objects.filter(name=group_name)
        if not groups.exists():
            group = Group(name=group_name)
            group.save()
        group = Group.objects.get(name=group_name)
        functions = Function.objects.filter(name=function_name, group__name=group_name)
        if not functions.exists():
            function = group.function_set.create(name=function_name)
            function.save()
        function = Function.objects.get(name=function_name, group__name=group_name)
        features = Feature.objects.filter(name=feature_name, function__name=function_name, function__group__name=group_name)
        if features.count() == 0:
            feature = function.feature_set.create(name=feature_name)
            feature.selection_name = selection_name
            feature.rule_type = rule_type
            feature.option_min = option_min
            feature.option_max = option_max
            feature.save()
        feature = Feature.objects.get(name=feature_name, function__name=function_name, function__group__name=group_name)
        for dependency in dependencies:
            if dependency != u'n/a':
                feature.dependency_set.create(name=dependency)

        feature.save()
        line_count += 1

    response_text = u'FMM.txt load complete. ' + str(line_count) + u' records Processed. '
    return HttpResponse(response_text)
