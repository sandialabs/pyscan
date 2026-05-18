from ctypes import c_byte, c_int16, c_long, c_short, c_uint16, c_ushort

BNT_BNCTriggerModes = c_long
NT_BNCModeTrigger = c_long(0x0000)
NT_BNCModeLVOut = c_long(0xFFFF)

BNT_CurrentLimit = c_long
NT_CurrentLimit_100mA = c_long(0x00)
NT_CurrentLimit_250mA = c_long(0x01)
NT_CurrentLimit_500mA = c_long(0x02)

BNT_FeedbackSignalSelection = c_long
NT_FeedbackSignalDC = c_long(0x0000)
NT_FeedbackSignalAC = c_long(0xFFFF)

BNT_OutputLowPassFilter = c_long
NT_OutputFilter_10Hz = c_long(0x0)
NT_OutputFilter_100Hz = c_long(0x1)
NT_OutputFilter_5kHz = c_long(0x2)
NT_OutputFilter_None = c_long(0x3)

ChannelEnableModes = c_int16
ChannelNone = c_int16(0x00)
Channel1Only = c_int16(0x01)
Channel2Only = c_int16(0x02)
Channel3Only = c_int16(0x03)
Channel4Only = c_int16(0x04)
Channels1and2 = c_int16(0x05)
Channels3and4 = c_int16(0x06)

FF_IOModes = c_long
FF_ToggleOnPositiveEdge = c_long(0x01)
FF_SetPositionOnPositiveEdge = c_long(0x02)
FF_OutputHighAtSetPosition = c_long(0x04)
FF_OutputHighWhemMoving = c_long(0x08)

FF_Positions = c_short

FF_SignalModes = c_long
FF_InputButton = c_long(0x01)
FF_InputLogic = c_long(0x02)
FF_InputSwap = c_long(0x04)
FF_OutputLevel = c_long(0x10)
FF_OutputPulse = c_long(0x20)
FF_OutputSwap = c_long(0x40)

HubAnalogueModes = c_short
analogCh1 = c_short()
analogCh2 = c_short()
externaSignalSMA = c_short()

KIM_Channels = c_uint16
Channel1 = c_uint16(1)
Channel2 = c_uint16(2)
Channel3 = c_uint16(2)
Channel4 = c_uint16(4)

KIM_DirectionSense = c_int16
Dir_Disabled = c_int16(0x0)
Dir_Forward = c_int16(0x01)
Dir_Reverse = c_int16(0x02)

KIM_FBSignalMode = c_int16
FB_LimitSwitch = c_int16(0x01)
FB_Encoder = c_int16(0x02)

KIM_JogMode = c_uint16
JogContinuous = c_uint16(0x01)
JogStep = c_uint16(0x02)

KIM_JoysticModes = c_int16
JS_Velocity = c_int16(0x01)
JS_Jog = c_int16(0x02)
JS_GotoPosition = c_int16(0x03)

KIM_JoystickModes = c_short

KIM_LimitSwitchModes = c_int16
Ignore = c_int16(0x01)
SwitchMakes = c_int16(0x02)
SwitchBreaks = c_int16(0x03)
SwitchMakes_HomeOnly = c_int16(0x04)
SwitchBreaks_HomeOnly = c_int16(0x05)

KIM_Stages = c_ushort
Undefined_stage = c_ushort(0)
PIA_stage = c_ushort(1)
PDR_Stage = c_ushort(2)

KIM_TravelDirection = c_byte
Forward = c_byte(0x01)
Reverse = c_byte(0x02)

KIM_TrigModes = c_int16
Trig_Disabled = c_int16(0x00)
Trig_In_GPI = c_int16(0x01)
Trig_InRelativeMove = c_int16(0x02)
Trig_InAbsoluteMove = c_int16(0x03)
Trig_InResetCount = c_int16(0x04)
Trig_Out_GP0 = c_int16(0x0A)
Trig_Out_InMotion = c_int16(0x0B)
Trig_Out_AtMaxVelocity = c_int16(0x0C)
Trig_Out_PosStepFwd = c_int16(0x0D)
Trig_Out_PosStepRev = c_int16(0x0E)
Trig_Out_PosStepBoth = c_int16(0x0F)
Trig_Out_AtFwdLimit = c_int16(0x10)
Trig_Out_AtRevLimit = c_int16(0x11)
Trig_Out_AtEitherLimit = c_int16(0x12)

