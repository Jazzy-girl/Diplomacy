from celery import shared_task
from .models import Game, Sandbox
from adjudicator.adjudication import adjudicate
from django.utils import timezone
from django.db import transaction
from datetime import timedelta


@shared_task
def adjudicate_game(game_id):
    game = Game.objects.get(pk=game_id)
    # SO FAR only handles non-Fast adjudication.
    SPRING = 0
    FALL = 1
    WINTER = 2
    RETREAT = -1
    outcome = adjudicate(game)

    data = game.settings.get('adjudication')
    unit = data.get('regular_unit')
    spring_fall = data.get('spring_fall')
    percent = data.get('winter_retreat') / 100
    winter_retreat = spring_fall * percent

    season = game.current_turn % 3
    # winter BOOL; true = winter/retreat, False = spring/fall
    winter = True if (season == WINTER or outcome == RETREAT) else False

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
    game.adjudicating = False
    game.save(update_fields=['adjudicating', 'next_adjudication'])
    

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
        game.save(update_fields=['adjudicating'])
        adjudicate_game.delay(game.pk)