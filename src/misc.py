from pyplc.pou import POU
from pyplc.sfc import SFC
from pyplc.utils.trig import TRIG
from pyplc.utils.misc import TON,BLINK
from gear import Gear

class Factory(POU):
    HOUR = 18000000

    manual = POU.var(True)
    emergency = POU.var(False)
    heartbeat= POU.output(False)
    scanTime = POU.var(0)
    moto = POU.var(int(0),persistent=True)
    powered = POU.var(int(0),persistent=True)

    def __init__(self,id:str = None,parent:POU=None) -> None:
        super().__init__( id,parent )
        self.manual = True
        self.emergency = False
        self.powerfail = True
        self.powerack = False
        self.f_manual = TRIG(clk = lambda: self.manual)
        self.f_emergency = TRIG(clk = lambda: self.emergency )
        self.f_powerack = TON(clk = lambda: self.powerack,pt=2000)
        self.hour = TON(pt=Factory.HOUR)
        self.__sec= BLINK(enable=True)
        self.moto = 0
        self.powered = 0
        self.__last_call = POU.NOW_MS
        self.on_mode = [lambda *args: self.log('ручной режим = ',*args)]
        self.on_emergency = [lambda *args: self.log('аварийный режим = ',*args)]

    def __call__(self) :
        with self:
            self.scanTime = POU.NOW_MS - self.__last_call
            self.__last_call = POU.NOW_MS
            self.heartbeat = self.__sec( )
            if self.f_manual( ):
                for e in self.on_mode:
                    e( self.manual )
            if self.f_emergency( ):
                for e in self.on_emergency:
                    e( self.emergency )
                
            if self.powerfail:
                self.powerfail = False
                self.powered += 1
                
class ControlStation(POU):
    start = POU.input(False,hidden=True)
    stop  = POU.input(False,hidden=True)
    
    def __init__(self,*_,start:bool,stop:bool,gear: Gear,id: str = None, parent: POU = None,**kwargs) -> None:
        super().__init__(id, parent)
        self.start = start
        self.stop = stop
        self.gear = gear
        self.active = False
        
    def main(self):
        if self.start or self.stop:
            self.active   = True
        if self.active:
            self.gear.on = self.start
            self.gear.off= self.stop
            self.active  = self.start or self.stop
    
    def __call__(self):
        with self:
            self.main()

class ControlPost(ControlStation):
    manual = POU.input(False,hidden=True)
    def __init__(self, *_, manual:bool, start: bool, stop: bool, gear: Gear, id: str = None, parent: POU = None) -> None:
        super().__init__(*_, start=start, stop=stop, gear=gear, id=id, parent=parent)
        self.manual = manual
        
    def main(self):
        if self.manual:
            super().main( )
