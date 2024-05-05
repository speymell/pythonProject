import uvicorn
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notificaiton(email: str, message: str = ""):
    with open("log.txt", mode="w") as email_file:
        content = f"Уведомление для {email}: {message}"
        email_file.write(content)

@app.post("/send-notification/{email}")
async def send_notification(email:str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notificaiton, email, message="некоторое уведомление")
    return {"message": "Уведомление отправлено в фоновом режиме"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0, port=5000, log_level=info")