## Steps to Set Up and Run the Application

### 1. Create a virtual environment with python3.11 and install necessary dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Calendar Data
Run the following command to generate calendar data using `generate_data.py`. This will create a `calendar.json` file in the data directory.

```bash
python generate_data.py
```

### 3. Run the chainlit UI to interact with the agent

```bash
chainlit run main.py
```

### 3. Navigate to http://localhost:8000 to interact with the agent

### Alternatively use Docker

### 1. Build Docker image

```bash
docker build -t booking-app .
```

### 2. Run docker container. Mount the data directory onto the container.

```bash
docker run -v data:/usr/src/app/data -p 8000:8000 -e OPENAI_API_KEY=your_openai_key booking-app
```

### 3. Navigate to http://localhost:8000 to interact with the agent




