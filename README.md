<p align="center">
<img width="350" src="https://github.com/SamuelIvan99/lightweight-programming-language/assets/43946320/c88a4ca5-0d2e-48c6-a596-01739adb38bf" alt="Based logo">
</p>

<h1 align="center">The Based programming language</h1>

## Getting Started

### Installation

Start by installing the dependencies:
```bash
pip install -r requirements.txt
```

### Compiling

While in the root directory of the project, you can run based as a python module
```bash
python based -h
```
Give based input files and an output path
```bash
python based program.based -o executable
```
Then run the executable
```bash
./executable
```

### Developing the Standard Library

Put in your C and Headers in the ```stdlib_implementation``` directory,

Running the based compiler with python will in turn compile all of your stdlib implementations and will link the final executable with a static library.

Based is a programming language designed specifically for Internet of Things (IoT) applications. With its simplicity, efficiency, and focus on IoT-centric features, Based aims to streamline the development process for embedded systems and IoT devices.

## Features

- **Simplicity**: Based prioritizes simplicity to enable rapid development of IoT applications without unnecessary complexities.
- **Efficiency**: Designed to be lightweight and efficient, Based optimizes resource usage for IoT devices with constrained hardware.
<!---
- **IoT-centric**: Provides built-in support for common IoT protocols and functionalities, such as MQTT, CoAP, and sensor data processing.
- **Scalability**: Whether you're developing for a single sensor node or a complex IoT network, Based scales seamlessly to meet your requirements.
- **Extensibility**: Easily extendable through libraries and modules, allowing developers to tailor Based to suit specific IoT project needs.
- **Cross-platform**: Supports multiple hardware platforms and operating systems commonly used in IoT environments.
-->

### Explore Documentation

Refer to the [Documentation](./docs/) for detailed information on language syntax, standard libraries, and best practices.

## License

Based is licensed under the [MIT License](./LICENSE).



python based.py -b main.based -c stdlib -o OUTPUT
