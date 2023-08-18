pip3 install "uvicorn[standard]" -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install fastapi -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install logru -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install schedule -i https://pypi.tuna.tsinghua.edu.cn/simple


nohup python FileVersion.py > out.log 2>&1 &