from celery import shared_task
from .models import Game, Sandbox, TimeZone
from adjudicator.adjudication import adjudicate
from django.utils import timezone
from django.db import transaction
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo

@shared_task
def adjudicate_game(game_id):
    
    game = Game.objects.get(pk=game_id)
    print(f"Beginning adjudicating game {game.name}!")
    # SO FAR only handles non-Fast adjudication.
    SPRING = 0
    FALL = 1
    WINTER = 2
    RETREAT = -1
    outcome = adjudicate(game)

    spring_fall = game.spring_fall
    percent = game.winter_retreat / 100
    winter_retreat = spring_fall * percent

    season = game.current_turn % 3
    # winter BOOL; true = winter/retreat, False = spring/fall
    winter = True if (season == WINTER or outcome == RETREAT) else False

    current = game.next_adjudication
    if winter:
        update = winter_retreat
    else:
        update = spring_fall
    delta = timedelta(minutes=update)
    
    new = current + delta
    # if fast: # Fast adjudication CHANGE: to early adjudication extra time!!!
    #     # T = adjudication period; R = time remaining before next scheduled adjudication. If R < T, add T to next adjudication.
    #     now = datetime.now(ZoneInfo(zone))
    #     if now < current: # Was adjudicated early
    #         diff = current - now
    #         if diff < delta:
    #             new += diff
    game.next_adjudication = new
    game.adjudicating = False
    game.save(update_fields=['adjudicating', 'next_adjudication'])
    print(f"Finished adjudicating game {game.name}!")
    

@shared_task
def adjudicate_sandbox(sandbox_id):
    sandbox = Sandbox.objects.get(pk=sandbox_id)
    adjudicate(sandbox)
    
@shared_task
def check_due_games():
    print("Checking!!!")
    now = timezone.now()
    with transaction.atomic():

        due_games = (
            Game.objects.select_for_update().
            filter(next_adjudication__lte=now,adjudicating=False,started=True)
            )
        for game in due_games:
            game.adjudicating = True
            game.save(update_fields=['adjudicating'])
            
            adjudicate_game.delay(game.pk)
        
        