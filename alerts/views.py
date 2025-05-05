from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Alert
from django.http import JsonResponse


@login_required
def alert_list(request):
    """View all alerts"""
    alerts = Alert.objects.filter(user=request.user)
    unread_count = alerts.filter(is_read=False).count()
    
    # Filter by category if requested
    category = request.GET.get('category', None)
    if category and category != 'all':
        alerts = alerts.filter(category=category)
    
    # Filter by level if requested
    level = request.GET.get('level', None)
    if level and level != 'all':
        alerts = alerts.filter(level=level)
    
    # Filter by read status if requested
    status = request.GET.get('status', None)
    if status == 'read':
        alerts = alerts.filter(is_read=True)
    elif status == 'unread':
        alerts = alerts.filter(is_read=False)
    
    context = {
        'alerts': alerts,
        'unread_count': unread_count,
        'selected_category': category or 'all',
        'selected_level': level or 'all',
        'selected_status': status or 'all',
    }
    
    return render(request, 'alerts/alert_list.html', context)


@login_required
def alert_detail(request, pk):
    """View a specific alert"""
    alert = get_object_or_404(Alert, pk=pk, user=request.user)
    
    # Mark as read when viewed
    if not alert.is_read:
        alert.is_read = True
        alert.save()
    
    return render(request, 'alerts/alert_detail.html', {'alert': alert})


@login_required
def mark_alert_read(request, pk):
    """Mark an alert as read"""
    alert = get_object_or_404(Alert, pk=pk, user=request.user)
    alert.is_read = True
    alert.save()
    
    # If AJAX request, return JSON response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    messages.success(request, 'Alert marked as read.')
    return redirect('alerts:alert_list')


@login_required
def mark_all_read(request):
    """Mark all alerts as read"""
    Alert.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    # If AJAX request, return JSON response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    messages.success(request, 'All alerts marked as read.')
    return redirect('alerts:alert_list')