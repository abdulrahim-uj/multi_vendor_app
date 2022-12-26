from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from main.functions import get_auto_id
from accounts.models import User, UserProfile

# RECOMMENDED WAY
'''
    ========================== POST_SAVE SIGNAL ==========================
    ONCE USER IS CREATED, AUTOMATICALLY CREATE A ROW IN USERPROFILE TABLE
    IF created: IS GETTING TRUE ONCE USER CREATED
        THEN CREATE NEW ROW IN USERPROFILE WITH VALUES
        [BY DEFAULT USER=INSTANCE IS ENEF, BUT OTHER FILEDS ARE MANDATORY]
    ELSE CASE WILL RUN ON USER TABLE UPDATE TIME
    TRY BLOCK CHECK USERPROFILE EXIST? IF THEN JUST SAVE, 
        OR GOTO EXCEPT BLOCK
    EXCEPT BLOCK WILL CREATE A NEW ROW ON USERPROFILE TABLE
        [SAME STEP AS IF CREATED:]
'''


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        autoid = get_auto_id(UserProfile)
        creator_id = instance
        updater_id = instance
        UserProfile.objects.create(user=instance, auto_id=autoid, creator=creator_id,
                                   updater=updater_id)
    else:
        # If created == False [update case]
        try:
            user_profile = UserProfile.objects.get(user=instance)
            user_profile.save()
        except:
            # Create Userprofile if it does not exist
            autoid = get_auto_id(UserProfile)
            creator_id = instance
            updater_id = instance
            UserProfile.objects.create(user=instance, auto_id=autoid,
                                       creator=creator_id, updater=updater_id)
# EASY WAY
# post_save.connect(receiver=post_save_create_profile_receiver, sender=User)


'''
    ========================== PRE_SAVE SIGNAL ==========================
    IT WILL EXECUTE BEFORE SAVING THE USER 
'''


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    # print(instance.username, 'This user is being saved...')
    pass
