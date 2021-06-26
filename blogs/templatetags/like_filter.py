from django import template
from blogs.models import OderCommand, UserProfile,Like    
from django.db.models import Count
from django.contrib.auth.models import AbstractUser, User
register = template.Library()
        
@register.filter
def like_filter(likes, idcpesend):
    count_like = 0 
    like_obj = likes.filter(idmy_id=idcpesend)
    
    for like_status in like_obj:
        
        if like_status.status == True:
            count_like += 1
        
    
    
    return  count_like

@register.filter
def is_like_filter(idsend,idcpeto):
    like_obj = Like.objects.filter(idmy_id=idcpeto)
    like_obj_islike =like_obj.filter(id_someone = idsend)
    
    like_obj_find_len = len(like_obj.filter(id_someone = idsend))
    if like_obj_find_len == 1 :
        for like in like_obj_islike:
            if(like.status == True):
                return True
    return False

@register.filter
def get_oderid_like(idsend,idcpeto):
    like_obj = Like.objects.filter(idmy_id=idcpeto)
    like_obj_islike =like_obj.filter(id_someone = idsend)
    like_obj_find_len = len(like_obj.filter(id_someone = idsend))
    if like_obj_find_len == 0:
        oder = Like.objects.create \
                            (
                            id_someone=idsend,
                            idmy_id=idcpeto,
                            status=False
                        )
        oder.save()
        like_obj = Like.objects.filter(idmy_id=idcpeto)
        like_obj_islike =like_obj.filter(id_someone = idsend)
        for like in like_obj_islike:
            return like.id
        
    
    for like in like_obj_islike:
        return like.id
    
@register.filter
def is_like_filter_appsend(id):
    likeobj =  Like.objects.filter(idmy_id=id)
    like_obj_status = likeobj.filter(status=True)
    
    
    return len(like_obj_status)

@register.filter
def findrank(id):
    
    like_obj = Like.objects.filter(status=True)
    
    likeobj = Like.objects.filter(status=True)
    users = User.objects.filter()
    maxcount = 0
    maxobj = None
    for user in users:
        countlike =  len(like_obj.filter(idmy_id = user.id))
        if countlike > maxcount:
            maxcount = countlike
            maxobj = user
    

    userpic = UserProfile.objects.get(user_id = maxobj.id)
    return userpic.profile_pic.url