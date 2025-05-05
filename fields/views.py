from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Field, Crop, SoilData
from .forms import FieldForm, CropForm, SoilDataForm
from weather.utils import get_current_weather, get_forecast


@login_required
def field_list(request):
    fields = Field.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'fields/field_list.html', {'fields': fields})


@login_required
def field_create(request):
    if request.method == 'POST':
        form = FieldForm(request.POST, request.FILES)
        if form.is_valid():
            field = form.save(commit=False)
            field.owner = request.user
            field.save()
            messages.success(request, f'Field "{field.name}" created successfully!')
            return redirect('fields:field_detail', pk=field.pk)
    else:
        form = FieldForm()
    
    return render(request, 'fields/field_form.html', {
        'form': form,
        'title': 'Add New Field'
    })


@login_required
def field_detail(request, pk):
    field = get_object_or_404(Field, pk=pk, owner=request.user)
    crops = field.crops.all().order_by('-planting_date')
    soil_data = field.soil_data.all()[:5]
    
    # Get weather data for this field
    weather_data = None
    forecast_data = None
    if field.latitude and field.longitude:
        weather_data = get_current_weather(field.latitude, field.longitude)
        forecast_data = get_forecast(field.latitude, field.longitude)
    
    context = {
        'field': field,
        'crops': crops,
        'soil_data': soil_data,
        'weather_data': weather_data,
        'forecast_data': forecast_data
    }
    
    return render(request, 'fields/field_detail.html', context)


@login_required
def field_update(request, pk):
    field = get_object_or_404(Field, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = FieldForm(request.POST, request.FILES, instance=field)
        if form.is_valid():
            form.save()
            messages.success(request, f'Field "{field.name}" updated successfully!')
            return redirect('fields:field_detail', pk=field.pk)
    else:
        form = FieldForm(instance=field)
    
    return render(request, 'fields/field_form.html', {
        'form': form,
        'field': field,
        'title': 'Update Field'
    })


@login_required
def field_delete(request, pk):
    field = get_object_or_404(Field, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        field_name = field.name
        field.delete()
        messages.success(request, f'Field "{field_name}" deleted successfully!')
        return redirect('fields:field_list')
    
    return render(request, 'fields/field_confirm_delete.html', {'field': field})


@login_required
def crop_create(request, field_pk):
    field = get_object_or_404(Field, pk=field_pk, owner=request.user)
    
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.field = field
            crop.save()
            messages.success(request, f'Crop "{crop.name}" added to {field.name}!')
            return redirect('fields:field_detail', pk=field.pk)
    else:
        form = CropForm()
    
    return render(request, 'fields/crop_form.html', {
        'form': form,
        'field': field,
        'title': 'Add New Crop'
    })


@login_required
def crop_detail(request, pk):
    crop = get_object_or_404(Crop, pk=pk, field__owner=request.user)
    field = crop.field
    
    return render(request, 'fields/crop_detail.html', {
        'crop': crop,
        'field': field
    })


@login_required
def crop_update(request, pk):
    crop = get_object_or_404(Crop, pk=pk, field__owner=request.user)
    
    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            messages.success(request, f'Crop "{crop.name}" updated successfully!')
            return redirect('fields:crop_detail', pk=crop.pk)
    else:
        form = CropForm(instance=crop)
    
    return render(request, 'fields/crop_form.html', {
        'form': form,
        'crop': crop,
        'field': crop.field,
        'title': 'Update Crop'
    })


@login_required
def crop_delete(request, pk):
    crop = get_object_or_404(Crop, pk=pk, field__owner=request.user)
    field = crop.field
    
    if request.method == 'POST':
        crop_name = crop.name
        crop.delete()
        messages.success(request, f'Crop "{crop_name}" deleted successfully!')
        return redirect('fields:field_detail', pk=field.pk)
    
    return render(request, 'fields/crop_confirm_delete.html', {
        'crop': crop,
        'field': field
    })


@login_required
def soil_data_create(request, field_pk):
    field = get_object_or_404(Field, pk=field_pk, owner=request.user)
    
    if request.method == 'POST':
        form = SoilDataForm(request.POST)
        if form.is_valid():
            soil_data = form.save(commit=False)
            soil_data.field = field
            soil_data.save()
            messages.success(request, f'Soil data added for {field.name}!')
            return redirect('fields:field_detail', pk=field.pk)
    else:
        form = SoilDataForm()
    
    return render(request, 'fields/soil_data_form.html', {
        'form': form,
        'field': field,
        'title': 'Add Soil Data'
    })


@login_required
def soil_data_list(request, field_pk):
    field = get_object_or_404(Field, pk=field_pk, owner=request.user)
    soil_data = field.soil_data.all().order_by('-reading_date')
    
    return render(request, 'fields/soil_data_list.html', {
        'field': field,
        'soil_data': soil_data
    })