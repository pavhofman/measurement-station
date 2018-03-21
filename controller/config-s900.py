# alsa card name
PC_SPEAKER_NAME = 'SB'
DO_POWER_OFF = True


def check_acpi_event(event)-> bool:
    return event[0] == 'button/power' and event[1] == 'PBTN'
