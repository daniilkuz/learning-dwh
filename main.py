from fastapi import FastAPI
from contextlib import asynccontextmanager
from router import router, admin_router, items_router
import uvicorn
from config.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер для управления жизненным циклом приложения.
    """
    # Запуск: создание таблиц при старте
    create_tables()
    print("База данных инициализирована")

    yield

    # Завершение: очистка ресурсов
    print("Приложение завершает работу")


app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# @app.exception_handler(AlreadyExistsException)
# def already_exists_exception_handler(_: Request, exc: AlreadyExistsException):
#     return JSONResponse(
#         status_code=409,
#         content={"message": exc.name}
#     )

app.include_router(items_router)
app.include_router(admin_router)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
