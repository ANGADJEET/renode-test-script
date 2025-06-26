# Dockerfile
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# 1) Install system deps + Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      python3 python3-venv python3-pip \
      git wget unzip curl ca-certificates \
      libssl-dev libicu-dev libpng-dev && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app

# 2) Copy your single main.py and the Renode script
COPY main.py script.resc ./

# 3) Install Antmicro packages & download Renode
COPY requirements.txt ./
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt && \
    renode-run download --renode-variant dotnet-portable
# 4) Make sure the Renode script is executable
RUN chmod +x script.resc

# 5) Run your unified script
CMD ["python3", "main.py"]

