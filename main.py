import _thread
import gc

from utime import sleep

from lib.actions.medical_scan import MedicalScanAction
from lib.actions.starfleet import StarfleetAction
from lib.actions.surface_scan import SurfaceScanAction
from lib.audio import Audio
from lib.control_panel import ControlPanel
from lib.displays import Displays
from lib.utils import log


def event_loop(disps: Displays, audio: Audio, ctrl_panel: ControlPanel):
    # Start by creating actions
    starfleet_act = StarfleetAction(disps, audio, ctrl_panel)
    med_disp_act = MedicalScanAction(disps, audio, ctrl_panel)
    surface_scan_act = SurfaceScanAction(disps, audio, ctrl_panel)
    current_act = starfleet_act

    try:
        current_act.start()
        while True:
            log(f'GC: {gc.mem_free()}')    
            btns = ctrl_panel.read_buttons()

            if btns[ControlPanel.SW1] or btns[ControlPanel.SW2] or btns[ControlPanel.SW3]:
                log(f'GC PRE: {gc.mem_free()} - {btns} - {btns[ControlPanel.SW1] and btns[ControlPanel.SW3]}')    
                current_act.stop()
                gc.collect()
                if btns[ControlPanel.SW1] and btns[ControlPanel.SW3]:
                    current_act = starfleet_act
                elif btns[ControlPanel.SW1]:
                    current_act = med_disp_act
                elif btns[ControlPanel.SW2]:
                    current_act = surface_scan_act

                log(f'GC POST: {gc.mem_free()}')    
                current_act.start()
            
            current_act.step()
            sleep(current_act.step_delay)
                            
    except KeyboardInterrupt:
        if current_act:
            current_act.stop()


def main():
    gc.enable()
    ctrl_panel = ControlPanel()
    disps = Displays()
    audio = Audio()
    gc.collect()    
    event_loop(disps, audio, ctrl_panel)

if __name__=='__main__':
    main()            

