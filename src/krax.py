#Ниже идет Ваша программа
from pyplc.platform import plc, plc as hw
from collections import namedtuple
from sys import platform
from project import name as project_name,version_short as project_version
from gear import Gear as Motor, Feeder
from mbfqconverters import FQConv
from misc import Factory,ControlPost,ControlStation

print(f'\tStarting {project_name} {project_version}')

if platform == 'fake':
  HW = namedtuple('HW', ['TE1','TE2','H1','BURNER_SP','MOTOR_ON_1','MOTOR_ON_2','MOTOR_ON_3','MOTOR_ON_4','MOTOR_ON_5','MOTOR_ON_6','MOTOR_ON_7','MOTOR_ON_8','MOTOR_ON_10','BURNER_START','MOTOR_ON_11','MOTOR_ON_12','MOTOR_ON_13','FILTER_START','MOTOR_ON_14','MOTOR_ON_15','MOTOR_ON_16','MOTOR_ON_17','MOTOR_ON_18','VIBRATOR_ON_1','MOTOR_ON_20','MOTOR_ON_19','VIBRATOR_ON_2','AUGER_ON_22','AUGER_ON_24','AUGER_ON_25','COMPRESSOR_ON_28','AUGER_ON_26','FAN_ON_27','ROPE_1','BELT_1','MOTOR_ISON_2','ROPE_3','BELT_3','MOTOR_ISON_4','ROPE_5','BELT_5','MOTOR_ISON_6','ROPE_7','BELT_7','HLEVEL_1','LLEVEL_2','ROPE_8','BELT_8','CLOSED_1','ROPE_10','BELT_10','MOTOR_ISON_11','AUGER_ISON_13','AUGER_ROT_13','ROPE_14','BELT_14','MOTOR_ISON_15','ROPE_16','BELT_16','MOTOR_ISON_17','ROPE_18','BELT_18','HLEVEL_2','LLEVEL_2','ROPE_20','BELT_20','OPENED_2','ROPE_19','BELT_19','HLEVEL_3','LLEVEL_3','AUGER_ROT_22','HLEVEL_4','AUGER_ROT_24','AUGER_ISON_25','AUGER_ROT_25','HLEVEL_4','LLEVEL_4','COMPRESSOR_ISON_28','FAN_ISON','EMERGENCY','PU_START_1','PU_STOP_1','PU_START_2','PU_STOP_2','MAN_1','START_1','STOP_1','MAN_2','START_2','STOP_2','MAN_3','START_3','STOP_3','MAN_4','START_4','STOP_4','MAN_5','START_5','STOP_5','MAN_6','START_6','STOP_6','MAN_7','START_7','STOP_7','MAN_8','START_8','STOP_8','MAN_9','START_9','STOP_9','MAN_10','START_10','STOP_10','MAN_11','START_11','STOP_11','MAN_12','START_12','STOP_12','MAN_13','START_13','STOP_13','MAN_14','START_14','STOP_14','MAN_15','START_15','STOP_15','MAN_16','START_16','STOP_16','MAN_17','START_17','STOP_17','MAN_18','START_18','STOP_18','MAN_19','START_19','STOP_19','MAN_20','START_20','STOP_20','MAN_21','START_21','STOP_21','MAN_22','START_22','STOP_22','MAN_23','START_23','STOP_23','MAN_28','START_28','STOP_28','CASCADE_START_1','CASCADE_STOP_1'] )
  hw = HW()

factory_1 = Factory()
fq_1 = FQConv(addr=1)

compressor_28 = Motor(q=hw.COMPRESSOR_ON_28,fault=~hw.COMPRESSOR_ISON_28)
mcompressor_28 = ControlPost(start=hw.START_28,stop=hw.STOP_28,manual=hw.MAN_28,gear=compressor_28)

motor_1 = Feeder(q=hw.MOTOR_ON_1, fault=fq_1.fault, lock=hw.ROPE_1, rot=hw.BELT_1,fq=fq_1.set_fq)
motor_2 = Motor(q=hw.MOTOR_ON_2, lock=hw.EMERGENCY)
motor_4 = Motor(q=hw.MOTOR_ON_4, lock=hw.EMERGENCY)
motor_6 = Motor(q=hw.MOTOR_ON_6, lock=hw.EMERGENCY)

instances = (factory_1,mcompressor_28, compressor_28,motor_1,motor_2,motor_4,motor_6,fq_1)  #так быстее

if platform == 'linux':
  from imitation import IMotor,IRotation
  icompressor_28 = IMotor( q= hw.COMPRESSOR_ON_28, ison=hw.COMPRESSOR_ISON_28)
  ibelt_1 = IRotation( q = hw.MOTOR_ON_1, rot = hw.BELT_1 )
  imotor_2 = IMotor( q = hw.MOTOR_ON_2, ison = hw.MOTOR_ISON_2)
  imotor_4 = IMotor( q = hw.MOTOR_ON_4, ison = hw.MOTOR_ISON_4)
  imotor_6 = IMotor( q = hw.MOTOR_ON_6, ison = hw.MOTOR_ISON_6)
  instances += (icompressor_28,ibelt_1,imotor_2,imotor_4,imotor_6)
  
plc.run( instances=instances, ctx=globals() )
