# Water-on-the-Ground
Anomaly Detect the Water on the Ground Using YOLOv8 with Jetson and Optris Thermal Camera 

## Check your device
`uname -a`
> Linux xavier 4.9.201-tegra #26 SMP PREEMPT Tue Mar 2 09:47:42 CST 2021 aarch64 aarch64 aarch64 GNU/Linux

`cat /etc/nv_tegra_release`
> \# R32 (release), REVISION: 5.0, GCID: 25531747, BOARD: t186ref, EABI: aarch64, DATE: Fri Jan 15 23:21:05 UTC 2021

aarch64是指ARM架构的64位指令集架构
### Noted!
> The installation of PyTorch on Jetson is different from normal PC, the GPU supported version can not be installed from pip method directly, you need to fetch wheel file to install that. You can find the wheel file here: https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
> 
> With the Jetson version checked above, we need to download **JetPack 4.5 (L4T R32.5.0)** and install it. The default installed torch is only CPU supported. You should note that only supports upto py36. https://github.com/ultralytics/ultralytics/issues/5019
>
> And `nvidia-smi` is not available on Jetson, you can use `jtop` instead.

```
x86: 它指的是由Intel开发的32位指令集架构
x64: intel向64位过渡的时候开发的ia64(x64架构), 兼容市场反应极差
x86-64: amd开发的x86的64位兼容(32和64的混合架构), 也叫amd64

x86目前泛指x86和x86-64架构，这是因为x86-64完全兼容x86。早期的x86是cisc的代表，后来的发展中逐步引入了risc的部分理念，将内部指令的实现大量模块化，准确来说是一个cisc外加risc部分技术的架构。到目前为止intel和amd的x86架构cpu虽然指令集上有很大差别了但是还是相互兼容的，所以软件可以直接用。目前x86的主要产品有Intel的至强，酷睿，奔腾，赛扬和凌动；amd的锐龙，apu等。上文提到的x64架构目前只有intel 安腾而且已经放弃了产品线。

arm是risc的典型代表(ARM可以指一家嵌入式芯片设计公司，也可以指该公司的架构)，不过在arm的发展过程中引入了部分复杂指令(完全没有复杂指令的话操作系统跑起来异常艰难)，所以是一个risc基础外加cisc技术的cpu。arm的主要专利技术在arm公司手中，像高通，三星，苹果这些公司需要拿到arm的授权。

另一个risc的典型处理器就是mips。mips是一个学院派的cpu，授权门槛极低，因此很多厂家都做mips或者mips衍生架构。我们平时接触到的mips架构cpu主要用在嵌入式领域，比如路由器。目前最活跃的mips是中国的龙芯

目前无论mips还是arm，性能和主流x86差距都很大，不过arm贵在便宜低功耗，mips则纯计算能力很强
```
## Connect Optris Thermal Camera
Thanks to [pyOptris](https://github.com/FiloCara/pyOptris). 
The camera connecting on Windows is unstable, since the dll file seems can not be loaded by python occasionally.
The best practice maybe the Linux.
Here, according to the device info, we choose **ARM64** SDK to download. 

`sudo dpkg -i libirimager-8.10.1-arm64.deb`

Following the instructions of `pyOptris`, after installed the packages, you need to modify some codes to adjust. There are some [bugs](https://github.com/FiloCara/pyOptris/blob/dev/pyOptris/direct_binding.py#L13) when `pyOptris` comes to Linux.
```python
DEFAULT_WIN_PATH = "..//..//irDirectSDK//sdk//x64//libirimager.dll"
DEFAULT_LINUX_PATH = "/usr/lib/libirdirectsdk.so"
lib = None

# Function to load the DLL accordingly to the OS
def load_DLL(dll_path: str=None) -> None:
    global lib
    if sys.platform == "linux":
        path = dll_path if dll_path is not None else DEFAULT_LINUX_PATH
        lib = ctypes.CDLL(path)

    elif sys.platform == "win32":
        path = dll_path if dll_path is not None else DEFAULT_WIN_PATH
        lib = ctypes.CDLL(path)
```
In Linux, the SDK will be installed automatically to system, and the dll file usually can not be located by user, we can simply let dll_path default be None to load the DEFAULT_LINUX_PATH.

If you encounted with some trouble of pip installing numpy, maybe you need to upgrade your pip. Furthermore, the installation of opencv-python may cost a lot of time because of the compling.

## Install YOLOv8
The oldest python that YOLOv8 supported is py38, you can not install it directly. 

```sh
# Clone the ultralytics repository
git clone https://github.com/ultralytics/ultralytics

# Navigate to the cloned directory
cd ultralytics

# Remove some unnecessary package requirement if error encountered

# Install the package in editable mode for development
pip install -e .
```

```py
>>> from ultralytics import YOLO

Traceback (most recent call last):
  File "/home/nvidia/Desktop/breeze/ultralytics/ultralytics/utils/checks.py", line 16, in <module>
    from importlib import metadata
ImportError: cannot import name 'metadata'
```

### Adjust some code to py36
`pip install importlib_metadata`

### Modify the code
`vi /home/nvidia/Desktop/breeze/ultralytics/ultralytics/utils/checks.py`

```py
# from importlib import metadata
try:
    from importlib import metadata
except ImportError: # for Python<3.8
    import importlib_metadata as metadata
__version__ = metadata.version("jsonschema")
```

## Visualize Demo
run the script to visualize in local:
`python inference.py`

run the script to visualize in web:
`python app.py`