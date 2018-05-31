# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from .models import Group, Function, Feature, Dependency, TestFeature
from .forms import NameForm


class GroupList(ListView):
    model = Group


class FunctionList(ListView):
    model = Function


class FeatureList(ListView):
    queryset = Feature.objects.select_related(u'function', u'function__group').all()


class DependencyList(ListView):
    queryset = Group.objects.prefetch_related('function','function__feature','function__feature__dependency')
    template_name = 'fmm/dependency_list.html'

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


# =============================================================================

def fmm_main(request, group_number):
    if Group.objects.filter(pk=group_number).count() > 0:
        group = Group.objects.get(pk=group_number)
        group_name = group.name
        group_list = list(Group.objects.order_by('name'))
    else:
        group_name = "Group_Not_Found"
        return HttpResponse(u"/fmm/fmm_main/%s" % group_name)

    template = 'fmm/fmm_main.html'
    feature_list = feature_list = Feature.objects.filter(function__group__pk=group_number)

    context = {'group_name': group_name, 'group_list': group_list, 'feature_list': feature_list}
    return render(request, template, context)


def fmm_main_index(request):
    groups = Group.objects.order_by('name')
    first_group = str(groups[0].pk)
    return HttpResponseRedirect(u"/fmm/fmm_main/%s" % first_group)

# =============================================================================


def loadfmm_old(request):
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
        if not features.exists():
            feature = function.feature_set.create(name=feature_name)
            feature.selection_name = selection_name
            feature.rule_type = rule_type
            feature.option_min = option_min
            feature.option_max = option_max
            feature.save()
        feature = Feature.objects.get(name=feature_name, function__name=function_name, function__group__name=group_name)
        for dependency in dependencies:

            feature.dependency_set.create(name=dependency)

        feature.save()
        line_count += 1
        print "lines processed:", line_count

    response_text = u'FMM.txt load complete. ' + str(line_count) + u' records Processed. '
    return HttpResponse(response_text)


def get_name(request):
    print "get_name: request_method", request.method
    if request.method == 'POST':
        form = NameForm(request.POST)
        print "form is valid?", form.is_valid()
        if form.is_valid():
            return HttpResponseRedirect('/fmm/yourname/')
    else:
        form = NameForm()

    return render(request, 'name.html',{'form': form})


def test(request):
    print "test view"
    return render(request, 'fmm/test.html/', {})

# =============================================================================
# Need to fix problem of grabbing features with same names.  I think that is why the linking sometimes does not work.
def edit_feature(request, feature_number):
    template = 'fmm/feature_detail.html'
    feature = Feature.objects.get(pk=feature_number)
    dependency_list =  Dependency.objects.filter(feature__pk=feature_number)
    print "view: edit_feature, feature:", feature, feature.pk, "; dependencies: ", dependency_list
    if dependency_list.count >0:
        for d in dependency_list:
            print "dependency: ", d.pk, d.name
    context = {'feature': feature, 'dependency_list':dependency_list}
    return render(request, template, context)

# =============================================================================
class TestFeatureList(ListView):
    model = TestFeature


def loadfmm(request):
    fmm = open(u'FMM.txt', u'r')
    line_count = 0
    print "lfmm: ", TestFeature.objects.count()
    if TestFeature.objects.count() > 0:
        TestFeature.objects.all().delete()
    print "lfmm: ", TestFeature.objects.count()
    for line in fmm:
        # 0-Group, 1-Function, 2-Feature_Name, 3-Feature, 4-Dependency, 5-Rule, 6-Min, 7-Max

        # group = models.CharField(max_length=50, blank=True)
        # function = models.CharField(max_length=50, blank=True)
        # feature_name = models.CharField(max_length=100, blank=True)
        # name = models.CharField(max_length=50, blank=True)  # keyword or feature
        # dependency = models.ManyToManyField("self", symmetrical=False)
        # rule_type = models.CharField(max_length=15, blank=True, choices=RULE_TYPES)
        # option_min = models.IntegerField(blank=True, null=True)
        # option_max = models.IntegerField(blank=True, null=True)
        # enabled = models.NullBooleanField(default=False)
        # selected = models.NullBooleanField(default=False)

        line_data = line.rstrip().split(u',')
        group_name = line_data[0]
        function_name = line_data[1]
        feature_name = line_data[2]
        feature = line_data[3] # 'name' in the model
        dependencies = line_data[4].split(u';')
        rule_type = line_data[5]
        option_min = line_data[6]
        option_max = line_data[7]

        # for dependency in dependencies:
        #     print "dep1:", dependency, TestFeature.objects.filter(name=dependency).count()
        #
        # for dependency in dependencies:
        #     if TestFeature.objects.filter(name=dependency).count() == 0:
        #         t = TestFeature(name=dependency)
        #         t.save()
        #
        # for dependency in dependencies:
        #     print "dep2:", dependency, TestFeature.objects.filter(name=dependency).count()
        #
        # print "lfmm3: ", feature, dependencies
        # print "lfmm4: ",
        # for t in TestFeature.objects.all():
        #     print t.pk, t.name
        # for dependency in dependencies:

        t = TestFeature(
            group=group_name,
            function=function_name,
            feature_name=feature_name,
            name=feature,
            dependency=dependencies,
            rule_type=rule_type,
            option_min=option_min,
            option_max=option_max
          )
        t.save()

        line_count += 1
        print "lines processed:", line_count

    response_text = u'FMM.txt load complete. ' + str(line_count) + u' records Processed. '
    return HttpResponse(response_text)
