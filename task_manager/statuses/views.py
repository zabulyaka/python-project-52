from django.shortcuts import redirect, render
from django.views import View

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusesView(View):
    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        url = 'statuses/statuses_show.html'
        context = {'statuses': statuses}
        return render(request, url, context)


class StatusViewCreate(View):
    def get(self, request, *args, **kwargs):
        form = StatusForm()
        url = 'statuses/status_create.html'
        context = {'form': form}
        return render(request, url, context)

    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        url = 'statuses/status_create.html'
        context = {'form': form}
        if form.is_valid():
            status = Status(name=form.cleaned_data['name'])
            status.save()
            return redirect('statuses_show')
        return render(request, url, context)

class StatusViewUpdate(View):
    def get(self, request, *args, **kwargs):
        status_pk = kwargs.get('pk')
        status = Status.objects.get(pk=status_pk)
        form = StatusForm(instance=status)
        url = 'statuses/status_update.html'
        context = {'form': form, 'status': status}
        return render(request, url, context)

    def post(self, request, *args, **kwargs):
        status_pk = kwargs.get('pk')
        status = Status.objects.get(pk=status_pk)
        form = StatusForm(request.POST, instance=status)
        url = 'statuses/status_update.html'
        context = {'form': form, 'status': status}
        if form.is_valid():
            form.save()
            return redirect('statuses_show')
        return render(request, url, context)

class StatusViewDelete(View):
    def get(self, request, *args, **kwargs):
        status_pk = kwargs.get('pk')
        status = Status.objects.get(pk=status_pk)
        url = 'statuses/status_delete.html'
        context = {'status': status}
        return render(request, url, context)

    def post(self, request, *args, **kwargs):
        status_pk = kwargs.get('pk')
        status = Status.objects.get(pk=status_pk)
        if status:
            status.delete()
        return redirect('statuses_show')