KIM_TrigPolarities = c_int16
Trig_High = c_int16(0x01)
Trig_Low = c_int16(0x02)

KLDTriggerMode = c_short
disabled = c_short()
input = c_short()
output = c_short()
laserOn = c_short()
interlockEnabled = c_short()
setPointChange = c_short()
highStability = c_short()
lowStability = c_short()

KLD_RAMPUP = c_int16
KLD_RampUpImmediate = c_int16(0)
KLD_RampUpRamped = c_int16(1)

KLD_TrigPolarity = c_ushort
KLD_TrigPol_High = c_ushort(0x01)
KLD_TrigPol_Low = c_ushort(0x02)

KLD_TriggerMode = c_ushort
KLD_Disabled = c_ushort(0)
KLD_Output = c_ushort(0x0a)
KLD_LaserOn = c_ushort(0x0b)
KLD_InterlockEnabled = c_ushort(0x0c)
KLD_SetPointChange = c_ushort(0x0d)
KLD_HighStability = c_ushort(0x0e)
KLD_LowStability = c_ushort(0x0f)
KLD_Input = c_ushort(1)

KLS_OpMode = c_ushort
KLS_ConstantPower = c_ushort(0)
KLS_ConstantCurrent = c_ushort(1)

KLS_Polarity = c_short

KLS_TrigPolarity = c_ushort
KLS_TrigPol_High = c_ushort(0x01)
KLS_TrigPol_Low = c_ushort(0x02)

KLS_TriggerMode = c_short
KLS_Disabled = c_short(0)
KLS_Output = c_short(0x0a)
KLS_LaserOn = c_short(0x0b)
KLS_InterlockEnabled = c_short(0x0c)
KLS_SetPointChange = c_short(0x0d)
KLS_HighStability = c_short(0x0e)
KLS_LowStability = c_short(0x0f)
KLS_Input = c_short(1)

KMOT_TriggerPortMode = c_short
triggerDisabled = c_short()
inputGeneralPurposeLogic = c_short()
inputMoveRelative = c_short()
inputMoveAbsolute = c_short()
inputHomeAction = c_short()
inputStop = c_short()
outputGeneralPurpose = c_short()
ouptputWhileMoving = c_short()
outputAtMaxVelocity = c_short()
outputPredefinedPositionSteps = c_short()
outputTBDMode = c_short()

KMOT_TriggerPortPolarity = c_short
outputHigh = c_short()
ouptutLow = c_short()

KMOT_WheelDirectionSense = c_short

KMOT_WheelMode = c_short
constantVelocity = c_short()
jog = c_short()
moveAbsolute = c_short()

KNA_Channels = c_long
KNA_ChannelUndefined = c_long(0x00)
KNA_Channel1 = c_long(0x01)
KNA_Channel2 = c_long(0x02)

KNA_FeedbackModeTypes = c_short
PZ_ControlModeUndefined = c_short(0)
PZ_OpenLoop = c_short(1)
PZ_CloseLoop = c_short(2)
PZ_OpenLoopSmooth = c_short(3)
PZ_CloseLoopSmooth = c_short(4)

KNA_FeedbackSource = c_short
tiaValue = c_short()
bnc1VRange = c_short()
bnc2VRange = c_short()
bnc5VRange = c_short()
bnc10VRange = c_short()

KNA_HighOutputVoltageRoute = c_short
default = c_short()
extinSMA = c_short()
extoutSMA = c_short()
enableInputboost = c_short()

KNA_HighVoltageRange = c_short
default75V = c_short()
high150V = c_short()

KNA_LowOutputVoltageRoute = c_short
outputIO1connector = c_short()

KNA_LowVoltageRange = c_short
v10V = c_short()

