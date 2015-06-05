__author__ = 'Hyunsoo'

import cybw
from time import sleep


client = cybw.BWAPIClient
Broodwar = cybw.Broodwar


def reconnect():
    while not client.connect():
        sleep(0.5)


def showPlayers():
    players = Broodwar.getPlayers()
    for player in players:
        Broodwar << "Player [" << player.getID() << "]: " << player.getName(
        ) << " is in force: " << player.getForce().getName() << "\n"


def showForces():
    forces = Broodwar.getForces()
    for force in forces:
        players = force.getPlayers()
        Broodwar << "Force " << force.getName() << " has the following players:\n"
        for player in players:
            Broodwar << "  - Player [" << player.getID() << "]: " << player.getName() << "\n"


def drawStats():
    line = 0
    allUnitTypes = cybw.UnitTypes.allUnitTypes()
    Broodwar.drawTextScreen(cybw.Position(5, 0), "I have " +
                            str(Broodwar.self().allUnitCount())+" units:")
    for unitType in allUnitTypes:
        count = Broodwar.self().allUnitCount(unitType)
        if count > 0:
            line += 1
            statStr = "- "+str(count)+" "+str(unitType)
            Broodwar.drawTextScreen(cybw.Position(5, 12*line), statStr)


def drawBullets():
    bullets = Broodwar.getBullets()
    for bullet in bullets:
        p = bullet.getPosition()
        velocityX = bullet.getVelocityX()
        velocityY = bullet.getVelocityY()
        lineColor = cybw.Colors.Red
        textColor = cybw.Text.Red
        if bullet.getPlayer == Broodwar.self():
            lineColor = cybw.Colors.Green
            textColor = cybw.Text.Green
        Broodwar.drawLineMap(p, p+cybw.Position(velocityX, velocityY), lineColor)
        Broodwar.drawTextMap(p, chr(textColor) + str(bullet.getType()))


def drawVisibilityData():
    wid = Broodwar.mapWidth()
    hgt = Broodwar.mapHeight()
    for x in range(wid):
        for y in range(hgt):
            drawColor = cybw.Colors.Red
            if Broodwar.isExplored(tileX=x, tileY=y):
                if Broodwar.isVisible(tileX=x, tileY=y):
                    drawColor = cybw.Colors.Green
                else:
                    drawColor = cybw.Colors.Blue

            Broodwar.drawDotMap(cybw.Position(x*32+16, y*32+16), drawColor)