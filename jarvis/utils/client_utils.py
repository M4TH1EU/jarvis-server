import os

from jarvis.utils import config_utils


def speak(sentence, quality=config_utils.get_in_config("LARYNX_QUALITY")):
    voice = config_utils.get_in_config("LARYNX_VOICE")
    denoiserstrength = config_utils.get_in_config("LARYNX_DENOISER_STRENGTH")

    os.system(
        "larynx \"" + sentence + "\" --voice " + voice + " --quality " + quality +
        # " --output-dir wav " +
        " --interactive " +
        "--denoiser-strength " + str(denoiserstrength) +
        " --output-naming time")