KNA_TIARange = c_short
i5nA = c_short()
i16nA = c_short()
i50nA = c_short()
i166nA = c_short()
i500nA = c_short()
i1p6uA = c_short()
i5uA = c_short()
i16p6uA = c_short()
i50uA = c_short()
i166uA = c_short()
i500uA = c_short()
i1p66mA = c_short()
i5mA = c_short()

KNA_TriggerPolarity = c_short

KNA_TriggerPortMode = c_short
disabled = c_short()
inputLatching = c_short()
inputTracking = c_short()
inputHome = c_short()
output = c_short()
outputTracking = c_short()

KNA_TriggerPortPolarity = c_short
outputHigh = c_short()
OutputLow = c_short()

KNA_WheelAdjustRate = c_short
lowVoltageChangeRate = c_short()
mediumVoltageChangeRate = c_short()
highVoltageChangeRate = c_short()

KPC_HubAnalogueModes = c_short
inputDisabled = c_short()
allHubBays = c_short()
adjacentHubBays = c_short()
fromExternalSMA = c_short()

KPC_IOSettings = c_short

KPC_MonitorOutputMode = c_short

KPC_TriggerPortMode = c_short
disabled = c_short()
inputGeneralPurpose = c_short()
inputRelative = c_short()
inputAbsolute = c_short()
outputGeneralPurpose = c_short()

KPC_TriggerPortPolarity = c_short
highWhenSet = c_short()
lowWhenSet = c_short()

KPZ_TriggerPortMode = c_short
ddisabled = c_short()
inputGeneralPurpose = c_short()
inputRelative = c_short()
inputAbsolute = c_short()
outputGeneralPurpose = c_short()

KPZ_TriggerPortPolarity = c_short
highWhenSet = c_short()
lowWhenSet = c_short()

KPZ_WheelChangeRate = c_int16
KPZ_WM_High = c_int16(0x01)
KPZ_WM_Medium = c_int16(0x02)
KPZ_WM_Low = c_int16(0x03)

KPZ_WheelDirectionSense = c_int16
KPZ_WM_Positive = c_int16(0x01)
KPZ_WM_Negative = c_int16(0x02)

KPZ_WheelMode = c_int16
KPZ_WM_MoveAtVoltage = c_int16(0x01)
KPZ_WM_JogVoltage = c_int16(0x02)
KPZ_WM_SetVoltage = c_int16(0x03)

KSC_TriggerPolarity = c_short

KSC_TriggerPortMode = c_int16
KSC_TrigDisabled = c_int16(0x00)
KSC_TrigIn_GPI = c_int16(0x01)
KSC_TrigOut_GPO = c_int16(0x0A)

KSC_TriggerPortPolarity = c_int16
KSC_TrigPolarityHigh = c_int16(0x01)
KSC_TrigPolarityLow = c_int16(0x02)

KSG_TriggerPortMode = c_int16
KSG_TrigDisabled = c_int16(0x00)
KSG_TrigIn_GPI = c_int16(0x01)
KSG_TrigOut_GPO = c_int16(0x0A)
KSG_TrigOut_LessThanLowerLimit = c_int16(0x0B)
KSG_TrigOut_MoreThanLowerLimit = c_int16(0x0C)
KSG_TrigOut_LessThanUpperLimit = c_int16(0x0D)
KSG_TrigOut_MoreThanUpperLimit = c_int16(0x0E)
KSG_TrigOut_BetweenLimits = c_int16(0x0F)
KSG_TrigOut_OutsideLimits = c_int16(0x10)

KSG_TriggerPortPolarity = c_int16
KSG_TrigPolarityHigh = c_int16(0x01)
KSG_TrigPolarityLow = c_int16(0x02)

KST_Stages = c_short
ZST6 = c_short()
ZST13 = c_short()
ZST25 = c_short()
ZST206 = c_short()
ZST213 = c_short()
ZST225 = c_short()
ZFS206 = c_short()
ZFS213 = c_short()
ZFS225 = c_short()
NR360 = c_short()
PLS_X = c_short()
PLS_XHiRes = c_short()
FW103 = c_short()

