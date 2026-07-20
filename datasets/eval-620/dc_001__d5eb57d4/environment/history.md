> DEVELOPER

安装任何工具调查目前macos的实时充电功率

> TOOL

tool_use Bash
```json
{
  "command": "which ioreg && ioreg -rn AppleSmartBattery | grep -iE \"amperage|voltage|instant|ischarging|watts\" | head -30",
  "description": "Check battery info via ioreg"
}
```

> TOOL

tool_result Bash
```
/usr/sbin/ioreg
      "AppleRawAdapterDetails" = ({"IsWireless"=No,"AdapterID"=0,"AdapterVoltage"=20000,"FamilyCode"=18446744073172697098,"UsbHvcHvcIndex"=4,"Watts"=45,"UsbHvcMenu"=({"Index"=0,"MaxCurrent"=2960,"MaxVoltage"=5000},{"Index"=1,"MaxCurrent"=2980,"MaxVoltage"=9000},{"Index"=2,"MaxCurrent"=2990,"MaxVoltage"=12000},{"Index"=3,"MaxCurrent"=2990,"MaxVoltage"=15000},{"Index"=4,"MaxCurrent"=2240,"MaxVoltage"=20000}),"Current"=2240,"PMUConfiguration"=2240,"Description"="pd charger"})
      "CarrierMode" = {"CarrierModeLowVoltage"=3600,"CarrierModeHighVoltage"=4100,"CarrierModeStatus"=0}
      "Amperage" = 1926
      "AppleRawBatteryVoltage" = 11928
      "BootVoltage" = 0
      "PowerOutDetails" = ({"PowerState"=0,"VConnAccumulatorErrorCount"=0,"USBSleepPoolPowermW"=0,"AccumulatedPower"=2136924,"PortType"=0,"FilteredPower"=0,"AccumulatorCount"=46353,"VConnMaxCurrent"=330,"USBWakePoolPowermW"=1500,"PortIndex"=3,"Watts"=0,"ConfiguredVoltage"=5000,"VConnCurrent"=0,"VConnAccumulatedPower"=0,"AccumulatorErrorCount"=0,"NumLDCMCollisions"=0,"VConnPower"=0,"Current"=0,"ConfiguredCurrent"=1500,"PDPowermW"=0,"AdapterVoltage"=5214,"VConnAccumulatorCount"=46353})
      "BatteryData" = {"Ra03"=113,"Ra10"=104,"CellWom"=(0,0),"RaTableRaw"=(<0063006a0070007100750067006c00630061005b00560065007f00b801060000>,<004c005a0058005e006700540057004c004c0052004a0057006c008a00cd0000>,<00600066006b007100820067007b006b006d006c0068007200a100d2012c0000>),"Qstart"=0,"AdapterPower"=,"TrueRemainingCapacity"=0,"DailyMinSoc"=6,"Ra04"=130,"CurrentSenseMonitorStatus"=0,"Ra11"=114,"CellVoltage"=(3968,3964,3993),"PackCurrentAccumulator"=122961,"PassedCharge"=18446744073709550538,"Flags"=16777216,"PresentDOD"=(44,45,44),"Ra05"=103,"Ra12"=161,"MiscStatus"=128,"FccComp1"=7454,"ChemID"=20784,"iMaxAndSocSmoothTable"=<0000000000000000000000000000000000000000000000000000000000000000>,"FccComp2"=7454,"PackCurrentAccumulatorCount"=80980,"DOD0"=(9280,9344,9248),"Dod0AtQualifiedQmax"=0,"Ra06"=123,"ResScale"=0,"Ra13"=210,"FilteredCurrent"=0,"WeightedRa"=(107,88,111),"RSS"=0,"CellCurrentAccumulatorCount"=0,"Serial"="C0171041G1WFY2C9I","DataFlashWriteCount"=941,"DailyMaxSoc"=90,"DateOfFirstUse"=0,"Ra07"=107,"Ra14"=300,"MaxCapacity"=100,"ChemicalWeightedRa"=0,"Ra00"=96,"BatteryHealthMetric"=0,"DesignCapacity"=8400,"Ra08"=109,"BatteryState"=<0000000e200000000047e4400280020012>,"CellCurrentAccumulator"=(0,0),"AlgoChemID"=20784,"MfgData"=<323032302d31322d303600000000000000000000000000000000000000000000>,"ManufactureDate"=59584906605107,"ISS"=1724,"Ra01"=102,"Soc1Voltage"=0,"QmaxDisqualificationReason"=0,"ChargeAccum"=0,"SimRate"=0,"Qmax"=(8380,8400,8390),"PMUConfigured"=2184,"ITMiscStatus"=0,"StateOfCharge"=71,"Ra09"=108,"GaugeFlagRaw"=128,"CycleCount"=291,"Voltage"=11863,"SystemPower"=,"LifetimeData"={"Raw"=<0000000000483ff4000108f100000000060ae9c40080e467b24000000000000001d9004e1106084b33091fc6155be5271a8ce074eadce8ac01110006e0070031>,"UpdateTime"=1779835600,"ResistanceUpdatedDisabledCount"=0,"CycleCountLastQmax"=5,"TimeAtHighSoc"=<00000000340000000800000000000000000000000000000000000000000000002700000001000000000000000000000000000000000000008e0000009a00000002000000000000000000000000000000000000001f0100005a0600005500000000000000000000000000000000000000>,"TemperatureSamples"=450567,"TotalOperatingTime"=28160,"MaximumDischargeCurrent"=18446744073709544743,"MinimumPackVoltage"=8134,"MaximumPackVoltage"=13065,"MaximumChargeCurrent"=5467,"AverageTemperature"=273,"MinimumTemperature"=78,"RDISCnt"=0,"MaximumTemperature"=473},"Ra02"=107}
      "ChargerData" = {"ChargerStatus"=<06008ad8440498800000000000000000000000000000000000000000000000000000000e200000000047e4400280020012000000000000000000000000000000>,"VacVoltageLimit"=4275,"NotChargingReason"=0,"SlowChargingReason"=0,"ChargerResetCounter"=0,"ChargerID"=13,"TimeChargingThermallyLimited"=0,"ChargingVoltage"=4172,"ChargerInhibitReason"=0,"ChargingCurrent"=7078}
      "AdapterDetails" = {"IsWireless"=No,"AdapterID"=0,"AdapterVoltage"=20000,"FamilyCode"=18446744073172697098,"UsbHvcHvcIndex"=4,"Watts"=45,"UsbHvcMenu"=({"Index"=0,"MaxCurrent"=2960,"MaxVoltage"=5000},{"Index"=1,"MaxCurrent"=2980,"MaxVoltage"=9000},{"Index"=2,"MaxCurrent"=2990,"MaxVoltage"=12000},{"Index"=3,"MaxCurrent"=2990,"MaxVoltage"=15000},{"Index"=4,"MaxCurrent"=2240,"MaxVoltage"=20000}),"Current"=2240,"PMUConfiguration"=2240,"Description"="pd charger"}
      "PowerTelemetryData" = {"AccumulatedWallEnergyEstimate"=414398833,"SystemEnergyConsumed"=11895,"SystemPowerInAccumulatorCount"=54538,"AdapterEfficiencyLoss"=1181,"SystemLoad"=19852,"AccumulatedSystemLoad"=1362141123,"AccumulatedSystemEnergyConsumed"=1516725794712,"SystemCurrentIn"=2192,"WallEnergyEstimate"=13076,"SystemLoadAccumulatorCount"=74966,"AdapterEfficiencyLossAccumulatorCount"=52275,"SystemVoltageIn"=19533,"SystemPowerIn"=42825,"AccumulatedBatteryPower"=496353955,"PowerTelemetryErrorCount"=0,"AccumulatedAdapterEfficiencyLoss"=48948631,"BatteryPowerAccumulatorCount"=29489,"AccumulatedSystemPowerIn"=5460213012752,"BatteryPower"=22973,"AccumulatedBatteryDischarge"=18446744073160636074,"BatteryDischargeAccumulatorCount"=43420}
      "InstantAmperage" = 1926
      "IsCharging" = Yes
      "Voltage" = 11928
```

> AGENT

无需安装额外工具——`ioreg` 已经能给出实时充电功率。

**当前充电状态：**

- **适配器输入功率**：`SystemPowerIn` = **42.8 W**（SystemVoltageIn 19.533 V × SystemCurrentIn 2.192 A）
- **进入电池的功率**：`BatteryPower` = **22.97 W**（Voltage 11.928 V × Amperage 1.926 A）
- **适配器规格**：45 W PD 充电器（20 V / 2.24 A 档位）
- **适配器效率损耗**：约 1.18 W
- 电池电量 71%，正在充电

差额（42.8 W − 23 W ≈ 20 W）是系统当前的实时负载（SystemLoad ≈ 19.85 W）。

想持续监控可以跑：

```sh
while true; do
  ioreg -rn AppleSmartBattery | awk -F'[ =]+' '/"SystemPowerIn"/{p=$3} /"BatteryPower" /{b=$3} END{printf "Adapter: %.2f W  Battery: %.2f W\n", p/1000, b/1000}'
  sleep 2
done
```