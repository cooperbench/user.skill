> DEVELOPER

计算实时充电功率

> TOOL

tool_use Bash
```json
{
  "command": "ioreg -rn AppleSmartBattery | grep -E '\"(Voltage|Amperage|InstantAmperage|IsCharging|CurrentCapacity|MaxCapacity|ExternalConnected|AdapterDetails)\"' | head -30",
  "description": "Read battery voltage and amperage from IOKit"
}
```

> TOOL

tool_result Bash
```
"CurrentCapacity" = 3
      "Amperage" = 4836
      "ExternalConnected" = Yes
      "BatteryData" = {"Ra03"=113,"Ra10"=104,"CellWom"=(0,0),"RaTableRaw"=(<0063006a0070007100750067006c00630061005b00560065007f00b801060000>,<004c005a0058005e006700540057004c004c0052004a0057006c008a00cd0000>,<00600066006b007100820067007b006b006d006c0068007200a100d2012c0000>),"Qstart"=0,"AdapterPower"=,"TrueRemainingCapacity"=0,"DailyMinSoc"=0,"Ra04"=130,"CurrentSenseMonitorStatus"=0,"Ra11"=114,"CellVoltage"=(3545,3626,3626),"PackCurrentAccumulator"=445657,"PassedCharge"=18446744073709550538,"Flags"=83886080,"PresentDOD"=(44,45,44),"Ra05"=103,"Ra12"=161,"MiscStatus"=128,"FccComp1"=7858,"ChemID"=20784,"iMaxAndSocSmoothTable"=<0000000000000000000000000000000000000000000000000000000000000000>,"FccComp2"=7858,"PackCurrentAccumulatorCount"=80,"DOD0"=(9280,9344,9248),"Dod0AtQualifiedQmax"=0,"Ra06"=123,"ResScale"=0,"Ra13"=210,"FilteredCurrent"=0,"WeightedRa"=(107,88,111),"RSS"=0,"CellCurrentAccumulatorCount"=0,"Serial"="C0171041G1WFY2C9I","DataFlashWriteCount"=941,"DailyMaxSoc"=1,"DateOfFirstUse"=0,"Ra07"=107,"Ra14"=300,"MaxCapacity"=100,"ChemicalWeightedRa"=0,"Ra00"=96,"BatteryHealthMetric"=0,"DesignCapacity"=8400,"Ra08"=109,"BatteryState"=<0000000e200000000047e4400280020012>,"CellCurrentAccumulator"=(0,0),"AlgoChemID"=20784,"MfgData"=<323032302d31322d303600000000000000000000000000000000000000000000>,"ManufactureDate"=59584906605107,"ISS"=4931,"Ra01"=102,"Soc1Voltage"=0,"QmaxDisqualificationReason"=0,"ChargeAccum"=0,"SimRate"=0,"Qmax"=(8380,8400,8390),"PMUConfigured"=4448,"ITMiscStatus"=0,"StateOfCharge"=2,"Ra09"=108,"GaugeFlagRaw"=640,"CycleCount"=294,"Voltage"=10770,"SystemPower"=,"LifetimeData"={"Raw"=<0000000000483ff4000108f100000000060ae9c40080e467b24000000000000001d9004e1106084b33091fc6155be5271a8ce074eadce8ac01110006e0070031>,"UpdateTime"=1779960374,"ResistanceUpdatedDisabledCount"=0,"CycleCountLastQmax"=5,"TimeAtHighSoc"=<00000000340000000800000000000000000000000000000000000000000000002700000001000000000000000000000000000000000000008e0000009a00000002000000000000000000000000000000000000001f0100005a0600005500000000000000000000000000000000000000>,"TemperatureSamples"=450567,"TotalOperatingTime"=28160,"MaximumDischargeCurrent"=18446744073709544743,"MinimumPackVoltage"=8134,"MaximumPackVoltage"=13065,"MaximumChargeCurrent"=5467,"AverageTemperature"=273,"MinimumTemperature"=78,"RDISCnt"=0,"MaximumTemperature"=473},"Ra02"=107}
      "AdapterDetails" = {"IsWireless"=No,"AdapterID"=0,"AdapterVoltage"=20000,"FamilyCode"=18446744073172697098,"UsbHvcHvcIndex"=4,"Watts"=100,"UsbHvcMenu"=({"Index"=0,"MaxCurrent"=3000,"MaxVoltage"=5000},{"Index"=1,"MaxCurrent"=3000,"MaxVoltage"=9000},{"Index"=2,"MaxCurrent"=3000,"MaxVoltage"=12000},{"Index"=3,"MaxCurrent"=3000,"MaxVoltage"=15000},{"Index"=4,"MaxCurrent"=5000,"MaxVoltage"=20000}),"Current"=5000,"PMUConfiguration"=4460}
      "MaxCapacity" = 100
      "InstantAmperage" = 4836
      "IsCharging" = Yes
      "Voltage" = 10810
```

> AGENT

**实时充电功率 ≈ 52.3 W**

| 量 | 值 |
|---|---|
| 电池电压 | 10.810 V |
| 充电电流（InstantAmperage） | 4.836 A |
| **充电功率 = U × I** | **≈ 52.3 W** |

补充信息：
- 状态：正在充电（`IsCharging = Yes`），电量 3 %
- 适配器：20 V / 5 A，最大 100 W；当前协商档位 20 V/5 A
- 这 52 W 只是流入电池的功率；剩下的功率正在被系统本身消耗，所以适配器实际输出会更高。如果想看适配器侧的整机输入功率，可以读 `AdapterDetails.Watts` 协商上限（100 W）或者用 `system_profiler SPPowerDataType` 看 `Wattage (W)` 字段。