LD_DisplayUnits = c_ushort
LD_ILim = c_ushort(0x01)
LD_ILD = c_ushort(0x02)
LD_IPD = c_ushort(0x03)
LD_PLD = c_ushort(0x04)

LD_InputSourceFlags = c_ushort
LD_SoftwareOnly = c_ushort(0)
LD_SoftwareOnly = c_ushort(0x01)
LD_Potentiometer = c_ushort(0x01)
LD_ExternalSignal = c_ushort(0x02)
LD_Potentiometer = c_ushort(0x04)
LD_WheelAndSoftware = c_ushort(0x04)

LD_POLARITY = c_int16
LD_CathodeGrounded = c_int16(1)
LD_AnodeGrounded = c_int16(2)

LD_TIA_RANGES = c_int16
LD_TIA_10uA = c_int16(1)
LD_TIA_1_10uA = c_int16(1)
LD_TIA_100uA = c_int16(2)
LD_TIA_2_100uA = c_int16(2)
LD_TIA_1mA = c_int16(4)
LD_TIA_3_1mA = c_int16(4)
LD_TIA_10mA = c_int16(8)
LD_TIA_4_10mA = c_int16(8)

LS_DisplayUnits = c_ushort
LS_mAmps = c_ushort(0x01)
LS_mWatts = c_ushort(0x02)
LS_mDb = c_ushort(0x03)

LS_InputSourceFlags = c_ushort
LS_SoftwareOnly = c_ushort(0)
LS_ExternalSignal = c_ushort(0x01)
LS_Potentiometer = c_ushort(0x04)
LS_WheelAndSoftware = c_ushort(0x04)

MOD_AuxIOPortMode = c_short
SW = c_short()
ENC = c_short()

MOD_IOPortMode = c_short
digitalInput = c_short()
digitalOutput = c_short()
analogInput = c_short()
analogOutput = c_short()

MOD_IOPortSource = c_short
software = c_short()
motorCh1 = c_short()
motorCh2 = c_short()
motorCh3 = c_short()

MOD_Monitor_Variable = c_short
positionError = c_short()
position = c_short()
motorPhaseACurrent = c_short()
motorPhaseBCurrent = c_short()
motorPhaseCCurrent = c_short()
motorCurrent = c_short()

MOT_ButtonModes = c_short
joggingMode = c_short()
presentMode = c_short()

MOT_CurrentLoopPhases = c_long
phaseA = c_long()
phaseB = c_long()
phaseAandB = c_long()

MOT_DirectionSense = c_short
normal = c_short()
backwards = c_short()

MOT_HomeLimitSwitchDirection = c_short
undefined = c_short()
forward = c_short()
reverse = c_short()

MOT_JogModes = c_short
undefined = c_short()
continuousJog = c_short()
jogOneStep = c_short()

MOT_LimitSwitchModes = c_short
undefined = c_short()
ignore = c_short()
makesOnContact = c_short()
breaksOnContact = c_short()
makesOnContactWhenHoming = c_short()
breaksOnContactWhenHoming = c_short()
reserved = c_short()
ignoreSwapped = c_short()
makesOnContactSwapped = c_short()
breaksOnContactSwapped = c_short()
makesOnContactWhenHomingSwapped = c_short()
breaksOnContactWhenHomingSwapped = c_short()

MOT_LimitSwitchSWModes = c_short
undefined = c_short()
ignore = c_short()
stopImmediately = c_short()
stopProfiled = c_short()
ignoreRotational = c_short()
stopImmediatelyRotational = c_short()
stopProfiledRotational = c_short()

MOT_LimitsSoftwareApproachPolicy = c_short
disallowIllegalMoves = c_short()
allowPartialMoves = c_short()
allowAllMoves = c_short()

MOT_MotorTypes = c_long
notAMotor = c_long()
dcMotor = c_long()
stepperMotor = c_long()
brushlessMotor = c_long()
customMotor = c_long()

