nohup uvicorn RoTaskNameOcr:app --host 0.0.0.0 --port 4090 --workers 5

nohup uvicorn RoTaskNameOcr:app --host 0.0.0.0 --port 4090 --workers 10 > /root/cn_ocr_server/name_ocr.log 2>&1 &