import os

import psychopy  # Necessary for paths to custom modules to load

import eyelinker

import resolutionwr


data_directory = os.path.join(
    os.path.expanduser('~'), 'Desktop', 'Colin', 'ResolutionWR', 'Pilot', 'Data')


task = resolutionwr.ResolutionWR(
        tracker=None,
        data_directory=data_directory,
        number_of_blocks=5,
        trials_per_set_size=5,
        experiment_name='ResolutionWR',
        data_fields=resolutionwr.data_fields,
        monitor_distance=90
    )


# Hooks
def init_tracker(self):
    self.tracker = eyelinker.EyeLinker(
        self.experiment_window,
        'RWR' + self.experiment_info['Subject Number'] + '_' +
        str(self.experiment_info['Session']) + '.edf',
        'BOTH')

    self.tracker.initialize_graphics()
    self.tracker.open_edf()
    self.tracker.initialize_tracker()
    self.tracker.send_tracking_settings()


def show_eyetracking_instructions(self):
    self.tracker.display_eyetracking_instructions()
    self.tracker.setup_tracker()


def pretrial_setup(self, _, block_num, trial_num):
    if trial_num % 5 == 0:
        self.tracker.drift_correct()

    status = 'Block {}, Trial {}'.format(block_num, trial_num)
    self.tracker.send_status(status)

    self.tracker.send_message('BLOCK %d' % block_num)
    self.tracker.send_message('TRIAL %d' % trial_num)

    self.tracker.start_recording()


def end_trial(self, _):
    self.tracker.stop_recording()


def kill_tracker(self):
    self.tracker.set_offline_mode()
    self.tracker.close_edf()
    self.tracker.transfer_edf()
    self.tracker.close_connection()


try:
    task.run(
        setup_hook=init_tracker,
        before_first_trial_hook=show_eyetracking_instructions,
        pre_trial_hook=pretrial_setup,
        post_trial_hook=end_trial,
        end_experiment_hook=kill_tracker,
    )
except Exception as e:
    kill_tracker(task)
    raise e