MOT_MovementDirections = c_short
quickest = c_short()
forwards = c_short()
reverse = c_short()

MOT_MovementModes = c_short
linearRange = c_short()
rotationalUnlimited = c_short()
rotationalWrapping = c_short()

MOT_PID_LoopMode = c_long
disabled = c_long()
openLoop = c_long()
closedLoop = c_long()

MOT_RasterScanMoveCmd = c_short
start = c_short()
pause = c_short()
stopDisable = c_short()

MOT_RasterScanMovePattern = c_long
flyback = c_long()
fowardReverse = c_long()

MOT_RasterScanMoveTriggerMode = c_long
software = c_long()
xStep = c_long()
yStep = c_long()
xyScan = c_long()
onOff = c_long()

MOT_StopModes = c_short
undefined = c_short()
immediate = c_short()
profiled = c_short()

MOT_TravelDirection = c_short
undefined = c_short()
fowards = c_short()
reverse = c_short()

MOT_TravelModes = c_short
undefined = c_short()
linear = c_short()
rotational = c_short()

MOT_TriggerInputConfigModes = c_short
triggerInDisabled = c_short()
triggerInGeneralPurpose = c_short()
triggerInRelative = c_short()
triggerInAbsolute = c_short()
triggerInHome = c_short()
triggerInStop = c_short()

MOT_TriggerInputSource = c_short
software = c_short()
port1 = c_short()
port2 = c_short()
port3 = c_short()

MOT_TriggerOutputConfigModes = c_short
triggerOutDisabled = c_short()
triggerOutGeneralPurpose = c_short()
triggerOutInMotion = c_short()
triggerOutAtMaxVelocity = c_short()
triggerOutAtPositionStepForward = c_short()
triggerOutAtPositionStepReverse = c_short()
triggerOutAtPositionBoth = c_short()
triggerOutAtForwardLimit = c_short()
triggerOutAtBackwardsLimit = c_short()
triggerOutAtLimit = c_short()

MOT_TriggerPolarity = c_short
high = c_short()
low = c_short()

MOT_TriggerState = c_short
arm = c_short()
cancel = c_short()

MOT_VelocityProfileModes = c_long
trapezoidal = c_long()
sCurve = c_long()

MPC_IOModes = c_long
MPC_ToggleOnPositiveEdge = c_long(0x01)
MPC_SetPositionOnPositiveEdge = c_long(0x02)
MPC_OutputHighAtSetPosition = c_long(0x04)
MPC_OutputHighWhemMoving = c_long(0x08)

MPC_SignalModes = c_long
MPC_InputButton = c_long(0x01)
MPC_InputLogic = c_long(0x02)
MPC_InputSwap = c_long(0x04)
MPC_OutputLevel = c_long(0x10)
MPC_OutputPulse = c_long(0x20)
MPC_OutputSwap = c_long(0x40)

NT_CircleAdjustment = c_long
linear = c_long()
log = c_long()
square = c_long()
cube = c_long()

NT_CircleDiameterMode = c_long
fixed = c_long()
absPower = c_long()
LUT = c_long()

NT_ControlMode = c_long
undefined = c_long()
openLoop = c_long()
closedLoop = c_long()
openLoopSmoothed = c_long()
closedLoopSmoothed = c_long()

NT_FeedbackSource = c_long
undefined = c_long()
tia = c_long()
bnc1V = c_long()
bnc2V = c_long()
bnc5V = c_long()
bnc10V = c_long()

NT_LowPassFrequency = c_long
disabled = c_long()
f1Hz = c_long()
f3Hz = c_long()
f10Hz = c_long()
f30Hz = c_long()
f100Hz = c_long()

NT_Mode = c_long
undefined = c_long()
piezo = c_long()
latched = c_long()
tracking = c_long()
horizontalTracking = c_long()
verticalTracking = c_long()

NT_OddOrEven = c_short
allTIARanges = c_short()
onlyOdd = c_short()
onlyEven = c_short()

NT_OutputVoltageRoute = c_long
smaOnly = c_long()
smaAndHub = c_long()

