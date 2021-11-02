import datetime
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from school.models import Children, Applications, Classes
from school.application_status import ApplicationStatus


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request, format=None):
    return Response(get_user_profile(request.user))


def get_user_profile(user: User):
    if is_parent(user):
        return get_parent_profile(user)
    elif is_teacher(user):
        return get_teacher_profile(user)
    else:
        return {}


def has_group(user: User, group_name):
    return len(list(filter(lambda g: g.name == group_name, user.groups.all())))


def is_parent(user: User):
    return has_group(user, 'Parents')


def is_teacher(user: User):
    return has_group(user, 'Teachers')


def get_parent_profile(user: User):
    return {
        'type': 'parent',
        "name": user.get_full_name(),
        "times": {
            "from": "17:45",
            "to": "23:00",
            "step": 15
        },
        "children": get_children(user)
    }


def get_children(user: User):
    return [get_child(c) for c in Children.objects.filter(parent_id=user.pk)]


def get_child(child: Children):
    return {
        'id': child.id,
        'label': {
            'rus': child.name_rus,
            'eng': child.name_eng
        },
        'application': get_application(child)
    }


def get_today_application(child: Children):
    return Applications.objects.filter(child=child, date__gte=datetime.date.today())


def get_application(child: Children):
    app = get_today_application(child).first()
    if app is None:
        return ''
    else:
        return {
            'date': app.date,
            'status': app.status
        }


def get_teacher_pupils(user: User):
    cls = Classes.objects.filter(teacher=user).first()
    if cls is None:
        return []
    d = {}
    for c in Children.objects.filter(grade=cls):
        app = get_application(c)
        if app == '':
            appLabel = 'unassigned'
        else:
            appLabel = app['date'].strftime('%H:%M')
        if appLabel not in d:
            d[appLabel] = [get_child(c)]
        else:
            d[appLabel].append(get_child(c))
    return d


def get_teacher_profile(user: User):
    return {
        "type": "teacher",
        "name": user.get_full_name(),
        "children": get_teacher_pupils(user)
    }

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_application(request, format=None):
    child = Children.objects.get(id=int(request.POST.get('id')))
    if child is None:
        raise ValueError('Unknown child')

    get_today_application(child).delete()

    now = datetime.datetime.now()
    t = datetime.datetime.strptime(request.POST.get('time'), "%H:%M")
    time = datetime.datetime(now.year, now.month, now.day, t.hour, t.minute, 0)
    app = Applications(
        child=child,
        date=time
    )
    app.save()

    return Response({'id': app.id})

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def set_application_status(request, format=None):
    print(request.POST)
    child = Children.objects.get(id=int(request.POST.get('child_id', '')))
    if child is None:
        raise ValueError('Unknown child')

    app = get_today_application(child).first()
    if app is None:
        raise ValueError('Unknown application')

    status = int(request.POST.get('status', ''))
    if not ApplicationStatus.valid(status):
        raise ValueError('Invalid status')

    app.status = status
    app.save()
    return Response({'id': app.id, status: app.status})
