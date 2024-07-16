from setuptools import setup, find_packages

setup(
    name="blindsee",
    version="1.0.0",
    description="Visually impaired assistive glasses on Raspberry Pi 2 with EEG, vision, GPT-4o, and TTS.",
    author="John Tian",
    author_email="john.tian31@gmail.com",
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=[
        "opencv-python",
        "numpy",
        "pyserial",
        "pyttsx3",
        "tensorflow",
        "tflite-runtime",
        "openai",
        "pydantic",
        "RPi.GPIO"
    ],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Operating System :: POSIX :: Linux",
    ],
)