NT_SignalState = c_short
NT_BadSignal = c_short(0x00)
NT_GoodSignal = c_short(0x01)


NT_TIARange = c_long
i5nA = c_long()
i16nA = c_long()
i50nA = c_long()
i166nA = c_long()
i500nA = c_long()
i1p6uA = c_long()
i5uA = c_long()
i16p6uA = c_long()
i50uA = c_long()
i166uA = c_long()
i500uA = c_long()
i1p66mA = c_long()
i5mA = c_long()

NT_TIARangeMode = c_short
automaticCurrent = c_short()
manualCurrent = c_short()
automaticSupplied = c_short()

NT_UnderOrOver = c_long
inRange = c_long()
underRange = c_long()
overRange = c_long()

NT_VoltageRange = c_long
v5V = c_long()
v10V = c_long()

PCC_DerivFilterState = c_long

PCC_DisplayIntensity = c_long

PCC_FeedbackPolarity = c_long

PCC_IOFeedbackSourceDefinition = c_long

PCC_IOOutputBandwidth = c_long

PCC_IOOutputMode = c_long

PCC_NotchFilterChannel = c_long

PCC_NotchFilterState = c_long

PDXC2_TriggerModes = c_uint16
Manual = c_uint16(0x00)
AnalogRising = c_uint16(0x01)
AnalogFalling = c_uint16(0x02)
FixedStepRising = c_uint16(0x03)
FixedStepFalling = c_uint16(0x04)
TwoPositionRising = c_uint16(0x05)
TwoPositionFalling = c_uint16(0x06)

POL_PaddleBits = c_ushort
PattleBit1 = c_ushort(0x01)
PattleBit1 = c_ushort(0x02)
PattleBit1 = c_ushort(0x04)
AllPaddlees = c_ushort(0x07)

POL_Paddles = c_short

POL_PattleBits = c_short

PPC_DerivFilterState = c_short
DerivFilterOn = c_short(0x01)
DerivFilterOff = c_short(0x02)
DerivFilterOn = c_short(0x1)
DerivFilterOff = c_short(0x2)

PPC_DisplayIntensity = c_short
Bright = c_short(0x01)
Dim = c_short(0x02)
Off = c_short(0x03)

PPC_FeedbackPolarity = c_long
Inverted = c_long(-1)
NonInverted = c_long(0)

PPC_IOControlMode = c_short
SWOnly = c_short(0x00)
ExtBNC = c_short(0x01)
Joystick = c_short(0x02)
JoystickBnc = c_short(0x03)

PPC_IOFeedbackSourceDefinition = c_short
StrainGauge = c_short(0x01)
Capacitive = c_short(0x02)
Optical = c_short(0x03)

PPC_IOOutputBandwidth = c_short
OP_Unfiltered = c_short(0x01)
OP_200Hz = c_short(0x02)

PPC_IOOutputMode = c_short
HV = c_short(0x01)
PosRaw = c_short(0x02)
PosCorrected = c_short(0x03)

PPC_NotchFilterChannel = c_short
NotchFilter1 = c_short(0x01)
NotchFilter2 = c_short(0x02)
NotchFilterBoth = c_short(0x03)

PPC_NotchFilterState = c_short
NotchFilterOn = c_short(0x01)
NotchFilterOff = c_short(0x02)

PZ_AmpOutParameters = c_short

PZ_ControlModeTypes = c_short
undefined = c_short()
openLoop = c_short()
closedLoop = c_short()
openLoopSmoothed = c_short()
closedLoopSmoothed = c_short()

PZ_InputSourceFlags = c_short
softwareOnly = c_short()
externalSignal = c_short()
potentiometer = c_short()
all = c_short()

PZ_JogModes = c_long

PZ_OutputLUTModes = c_short
continuous = c_short()
fixed = c_short()
outputTrigEnabled = c_short()
inputTrigEnabled = c_short()
outpTrigSenseHigh = c_short()
inputTrigSenseHigh = c_short()
outputGated = c_short()
outputTrigRepeated = c_short()

