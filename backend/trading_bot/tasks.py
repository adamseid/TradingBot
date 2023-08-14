from celery import shared_task
from .task_modules import UpdateRaw, UpdateAnalysis, UpdateFrontend, UpdateSimulation


@shared_task(name='updateAnalysis')
def updateAnalysis():
    print('UPDATEANALYSIS')
    UpdateAnalysis.run()


@shared_task(name='updateFrontend')
def updateFrontend():
    print('UPDATEFRONTEND')
    UpdateFrontend.run()


@shared_task(name='updateSimulation')
def updateSimulation():
    print('UPDATESIMULATION')
    UpdateSimulation.run()


@shared_task(name='updateRaw')
def updateRaw():
    print('UPDATERAW')
    UpdateRaw.run()
