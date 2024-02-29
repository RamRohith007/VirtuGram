from django.shortcuts import render
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
from django.views.decorators.csrf import csrf_exempt
from .models import RoomMember
import random
import time
import json

# Create your views here.
def lobby(request):
    return render(request,"chatgram/lobby.html")

def room(request):
    return render(request,"chatgram/room.html")


#--Agora
def getToken(request):
    appId = '7a23baea19734f39982ceb49a634eed1'
    appCertificate = '19d2a9983e854b74bb224469fd4519f5'
    channelName = request.GET.get('channel')
    uid = random.randint(1,230)
    expirationTimeInSeconds = 3600 * 24
    currentTimestamp = time.time()
    privilegeExpiredTs = currentTimestamp + expirationTimeInSeconds
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token, 'uid':uid},safe=False)

#--Username
@csrf_exempt
def createMember(request):
    data = json.loads(request.body)

    member, created = RoomMember.objects.get_or_create(
        name = data['name'], 
        uid = data['UID'],
        room_name = data['room_name']
    )
    return JsonResponse({'name':data['name']}, safe=False)

def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid = uid,
        room_name = room_name,
    )

    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)

    member = RoomMember.objects.get(
        name = data['name'],
        uid = data['UID'],
        room_name = data['room_name'],
    )
    member.delete()
    return JsonResponse('Member was deleted!', safe=False)