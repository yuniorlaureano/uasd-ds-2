import platform

import tensorflow as tf

def check_runtime():
    return f"""
    - Python/OS: {platform.python_version()} {platform.platform()}
    - TensorFlow: {tf.__version__}
    - GPU: {tf.config.list_physical_devices("GPU")}
    """