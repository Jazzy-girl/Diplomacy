from celery import shared_task
from .models import Game, Sandbox
from adjudicator.adjudication import adjudicate
from django.utils import timezone
from django.db import transaction
from datetime import timedelta


@shared_task
def adjudicate_game(game_id):
    game = Game.objects.get(pk=game_id)
    # add check to see if game.next_adjudication is now?
    SPRING = 0
    FALL = 1
    WINTER = 2
    outcome = adjudicate(game)
    # get adjudication time - JSON; game.settings.get(...)

    def _update_adjudication_time(game:Game, winter=False):
        data = game.settings.get('adjudication')
        unit = data.get('regular_unit')
        spring_fall = data.get('spring_fall')
        winter_retreat = spring_fall / data.get('winter_retreat')

        # winter BOOL; true = winter/retreat, False = spring/fall
        if winter:
            update = winter_retreat
        else:
            update = spring_fall
        if unit == Game.AdjudicationLength.DAYS:
            delta = timedelta(days=update)
        elif unit == Game.AdjudicationLength.HOURS:
            delta = timedelta(hours=update)
        elif unit == Game.AdjudicationLength.MINUTES:
            delta = timedelta(minutes=update)
        current = game.next_adjudication
        new = current + delta
        game.next_adjudication = new
        game.save(update_fields=['next_adjudication'])

    season = game.current_turn % 3
    winter = True if (season == WINTER or outcome == -1) else False
    _update_adjudication_time(game, winter)
    game.adjudicating = False
    game.save(update_fields=['adjudicating'])
    

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
