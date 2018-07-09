import time

from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from Backend.models import Square, UserProfile
from Backend.utils import get_square_id_by_location, get_random_color, load_data, CHANGE_SQUARE_DELAY

'''
API documentation at https://docs.google.com/document/d/1pbdqBmTb9zvqssmj4nSL7hbwmlvXY7tLn7uxyroTjP0/edit
TODO Remove copypasta

DONE Check lat/lon consistency !important
DONE add floats
'''


'''
TODO Think about security
Adds user to db on first login
'''
@require_POST
@csrf_exempt
def add_user(request):
    data = load_data(request)

    user_id = data['user_id']
    new_user = UserProfile(user_id=user_id, color=get_random_color())
    new_user.save()

    return JsonResponse({
        'user_color': new_user.color,
    })


'''
Resets square owner
'''
@require_POST
@csrf_exempt
def set_square_state(request):
    data = load_data(request)

    user_id = data['user_id']
    latitude = float(data['latitude'])
    longitude = float(data['longitude'])

    vertical_id, horizontal_id = get_square_id_by_location(latitude, longitude)
    request_time = time.time()

    # Check if this square exists already
    if Square.objects.filter(vertical_id=vertical_id, horizontal_id=horizontal_id).exists():
        Square.objects.filter(vertical_id=vertical_id, horizontal_id=horizontal_id,
                              time_stamp_lte=(request_time-CHANGE_SQUARE_DELAY)).update(owner=user_id,
                                                                                        time_stamp=request_time)
    else:
        current_square = Square(vertical_id=vertical_id,
                                horizontal_id=horizontal_id,
                                owner=UserProfile.objects.get(user_id=user_id),
                                time_stamp=request_time)
        current_square.save()

    return JsonResponse({
        'status': 'OK',
    })


'''
TODO For later versions
TODO 0 meridian error
'''
@require_GET
def get_frame_data(request):
    data = request.GET
    response = []

    bottom_left_longitude = float(data['bottom_left_corner']['longitude'])
    bottom_left_latitude = float(data['bottom_left_corner']['latitude'])
    top_right_longitude = float(data['top_right_corner']['longitude'])
    top_right_latitude = float(data['top_right_corner']['latitude'])

    bottom_left_vertical_id, bottom_left_horizontal_id = get_square_id_by_location(bottom_left_latitude,
                                                                                   bottom_left_longitude)
    top_right_vertical_id, top_right_horizontal_id = get_square_id_by_location(top_right_latitude,
                                                                               top_right_longitude)

    for square in Square.objects.filter(horizontal_id__gte=bottom_left_horizontal_id,
                                        horizontal_id__lte=top_right_horizontal_id,
                                        vertical_id__gte=bottom_left_vertical_id,
                                        vertical_id__lte=top_right_vertical_id):
        response.append({'horizontal_id': square.horizontal_id,
                         'vertical_id': square.vertical_id,
                         'color': square.owner.color})
    return JsonResponse({
        'squares': response
    })


'''
TODO
/get_frame_data temporary replacement
'''
@require_GET
def get_squares_data(request):
    raw_squares = Square.objects.all()
    squares = []

    for square in raw_squares:
        squares.append({
            'vertical_id': square.vertical_id,
            'horizontal_id': square.horizontal_id,
            'color': square.owner.color,
        })

    return JsonResponse({
        'squares': squares,
    })


'''
Returns user's score
'''
@require_GET
def get_user_score(request):
    data = request.GET

    user_id = data['user_id']
    user_score = Square.objects.filter(owner=user_id).count()

    return JsonResponse({
        'user_score': user_score,
    })


'''
Returns top 5 users
'''
@require_GET
def get_scoreboard(request):
    raw_scoreboard = UserProfile.objects.annotate(num_squares=Count('square')).\
        order_by('-num_squares')[:5]

    scoreboard = []
    for current_user in raw_scoreboard:
        scoreboard.append({
            'user_id': current_user.user_id,
            'user_score': current_user.get_user_score(),
        })

    return JsonResponse({
        'scoreboard': scoreboard,
    })


'''
Returns nearest grid square
'''
@require_GET
def get_nearest_square(request):
    data = request.GET

    latitude = float(data['latitude'])
    longitude = float(data['longitude'])

    vertical_id, horizontal_id = get_square_id_by_location(latitude, longitude)

    return JsonResponse({
        'nearest_latitude': vertical_id,
        'nearest_longitude': horizontal_id,
    })


'''
Returns user's color by his id
'''
@require_GET
def get_user_color(request):
    data = request.GET

    user_id = data['user_id']
    user_color = UserProfile.objects.get(user_id=user_id).color

    return JsonResponse({
        'user_color': user_color,
    })


'''
Drops a bomb on user's current location
'''
@require_POST
@csrf_exempt
def drop_bomb(request):
    data = load_data(request)

    user_id = data['user_id']
    latitude = float(data['latitude'])
    longitude = float(data['longitude'])

    base_vertical_id, base_horizontal_id = get_square_id_by_location(latitude, longitude)
    request_time = time.time()

    for vertical_delta in range(-50, 51):
        for horizontal_delta in range(-50, 51):
            vertical_id = base_vertical_id + vertical_delta
            horizontal_id = base_horizontal_id + horizontal_delta

            # Check if this square exists already
            if Square.objects.filter(vertical_id=vertical_id, horizontal_id=horizontal_id).exists():
                Square.objects.filter(vertical_id=vertical_id, horizontal_id=horizontal_id,
                                      time_stamp_lte=(request_time-CHANGE_SQUARE_DELAY)).update(owner=user_id, time_stamp=request_time)
            else:
                current_square = Square(vertical_id=vertical_id,
                                        horizontal_id=horizontal_id,
                                        owner=UserProfile.objects.get(user_id=user_id),
                                        time_stamp=request_time)
                current_square.save()

    return JsonResponse({
        'status': 'OK',
    })


'''
Deletes all squares
'''
@require_POST
@csrf_exempt
def wipe(request):
    Square.objects.all().delete()

    return JsonResponse({
        'status': 'OK',
    })


@csrf_exempt
def report(request):
    try:
        print(request.META['REMOTE_ADDR'])
    except:
        pass
    try:
        print(request.META['HTTP_X_FORWARDED_FOR'])
    except:
        pass

    return HttpResponse(status=418)