QD_FilterEnable = c_long
QD_Undefined = c_long(0)
QD_Enabled = c_long(1)
QD_Disabled = c_long(2)

QD_KPA_TrigModes = c_long
QD_Trig_Disabled = c_long(0x00)
QD_TrigIn_GPI = c_long(0x01)
QD_TrigIn_LoopOpenClose = c_long(0x02)
KD_TrigOut_GPO = c_long(0x0A)
KD_TrigOut_Sum = c_long(0x0B)
KD_TrigOut_Diff = c_long(0x0C)
KD_TrigOut_SumDiff = c_long(0x0D)

QD_KPA_TrigPolarities = c_long
GD_Trig_High = c_long(0x01)
GD_Trig_Low = c_long(0x02)

QD_LowVoltageRoute = c_short
QD_RouteUndefined = c_short(0)
QD_SMAOnly = c_short(1)
QD_HubAndSMA = c_short(2)

QD_OpenLoopHoldValues = c_short
QD_HoldOnZero = c_short(1)
QD_HoldOnLastValue = c_short(2)

QD_OperatingMode = c_short
QD_ModeUndefined = c_short(0)
QD_Monitor = c_short(1)
QD_OpenLoop = c_short(2)
QD_ClosedLoop = c_short(3)
QD_AutoOpenClosedLoop = c_short(4)

SC_OperatingModes = c_byte
SC_Manual = c_byte(0x01)
SC_Single = c_byte(0x02)
SC_Auto = c_byte(0x03)
SC_Triggered = c_byte(0x04)

SC_OperatingStates = c_byte
SC_Active = c_byte(0x01)
SC_Inactive = c_byte(0x02)

SC_SolenoidStates = c_byte
SC_SolenoidOpen = c_byte(0x01)
SC_SolenoidClosed = c_byte(0x02)

TC_DisplayModes = c_ushort
TC_ActualTemperature = c_ushort(0x00)
TC_TargetTemperature = c_ushort(0x01)
TC_TempDifference = c_ushort(0x02)
TC_Current = c_ushort(0x03)

TC_SensorTypes = c_ushort
TC_Transducer = c_ushort(0x00)
TC_TH20kOhm = c_ushort(0x01)
TC_TH200kOhm = c_ushort(0x02)

TIM_ButtonsMode = c_uint16
Jog = c_uint16(0x01)
Position = c_uint16(0x02)

TIM_Channels = c_ushort
Channel1 = 1
Channel2 = 2
Channel3 = 3
Channel4 = 4

TIM_Direction = c_byte
Forward = c_byte(0x01)
Reverse = c_byte(0x02)

TIM_JogMode = c_uint16
JogContinuous = 0x01
JogStep = 0x02

TSG_DisplayModes = c_long

TSG_Display_Modes = c_short
TSG_Undefined = c_short(0)
TSG_Position = c_short(1)
TSG_Voltage = c_short(2)
TSG_Force = c_short(3)

TSG_Hub_Analogue_Modes = c_short
TSG_HubChannel1 = c_short(1)
TSG_HubChannel2 = c_short(2)

TST_Stages = c_short
ZST6 = c_short(0x20)
ZST13 = c_short(0x21)
ZST25 = c_short(0x22)
ZST206 = c_short(0x30)
ZST213 = c_short(0x31)
ZST225 = c_short(0x32)
ZFS206 = c_short(0x40)
ZFS213 = c_short(0x41)
ZFS225 = c_short(0x42)
TBD1 = c_short(0x60)
TBD2 = c_short(0x61)
TBD3 = c_short(0x62)
TBD4 = c_short(0x63)
NR360 = c_short(0x70)
MVS025 = c_short(0x71)
PLS_X25MM = c_short(0x72)
PLS_X25MM_HiRes = c_short(0x73)
FW103 = c_short(0x75)
NEWZFS06 = c_short(10006)
NEWZFS13 = c_short(10013)
NEWZFS25 = c_short(10025)
NEWZST06 = c_short(11006)
NEWZST13 = c_short(11013)
NEWZST25 = c_short(12025)
