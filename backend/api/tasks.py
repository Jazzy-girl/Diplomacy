from celery import shared_task
from .models import *


@shared_task
def adjudicate_game(game_id):
    from adjudicator.adjudication import adjudicate
    game = Game.objects.get(pk=game_id)
    # add check to see if game.next_adjudication is now?
    adjudicate(game)

@shared_task
def adjudicate_sandbox(sandbox_id):
    from adjudicator.adjudication import adjudicate
    sandbox = Sandbox.objects.get(pk=sandbox_id)
    adjudicate(sandbox)
    

