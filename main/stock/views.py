from django.shortcuts import render
from django.contrib.auth import get_user_model
from .simulator import simulate, read_from_mongodb,flush_mongodb
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from django.http import JsonResponse

User= get_user_model()


def user_dashboard(request):
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    trades_data = read_from_mongodb(account=5015389644,type='read', timestamp=ten_minutes_ago, limit=10)
    equity = []
    timestamps = []
    
    for data in trades_data:
        equity.append(data['equity'])
        timestamp = datetime.fromtimestamp(data['timestamp']).time()
        minute = str(timestamp.minute).zfill(2)  # Add leading zero if minute is a single digit
        timestamps.append(f"{timestamp.hour}:{minute}")

    
    context = {'timestamps': mark_safe(timestamps), 'equity': equity}
    return render(request, 'user_dashboard.html', context)
   
def poll(request):
    account=request.GET.get('account')
    timestamp = datetime.now()
    trade = read_from_mongodb(account=account, type='poll',limit=1, timestamp=timestamp)
    
    if trade:
        equity = trade[0]['equity']
        timestamp_str = f"{datetime.fromtimestamp(trade[0]['timestamp']).time().hour}:{datetime.fromtimestamp(trade[0]['timestamp']).time().minute}"
    else:
        equity = None
        timestamp_str = None
        
    return JsonResponse({'equity': equity, 'timestamp': mark_safe(timestamp_str)})


# def admin_dashboard(request):
#     colors = ['#f10075', '#00ff00', '#0000ff', '#ff00ff', '#ffff00', '#00ffff', '#ff0000', '#800080', '#008000', '#000080']
#     user_data = {}
#     timestamps = []
#     for id in range(1,11):
#         ten_minutes_ago = datetime.now() - timedelta(minutes=10)
#         trades_data = read_from_mongodb(account=5015389644,type='read', timestamp=ten_minutes_ago, limit=10)
#         for data in trades_data:
#             user_id = data.get('5015389644')
#             if user_id not in user_data:
#                 user_data[user_id] = {
#                     'equity': [],
#                     'color': colors.pop(0) if colors else None
#                 }
#             user_data[user_id]['equity'].append(data['equity'])
#             # timestamp = f"{datetime.fromtimestamp(data['timestamp']).time().hour}:{datetime.fromtimestamp(data['timestamp']).time().minute}"
#             timestamp_str = datetime.fromtimestamp(data['timestamp']).time()
#             minute = str(timestamp_str.minute).zfill(2)  # Add leading zero if minute is a single digit
#             timestamp=f"{timestamp_str.hour}:{minute}"
#             if timestamp not in timestamps:
#                 timestamps.append(timestamp)
#     print(user_data)
#     context = {'user_data': user_data, 'timestamps': mark_safe(timestamps)}
#     return render(request, 'admin.html', context)

