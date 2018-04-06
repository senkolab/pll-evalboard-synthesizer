<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="8.7.1">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="2" name="Route2" color="1" fill="3" visible="no" active="no"/>
<layer number="3" name="Route3" color="4" fill="3" visible="no" active="no"/>
<layer number="4" name="Route4" color="1" fill="4" visible="no" active="no"/>
<layer number="5" name="Route5" color="4" fill="4" visible="no" active="no"/>
<layer number="6" name="Route6" color="1" fill="8" visible="no" active="no"/>
<layer number="7" name="Route7" color="4" fill="8" visible="no" active="no"/>
<layer number="8" name="Route8" color="1" fill="2" visible="no" active="no"/>
<layer number="9" name="Route9" color="4" fill="2" visible="no" active="no"/>
<layer number="10" name="Route10" color="1" fill="7" visible="no" active="no"/>
<layer number="11" name="Route11" color="4" fill="7" visible="no" active="no"/>
<layer number="12" name="Route12" color="1" fill="5" visible="no" active="no"/>
<layer number="13" name="Route13" color="4" fill="5" visible="no" active="no"/>
<layer number="14" name="Route14" color="1" fill="6" visible="no" active="no"/>
<layer number="15" name="Route15" color="4" fill="6" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="24" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="88" name="SimResults" color="9" fill="1" visible="yes" active="yes"/>
<layer number="89" name="SimProbes" color="9" fill="1" visible="yes" active="yes"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
<layer number="100" name="Tolerances" color="7" fill="1" visible="no" active="yes"/>
<layer number="101" name="Power" color="7" fill="1" visible="no" active="yes"/>
<layer number="102" name="SIZE" color="7" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="lib">
<packages>
<package name="SMA-END">
<smd name="SIGNAL" x="0" y="1.8542" dx="2.3622" dy="1.4986" layer="1" rot="R90"/>
<wire x1="-6.35" y1="0" x2="6.35" y2="0" width="0.127" layer="51"/>
<smd name="P$2" x="-4.2545" y="3.039109375" dx="1.6002" dy="4.9022" layer="16" rot="R180"/>
<smd name="P$3" x="4.2545" y="3.039109375" dx="1.6002" dy="4.9022" layer="16" rot="R180"/>
<smd name="P$4" x="4.2545" y="3.039109375" dx="1.6002" dy="4.9022" layer="1" rot="R180"/>
<smd name="P$5" x="-4.2545" y="3.039109375" dx="1.6002" dy="4.9022" layer="1" rot="R180"/>
</package>
<package name="R1206">
<text x="-2.6" y="1.05" size="1.27" layer="21" font="vector" ratio="12">&gt;NAME</text>
<text x="-2.25" y="-0.6" size="1.27" layer="21" font="vector" ratio="12">&gt;NAME</text>
<wire x1="-2.95" y1="1.05" x2="-2.95" y2="-1.05" width="0.127" layer="21"/>
<wire x1="-2.95" y1="-1.05" x2="3" y2="-1.05" width="0.127" layer="21"/>
<wire x1="3" y1="-1.05" x2="3" y2="1.05" width="0.127" layer="21"/>
<wire x1="3" y1="1.05" x2="-2.95" y2="1.05" width="0.127" layer="21"/>
<wire x1="-1.524" y1="-1.27" x2="-1.524" y2="1.27" width="0" layer="21"/>
<wire x1="-1.524" y1="1.27" x2="1.524" y2="1.27" width="0" layer="21"/>
<wire x1="1.524" y1="1.27" x2="1.524" y2="-1.27" width="0" layer="21"/>
<wire x1="1.524" y1="-1.27" x2="-1.524" y2="-1.27" width="0" layer="21"/>
<smd name="P$1" x="-1.8542" y="0.0254" dx="1.2954" dy="1.8034" layer="1"/>
<smd name="P$2" x="1.8796" y="0" dx="1.2954" dy="1.8034" layer="1"/>
</package>
</packages>
<symbols>
<symbol name="SMA-END">
<pin name="SIGNAL" x="0" y="0" length="point"/>
<pin name="P$2" x="-5.08" y="-5.08" visible="off" length="point"/>
<pin name="P$3" x="-2.54" y="-5.08" visible="off" length="point"/>
<pin name="P$4" x="2.54" y="-5.08" visible="off" length="point"/>
<pin name="P$5" x="5.08" y="-5.08" visible="off" length="point"/>
<text x="0" y="2.54" size="1.27" layer="94">&gt;NAME</text>
<circle x="0" y="0" radius="3.5921" width="0.254" layer="94"/>
<circle x="0" y="0" radius="1.04726875" width="0.254" layer="94"/>
<wire x1="-2.54" y1="-2.54" x2="-5.08" y2="-2.54" width="0.254" layer="94"/>
<wire x1="-5.08" y1="-2.54" x2="-5.08" y2="-5.08" width="0.254" layer="94"/>
<wire x1="-2.54" y1="-2.54" x2="-2.54" y2="-5.08" width="0.254" layer="94"/>
<wire x1="2.54" y1="-2.54" x2="2.54" y2="-5.08" width="0.254" layer="94"/>
<wire x1="2.54" y1="-2.54" x2="5.08" y2="-2.54" width="0.254" layer="94"/>
<wire x1="5.08" y1="-2.54" x2="5.08" y2="-5.08" width="0.254" layer="94"/>
</symbol>
<symbol name="GROUND">
<wire x1="5.08" y1="2.54" x2="5.08" y2="-2.54" width="0.254" layer="94"/>
<wire x1="6.604" y1="1.524" x2="6.604" y2="-1.524" width="0.254" layer="94"/>
<wire x1="8.128" y1="0.508" x2="8.128" y2="-0.762" width="0.254" layer="94"/>
<pin name="GROUND" x="0" y="0" visible="off" length="middle" direction="sup"/>
</symbol>
<symbol name="RESISTOR">
<pin name="A" x="0" y="0" visible="off" length="point"/>
<pin name="B" x="17.78" y="0" visible="off" length="point"/>
<wire x1="0" y1="0" x2="2.54" y2="0" width="0.254" layer="94"/>
<wire x1="2.54" y1="0" x2="5.08" y2="2.54" width="0.254" layer="94"/>
<wire x1="5.08" y1="2.54" x2="7.62" y2="-2.54" width="0.254" layer="94"/>
<wire x1="7.62" y1="-2.54" x2="10.16" y2="2.54" width="0.254" layer="94"/>
<wire x1="10.16" y1="2.54" x2="12.7" y2="-2.54" width="0.254" layer="94"/>
<wire x1="12.7" y1="-2.54" x2="15.24" y2="0" width="0.254" layer="94"/>
<wire x1="15.24" y1="0" x2="17.78" y2="0" width="0.254" layer="94"/>
<text x="7.62" y="3.81" size="1.778" layer="95" ratio="12" rot="R180">&gt;NAME</text>
<text x="19.05" y="3.81" size="1.778" layer="96" ratio="12" rot="R180">&gt;VALUE</text>
<text x="5.08" y="-2.54" size="1.778" layer="96" ratio="12" rot="R180">&gt;TOLERANCE</text>
<text x="20.32" y="-2.54" size="1.778" layer="96" ratio="12" rot="R180">&gt;POWER</text>
<text x="17.78" y="-2.54" size="1.778" layer="102" rot="R180">&gt;SIZE</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="SMA-END" prefix="J">
<gates>
<gate name="G$1" symbol="SMA-END" x="0" y="0"/>
</gates>
<devices>
<device name="" package="SMA-END">
<connects>
<connect gate="G$1" pin="P$2" pad="P$5"/>
<connect gate="G$1" pin="P$3" pad="P$4"/>
<connect gate="G$1" pin="P$4" pad="P$3"/>
<connect gate="G$1" pin="P$5" pad="P$2"/>
<connect gate="G$1" pin="SIGNAL" pad="SIGNAL"/>
</connects>
<technologies>
<technology name="">
<attribute name="PARTNUM" value="ACX1911-ND" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="GROUND">
<gates>
<gate name="G$1" symbol="GROUND" x="2.54" y="0"/>
</gates>
<devices>
<device name="">
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="RESISTOR" prefix="R" uservalue="yes">
<gates>
<gate name="&gt;NAME" symbol="RESISTOR" x="0" y="0"/>
</gates>
<devices>
<device name="-R1206" package="R1206">
<connects>
<connect gate="&gt;NAME" pin="A" pad="P$1"/>
<connect gate="&gt;NAME" pin="B" pad="P$2"/>
</connects>
<technologies>
<technology name="">
<attribute name="POWER" value="1W" constant="no"/>
<attribute name="SIZE" value="1206" constant="no"/>
<attribute name="TOLERANCE" value="1%" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="J1" library="lib" deviceset="SMA-END" device=""/>
<part name="J2" library="lib" deviceset="SMA-END" device=""/>
<part name="J3" library="lib" deviceset="SMA-END" device=""/>
<part name="J4" library="lib" deviceset="SMA-END" device=""/>
<part name="U$1" library="lib" deviceset="GROUND" device=""/>
<part name="U$2" library="lib" deviceset="GROUND" device=""/>
<part name="U$3" library="lib" deviceset="GROUND" device=""/>
<part name="U$4" library="lib" deviceset="GROUND" device=""/>
<part name="R1" library="lib" deviceset="RESISTOR" device="-R1206" value="50 Ohm"/>
<part name="R2" library="lib" deviceset="RESISTOR" device="-R1206" value="50 Ohm"/>
<part name="R3" library="lib" deviceset="RESISTOR" device="-R1206" value="50 Ohm"/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="J1" gate="G$1" x="-10.16" y="66.04" rot="R90"/>
<instance part="J2" gate="G$1" x="-10.16" y="40.64" rot="R90"/>
<instance part="J3" gate="G$1" x="-10.16" y="17.78" rot="R90"/>
<instance part="J4" gate="G$1" x="104.14" y="40.64" rot="R270"/>
<instance part="U$1" gate="G$1" x="2.54" y="71.12"/>
<instance part="U$2" gate="G$1" x="2.54" y="45.72"/>
<instance part="U$3" gate="G$1" x="2.54" y="22.86"/>
<instance part="U$4" gate="G$1" x="88.9" y="45.72" rot="R180"/>
<instance part="R1" gate="&gt;NAME" x="35.56" y="45.72" smashed="yes" rot="R90">
<attribute name="NAME" x="38.354" y="61.722" size="1.778" layer="95" ratio="12"/>
<attribute name="VALUE" x="38.1" y="58.674" size="1.778" layer="96" ratio="12"/>
<attribute name="TOLERANCE" x="38.1" y="55.88" size="1.778" layer="96" ratio="12"/>
<attribute name="POWER" x="38.1" y="50.8" size="1.778" layer="96" ratio="12"/>
<attribute name="SIZE" x="38.1" y="53.34" size="1.778" layer="102"/>
</instance>
<instance part="R2" gate="&gt;NAME" x="35.56" y="38.1" smashed="yes" rot="R270">
<attribute name="NAME" x="38.1" y="36.83" size="1.778" layer="95" ratio="12"/>
<attribute name="VALUE" x="38.1" y="33.528" size="1.778" layer="96" ratio="12"/>
<attribute name="TOLERANCE" x="38.1" y="27.94" size="1.778" layer="96" ratio="12"/>
<attribute name="POWER" x="38.1" y="30.48" size="1.778" layer="96" ratio="12"/>
<attribute name="SIZE" x="38.1" y="25.4" size="1.778" layer="102"/>
</instance>
<instance part="R3" gate="&gt;NAME" x="40.64" y="45.72" smashed="yes">
<attribute name="NAME" x="45.72" y="49.53" size="1.778" layer="95" ratio="12" rot="R180"/>
<attribute name="VALUE" x="57.15" y="49.53" size="1.778" layer="96" ratio="12" rot="R180"/>
<attribute name="TOLERANCE" x="45.72" y="45.72" size="1.778" layer="96" ratio="12" rot="R180"/>
<attribute name="POWER" x="55.88" y="43.18" size="1.778" layer="96" ratio="12" rot="R180"/>
<attribute name="SIZE" x="50.8" y="43.18" size="1.778" layer="102" rot="R180"/>
</instance>
</instances>
<busses>
</busses>
<nets>
<net name="N$1" class="0">
<segment>
<pinref part="R3" gate="&gt;NAME" pin="B"/>
<wire x1="58.42" y1="45.72" x2="63.5" y2="45.72" width="0.1524" layer="91"/>
<label x="63.5" y="40.64" size="1.778" layer="95"/>
<pinref part="J1" gate="G$1" pin="SIGNAL"/>
<wire x1="-10.16" y1="66.04" x2="35.56" y2="66.04" width="0.1524" layer="91"/>
<pinref part="J4" gate="G$1" pin="SIGNAL"/>
<wire x1="35.56" y1="66.04" x2="71.12" y2="66.04" width="0.1524" layer="91"/>
<wire x1="71.12" y1="66.04" x2="71.12" y2="40.64" width="0.1524" layer="91"/>
<wire x1="71.12" y1="40.64" x2="104.14" y2="40.64" width="0.1524" layer="91"/>
<pinref part="J2" gate="G$1" pin="SIGNAL"/>
<wire x1="-10.16" y1="40.64" x2="63.5" y2="40.64" width="0.1524" layer="91"/>
<junction x="71.12" y="40.64"/>
<pinref part="J3" gate="G$1" pin="SIGNAL"/>
<wire x1="63.5" y1="40.64" x2="71.12" y2="40.64" width="0.1524" layer="91"/>
<wire x1="-10.16" y1="17.78" x2="35.56" y2="17.78" width="0.1524" layer="91"/>
<wire x1="35.56" y1="17.78" x2="71.12" y2="17.78" width="0.1524" layer="91"/>
<wire x1="71.12" y1="17.78" x2="71.12" y2="40.64" width="0.1524" layer="91"/>
<pinref part="R2" gate="&gt;NAME" pin="B"/>
<wire x1="35.56" y1="17.78" x2="35.56" y2="20.32" width="0.1524" layer="91"/>
<junction x="35.56" y="17.78"/>
<pinref part="R1" gate="&gt;NAME" pin="B"/>
<wire x1="35.56" y1="63.5" x2="35.56" y2="66.04" width="0.1524" layer="91"/>
<junction x="35.56" y="66.04"/>
<wire x1="63.5" y1="45.72" x2="63.5" y2="40.64" width="0.1524" layer="91"/>
<junction x="63.5" y="40.64"/>
</segment>
<segment>
<pinref part="R2" gate="&gt;NAME" pin="A"/>
<pinref part="R1" gate="&gt;NAME" pin="A"/>
<wire x1="35.56" y1="38.1" x2="35.56" y2="45.72" width="0.1524" layer="91"/>
<pinref part="R3" gate="&gt;NAME" pin="A"/>
<wire x1="40.64" y1="45.72" x2="35.56" y2="45.72" width="0.1524" layer="91"/>
<junction x="35.56" y="45.72"/>
</segment>
</net>
<net name="GROUND" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="P$5"/>
<pinref part="U$1" gate="G$1" pin="GROUND"/>
<wire x1="-5.08" y1="71.12" x2="-2.54" y2="71.12" width="0.1524" layer="91"/>
<pinref part="J1" gate="G$1" pin="P$4"/>
<wire x1="-2.54" y1="71.12" x2="2.54" y2="71.12" width="0.1524" layer="91"/>
<wire x1="-5.08" y1="68.58" x2="-2.54" y2="68.58" width="0.1524" layer="91"/>
<wire x1="-2.54" y1="68.58" x2="-2.54" y2="71.12" width="0.1524" layer="91"/>
<junction x="-2.54" y="71.12"/>
<pinref part="J1" gate="G$1" pin="P$3"/>
<wire x1="-5.08" y1="63.5" x2="-2.54" y2="63.5" width="0.1524" layer="91"/>
<wire x1="-2.54" y1="63.5" x2="-2.54" y2="68.58" width="0.1524" layer="91"/>
<junction x="-2.54" y="68.58"/>
<pinref part="J1" gate="G$1" pin="P$2"/>
<wire x1="-5.08" y1="60.96" x2="-2.54" y2="60.96" width="0.1524" layer="91"/>
<wire x1="-2.54" y1="60.96" x2="-2.54" y2="63.5" width="0.1524" layer="91"/>
<junction x="-2.54" y="63.5"/>
</segment>
<segment>
<pinref part="J2" gate="G$1" pin="P$5"/>
<pinref part="U$2" gate="G$1" pin="GROUND"/>
<wire x1="-5.08" y1="45.72" x2="-2.54" y2="45.72" width="0.1524" layer="91"/>
<pinref part="J2" gate="G$1" pin="P$4"/>
<wire x1="-2.54" y1="45.72" x2="2.54" y2="45.72" width="0.1524" layer="91"/>
<wire x1="-5.08" y1="43.18" x2="-2.54" y2="43.18" width="0.1524" layer="91"/>
<wire x1="-2.54" y1="43.18" x2="-2.54" y2="45.72" width="0.1524" layer="91"/>
<junction x="-2.54" y="45.72"/>
<pinref part="J2" gate="G$1" pin="P$3"/>
<wire x1="-5.08" y1="38.1" x2="-2.54" y2="38.1" width="0.1524" layer="91"/>
<wire x1="-2.54" y1="38.1" x2="-2.54" y2="43.18" width="0.1524" layer="91"/>
<junction x="-2.54" y="43.18"/>
<pinref part="J2" gate="G$1" pin="P$2"/>
<wire x1="-5.08" y1="35.56" x2="-2.54" y2="35.56" width="0.1524" layer="91"/>
<wire x1="-2.54" y1="35.56" x2="-2.54" y2="38.1" width="0.1524" layer="91"/>
<junction x="-2.54" y="38.1"/>
</segment>
<segment>
<pinref part="U$3" gate="G$1" pin="GROUND"/>
<pinref part="J3" gate="G$1" pin="P$5"/>
<wire x1="2.54" y1="22.86" x2="-2.54" y2="22.86" width="0.1524" layer="91"/>
<pinref part="J3" gate="G$1" pin="P$4"/>
<wire x1="-2.54" y1="22.86" x2="-5.08" y2="22.86" width="0.1524" layer="91"/>
<wire x1="-5.08" y1="20.32" x2="-2.54" y2="20.32" width="0.1524" layer="91"/>
<wire x1="-2.54" y1="20.32" x2="-2.54" y2="22.86" width="0.1524" layer="91"/>
<junction x="-2.54" y="22.86"/>
<pinref part="J3" gate="G$1" pin="P$3"/>
<wire x1="-5.08" y1="15.24" x2="-2.54" y2="15.24" width="0.1524" layer="91"/>
<wire x1="-2.54" y1="15.24" x2="-2.54" y2="20.32" width="0.1524" layer="91"/>
<junction x="-2.54" y="20.32"/>
<pinref part="J3" gate="G$1" pin="P$2"/>
<wire x1="-5.08" y1="12.7" x2="-2.54" y2="12.7" width="0.1524" layer="91"/>
<wire x1="-2.54" y1="12.7" x2="-2.54" y2="15.24" width="0.1524" layer="91"/>
<junction x="-2.54" y="15.24"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="GROUND"/>
<pinref part="J4" gate="G$1" pin="P$2"/>
<wire x1="88.9" y1="45.72" x2="96.52" y2="45.72" width="0.1524" layer="91"/>
<pinref part="J4" gate="G$1" pin="P$3"/>
<wire x1="96.52" y1="45.72" x2="99.06" y2="45.72" width="0.1524" layer="91"/>
<wire x1="99.06" y1="43.18" x2="96.52" y2="43.18" width="0.1524" layer="91"/>
<wire x1="96.52" y1="43.18" x2="96.52" y2="45.72" width="0.1524" layer="91"/>
<junction x="96.52" y="45.72"/>
<pinref part="J4" gate="G$1" pin="P$4"/>
<wire x1="99.06" y1="38.1" x2="96.52" y2="38.1" width="0.1524" layer="91"/>
<wire x1="96.52" y1="38.1" x2="96.52" y2="43.18" width="0.1524" layer="91"/>
<junction x="96.52" y="43.18"/>
<pinref part="J4" gate="G$1" pin="P$5"/>
<wire x1="99.06" y1="35.56" x2="96.52" y2="35.56" width="0.1524" layer="91"/>
<wire x1="96.52" y1="35.56" x2="96.52" y2="38.1" width="0.1524" layer="91"/>
<junction x="96.52" y="38.1"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
</eagle>
