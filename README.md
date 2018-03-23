# Audio Measurement Workstation
## Initial Specifications
- Class II appliance - no ground loops incl. display
- Balanced inputs for measuring bridged or digital amps
- Dedicated device
- Decent measurement quality - PCI soundcard ESI Juli@

## Design Overview
### Thin Client PC FS Futro S900N
- Class II power adapter
- PCI slot incl. +12/-12V supply voltages
- Dual core CPU to allow measurement and VNC remote access
- Connectors for two SATA drives to allow increasing reliability/repairability with RAID1 configuration
- No monitor, keyboard, mouse - access via network VNC
- Current IP address relayed via speech synthesis announcements, using internal soundcard and speaker.
- Inexpensive from ebay

### ESI Juli@
- Both balanced and single-ended inputs and outputs, functioning simultaneously. It allows feeding an amp with single-ended signal and measure balanced speaker output at the same time.
- Digital outputs/inputs for extra measurements/tests
- Full support in linux
- Priced moderately on ebay due to lack of PCI slots in modern PCs


### Software
- Linux Mint Mate (v. 18 at the time of writing)
- Arta measurement software running under wine
- Control - python script hooked to ACPI power button.
  - At startup - Etherner and/or wifi IP addresses are announced.
  - Pushing the power button once - IP addresses announced
  - Pushing the power button twice within two seconds - shutting down + announcement

### Operation
- Measurement mode - remotely via VNC on another PC
- Admin mode - possible to connect monitor/keyboard/mouse at any time


## Construction
All parts are 3D printed, FreeCAD sources and STL models are included in design folder.

Since the thin client supports only half-size PCI cards, room/holes must be made for full-sized one. Upper sound jacks and PS/2 slot must be removed/sawn off.

<img src="https://github.com/pavhofman/measurement-station/raw/master/images/1.jpg">
<img src="https://github.com/pavhofman/measurement-station/raw/master/images/3.jpg">
<img src="https://github.com/pavhofman/measurement-station/raw/master/images/4.jpg">

The original holder of the secondary heat sink must be removed, the heat sink fixed directly to the bottom with a new holder.
<img src="https://github.com/pavhofman/measurement-station/raw/master/images/2.jpg">

The soundcard is connected with a PCI cable adapter (https://www.aliexpress.com/wholesale?SearchText=19cm+PCI+extension+cable). It is mounted with 3D-printed brackets. The lower brackets provide only shielding, using copper tape connected to the PC enclosure.
Coax digital input and output are extracted from the multiconnector socket to individual add-on cinches.

<img src="https://github.com/pavhofman/measurement-station/raw/master/images/5.jpg">
<img src="https://github.com/pavhofman/measurement-station/raw/master/images/6.jpg">
<img src="https://github.com/pavhofman/measurement-station/raw/master/images/7.jpg">
<img src="https://github.com/pavhofman/measurement-station/raw/master/images/8.jpg">
<img src="https://github.com/pavhofman/measurement-station/raw/master/images/9.jpg">
<img src="https://github.com/pavhofman/measurement-station/raw/master/images/10.jpg">

The back panel is printed in two colors.
<img src="https://github.com/pavhofman/measurement-station/raw/master/images/12.jpg">
<img src="https://github.com/pavhofman/measurement-station/raw/master/images/13.jpg">

Holes for long cinches are drilled into the front panel, covered with a two-color printed plate.
<img src="https://github.com/pavhofman/measurement-station/raw/master/images/11.jpg">

## Performance
Single-ended and balanced inputs are mixed before the ADC. Therefore, for best performance of the higher-voltage balanced inputs short-circuit the more sensitive single-ended inputs with short-circuited cinches. In balanced-balanced closed-loop measurement this improves noise RMS from -102dB to -105dBFS.

Closed loop no signal
<img src="https://github.com/pavhofman/measurement-station/raw/master/images/loop.png">

Closed loop 1kHz signal
<img src="https://github.com/pavhofman/measurement-station/raw/master/images/1khz_loop.png">

Amps are measured with a dummy load with replaceable balanced voltage dividers made from old CPU heatsinks, optionally cooled with the original heatsink fans. I will post more pictures and resistor values.
<img src="https://github.com/pavhofman/measurement-station/raw/master/images/14.jpg">

## Notes
### Testing Juli@ Voltage Supplies
The PC generates +12V/-12V voltages for the PCI slot. I cut these supply pins on the connector between digital and ADC/DAC parts of Juli and fed the ADC/DAC part with 7812/7912 linear PSUs. No change in noise background was detected in Arta. It means the internal regulators on Juli are capable of filtering the SMPS-generated supply voltage sufficiently and the PCI-supplied voltages can be used safely.

### Shielding Juli@
I measured the closed-loop noise floor before covering the bottom holders of Juli@ with copper tape and connecting to the case. The difference between the unshielded  and shielded soundcard was less than 0.2dBFS. Therefore I assume the bottom shields are not necessary and do not have to be printed/installed at all.

### No Impact of SSD on Measurement Performance
Running full RAID1 sync on the secondary SSD located right beneath the soundcard had no measurable impact on the closed-loop noise floor of 105.1dBFS.
