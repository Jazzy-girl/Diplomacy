from celery import shared_task
from .models import Game, Sandbox
from adjudicator.adjudication import adjudicate
from django.utils import timezone
from django.db import transaction


@shared_task
def adjudicate_game(game_id):
    game = Game.objects.get(pk=game_id)
    # add check to see if game.next_adjudication is now?
    SPRING = 0
    FALL = 1
    WINTER = 2
    outcome = adjudicate(game)
    # get adjudication time - JSON; game.settings.get(...)
    if outcome == -1:
        # retreats.
        pass
    else:
        season = game.current_turn % 3
        if season == SPRING or FALL:
            pass
        else: # season == WINTER
            pass
    game.adjudicating = False
    game.save()
    

@shared_task
def adjudicate_sandbox(sandbox_id):
    sandbox = Sandbox.objects.get(pk=sandbox_id)
    adjudicate(sandbox)
    
@shared_task
def check_due_games():
    now = timezone.now()
    with transaction.atomic():

        due_games = (
            Game.objects.select_for_update().
            filter(next_adjudication__lte=now,adjudicating=False)
            )
    for game in due_games:
        game.adjudicating = True
        game.save()
        adjudicate_game.delay(game.id)
