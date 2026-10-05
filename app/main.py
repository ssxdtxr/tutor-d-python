from fastapi import FastAPI, status

app = FastAPI()


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check() -> dict:
    return {"status": "ok"}


def main():
    print("Hello from tutors-d!")


if __name__ == "__main__":
    main()
