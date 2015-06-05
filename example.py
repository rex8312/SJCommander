import cybw

from utils import reconnect
from utils import Broodwar
from utils import client
from utils import showPlayers
from utils import showForces
from utils import drawBullets
from utils import drawVisibilityData
from utils import drawStats


if __name__ == '__main__':
    print("Connecting...")
    reconnect()
    while True:
        print("waiting to enter match")
        while not Broodwar.isInGame():
            client.update()
            if not client.isConnected():
                print("Reconnecting...")
                reconnect()
        print("starting match!")
        Broodwar.sendText( "Hello world from python!")
        Broodwar.printf( "Hello world from python!")

        # need newline to flush buffer
        Broodwar << "The map is " << Broodwar.mapName() << ", a " \
            << len(Broodwar.getStartLocations()) << " player map" << " \n"

        # Enable some cheat flags
        Broodwar.enableFlag(cybw.Flag.UserInput)

        show_bullets = False
        show_visibility_data = False

        if Broodwar.isReplay():
            Broodwar << "The following players are in this replay:\n"
            players = Broodwar.getPlayers()
            # TODO add rest of replay actions

        else:
            Broodwar << "The matchup is " << Broodwar.self().getRace() << " vs " << Broodwar.enemy().getRace() << "\n"
            # send each worker to the mineral field that is closest to it
            units    = Broodwar.self().getUnits()
            minerals  = Broodwar.getMinerals()
            print("got", len(units), "units")
            print("got", len(minerals), "minerals")
            for unit in units:
                if unit.getType().isWorker():
                    closestMineral = None
                    # print("worker")
                    for mineral in minerals:
                        if closestMineral is None or unit.getDistance(mineral) < unit.getDistance(closestMineral):
                            closestMineral = mineral
                    if closestMineral:
                        unit.rightClick(closestMineral)
                elif unit.getType().isResourceDepot():
                    unit.train(Broodwar.self().getRace().getWorker())
            events = Broodwar.getEvents()
            print(len(events))

        while Broodwar.isInGame():
            events = Broodwar.getEvents()
            for e in events:
                eventtype = e.getType()
                if eventtype == cybw.EventType.MatchEnd:
                    if e.isWinner():
                        Broodwar << "I won the game\n"
                    else:
                        Broodwar << "I lost the game\n"
                elif eventtype == cybw.EventType.SendText:
                    if e.getText() == "/show bullets":
                        show_bullets = not show_bullets
                    elif e.getText() == "/show players":
                        showPlayers()
                    elif e.getText() == "/show forces":
                        showForces()
                    elif e.getText() == "/show visibility":
                        show_visibility_data = not show_visibility_data
                    else:
                        Broodwar << "You typed \"" << e.getText() << "\"!\n"
                elif eventtype == cybw.EventType.ReceiveText:
                    Broodwar << e.getPlayer().getName() << " said \"" << e.getText() << "\"\n"
                elif eventtype == cybw.EventType.PlayerLeft:
                    Broodwar << e.getPlayer().getName() << " left the game.\n"
                elif eventtype == cybw.EventType.NukeDetect:
                    if e.getPosition() is not cybw.Positions.Unknown:
                        Broodwar.drawCircleMap(e.getPosition(), 40,
                            cybw.Colors.Red, True)
                        Broodwar << "Nuclear Launch Detected at " << e.getPosition() << "\n"
                    else:
                        Broodwar << "Nuclear Launch Detected.\n"
                elif eventtype == cybw.EventType.UnitCreate:
                    if not Broodwar.isReplay():
                        Broodwar << "A " << e.getUnit() << " has been created at " << e.getUnit().getPosition() << "\n"
                    else:
                        if(e.getUnit().getType().isBuilding() and
                          (e.getUnit().getPlayer().isNeutral() == False)):
                            seconds = Broodwar.getFrameCount()/24
                            minutes = seconds/60
                            seconds %= 60
                            Broodwar.sendText(str(minutes)+":"+str(seconds)+": "+e.getUnit().getPlayer().getName()+" creates a "+str(e.getUnit().getType())+"\n")
                elif eventtype == cybw.EventType.UnitDestroy:
                    if not Broodwar.isReplay():
                        Broodwar << "A " << e.getUnit() << " has been destroyed at " << e.getUnit().getPosition() << "\n"
                elif eventtype == cybw.EventType.UnitMorph:
                    if not Broodwar.isReplay():
                        Broodwar << "A " << e.getUnit() << " has been morphed at " << e.getUnit().getPosition() << "\n"
                    else:
                        # if we are in a replay, then we will print out the build order
                        # (just of the buildings, not the units).
                        if e.getUnit().getType().isBuilding() and not e.getUnit().getPlayer().isNeutral():
                            seconds = Broodwar.getFrameCount()/24
                            minutes = seconds/60
                            seconds %= 60
                            Broodwar << str(minutes) << ":" << str(seconds) << ": " << e.getUnit().getPlayer().getName() << " morphs a " << e.getUnit().getType() << "\n"
                elif eventtype == cybw.EventType.UnitShow:
                    if not Broodwar.isReplay():
                        Broodwar << e.getUnit() << " spotted at " << e.getUnit().getPosition() << "\n"
                elif eventtype == cybw.EventType.UnitHide:
                    if not Broodwar.isReplay():
                        Broodwar << e.getUnit() << " was last seen at " << e.getUnit().getPosition() << "\n"
                elif eventtype == cybw.EventType.UnitRenegade:
                    if not Broodwar.isReplay():
                        Broodwar << e.getUnit() << " is now owned by " << e.getUnit().getPlayer() << "\n"
                elif eventtype == cybw.EventType.SaveGame:
                    Broodwar << "The game was saved to " << e.getText() << "\n"
            if show_bullets:
                drawBullets()
            if show_visibility_data:
                drawVisibilityData()
            drawStats()
            Broodwar.drawTextScreen(cybw.Position(300, 0), "FPS: " +
                str(Broodwar.getAverageFPS()))
            client.update()

