import os

#os.environ['DISPLAY'] = ":0.0"
#os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.animation import Animation

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel

from dpeaDPi.DPiComputer import DPiComputer
from dpeaDPi.DPiStepper import *
from time import sleep

dpiStepper = DPiStepper()
dpiStepper.setBoardNumber(0)

if dpiStepper.initialize() != True:
    print("Communication with the DPiStepper board failed.")

dpiStepper.enableMotors(True)

microstepping = 8
dpiStepper.setMicrostepping(microstepping)

speed_steps_per_second = 200 * microstepping
accel_steps_per_second_per_second = speed_steps_per_second
dpiStepper.setSpeedInStepsPerSecond(0, speed_steps_per_second)
dpiStepper.setSpeedInStepsPerSecond(1, speed_steps_per_second)
dpiStepper.setAccelerationInStepsPerSecondPerSecond(0, accel_steps_per_second_per_second)
dpiStepper.setAccelerationInStepsPerSecondPerSecond(1, accel_steps_per_second_per_second)

stepperStatus = dpiStepper.getStepperStatus(0)
print(f"Pos = {stepperStatus}")

stepper_num = 0
steps = 1600
wait_to_finish_moving_flg = True
dpiStepper.moveToRelativePositionInSteps(stepper_num, steps, wait_to_finish_moving_flg)

from datetime import datetime

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
SECOND_SCREEN_NAME = 'second'
ADMIN_SCREEN_NAME = 'admin'
NEW_SCREEN_NAME = 'new'


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER

#hi bestie

Window.clearcolor = (1, 1, 1, 1)  # White
count = 0

class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from MainScreen.pressed()")

    def moto_on_off(self):
        motor_label = self.ids.motor_label
        motor_label.text = 'Motor Off' if motor_label.text == 'Motor On' else 'Motor On'

    def click(self):
        global count
        count = count + 1
        self.ids.btn.text= str(count)

    def secondscreen(self):
        SCREEN_MANAGER.current = "second"

    def newscreen(self):
        SCREEN_MANAGER.current = "new"

    def animate_button(self):
        anim = Animation(size = (200, 200), duration = 5)
        anim.start(self.ids.cat2)
        anim = Animation(size = (100, 100), duration = 2)
        anim.start(self.ids.cat2)
        self.newscreen()

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'

class SecondScreen(Screen):
    def secondscreen(self):
        SCREEN_MANAGER.current = "main"

class NewScreen(Screen):
    def newscreen(self):
        SCREEN_MANAGER.current = "main"



class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:

        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


"""
Widget additions
"""

Builder.load_file('main.kv')
Builder.load_file('second.kv')
Builder.load_file('new.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(SecondScreen(name=SECOND_SCREEN_NAME))
SCREEN_MANAGER.add_widget(NewScreen(name=NEW_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()

if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
