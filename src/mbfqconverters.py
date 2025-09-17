from umodbus.tcp import TCP as ModbusTCPMaster
from _thread import start_new_thread,allocate_lock
from collections import namedtuple
from typing import cast

_lock = allocate_lock()
_queue = []
MAX_QUEUE_SIZE = 32

REQUEST = namedtuple('REQUEST', ['addr','func','reg','val'])

def __thread_mbus():
    _master = None
    faults = 0
    while True:
        _lock.acquire()
        if len(_queue)==0:
            _lock.release()
            continue
        req = cast(REQUEST,_queue.pop(0))
        _lock.release()
        try:
            if _master is None:
                faults = 0
                _master = ModbusTCPMaster(slave_ip='192.168.2.11')

            ret = None
            if(req.func==0): # write coil
                _master.write_single_coil(req.addr, req.reg, req.val)
            if(req.func==1): # read input discrete
                ret = _master.read_discrete_inputs(req.addr,req.reg,1)
            if(req.func==4): # write reg
                _master.write_single_register(req.addr,req.reg,req.val,signed=False)
            if(req.func==3): # read reg
                ret = _master.read_input_registers(req.addr,req.reg,1,signed=False)
            if ret is not None:
                req.val( req.func, req.reg,ret[0] )
        except Exception as e:
            faults +=1 
            if _master is not None and faults>2:
                del _master
                _master = None
            print(f'Exception in __thread_mbus: {e}')

start_new_thread(__thread_mbus, ())

class FQConv():
    FQ_REG = 768        # адрес регистра где частота лежит
    FAULT_REG = 0        # адрес регистра где fault
    ON_REG = 0          # адрес регистра включить можно

    def __init__(self, addr: int=1) -> None:
        self.addr = addr
        self.dflags = 0
        self.fq  = 0
        self.on  = False
        self.pause = 0      #пауза после запроса на чтение (чтоб результат успел прийти)
        self._fault= False
        self._lock = allocate_lock()
        self._timeout = 0
    
    @property
    def timeout(self)->int:
        self._lock.acquire()
        t= self._timeout
        self._lock.release()
        return t

    def fault(self)->bool:
        self._lock.acquire()
        v = self._fault
        self._lock.release()
        return v==False
    
    def set_fq(self,fq: int):
        self.fq = fq
        self.dflags |= 0x0001
        
    def set_on(self,on: bool):
        self.on = on
        self.dflags |= 0x0002
        
    def callback(self,fn:int, reg:int,val):
        self._lock.acquire()
        self._timeout = 10          #какое-то время не читать
        if reg==FQConv.FAULT_REG and fn==1:
            self._fault = (val==True)
        if fn==3:
            pass
        self._lock.release()
        
    def __call__(self):
        global _lock,_queue
        
        timeout = self.timeout
        
        if timeout==0 and self.pause==0:
            self.pause = 5
            _lock.acquire()
            if len(_queue)<MAX_QUEUE_SIZE:
                _queue.append( REQUEST(self.addr,1,FQConv.FAULT_REG,self.callback))
            _lock.release()
        elif timeout>0:
            self._lock.acquire()
            self._timeout -= 1
            self._lock.release()
        elif self.pause>0:
            self.pause -= 1
        
        if self.dflags == 0:
            return
        _lock.acquire()
        if self.dflags & 0x0001:
            _queue.append( REQUEST(self.addr,4,FQConv.FQ_REG,self.fq) )
        if self.dflags & 0x0002:
            _queue.append( REQUEST(self.addr,0,FQConv.ON_REG,self.on) )
        self.dflags = 0
        _lock.release()
