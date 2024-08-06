from fastapi import FastAPI
import models
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import router.typing_router as typing_router
import router.user_router as user_router

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(typing_router.app, tags=["typing"])
app.include_router(user_router.app, tags=["user"])

origins = [
    "http://localhost:5173/",
    "https://monkeyfinger.netlify.app",
    "https://master--monkeyfinger.netlify.app",
]
# origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return "hello"


# client = OpenAI(
#     organization="org-MTh1QeshOBBE0hOZAi5z9Mfo",
#     project="proj_CH1M2LPgCzpMvmS2W4TJD4Fj",
# )

# load_dotenv()
# client.api_key = os.getenv("OPENAI_API_KEY")


# # 이것도 get으로 변경하자.
# @app.get("/advice")
# # 이거 그냥 DB 조회로 하자. body로 데이터 받지 말고.
# def advice():
#     engine, view_table, m = connDB("MONKEY_FINGER_VIEW")

#     with engine.connect() as conn:
#         d = view(view_table, conn)
#     model = "gpt-4o-mini"
#     query = f"{d}"
#     messages = [
#         {
#             "role": "system",
#             "content": "타자연습 데이터를 매우 상세하게 분석해서 텍스트 형태로 반환해줘.  주어진 데이터는 wpm, acc, 테스트 소요 시간, 테스트 모드야. 말투는 비서처럼. 간단하게 설명해줘.",
#         },
#         {"role": "user", "content": query},
#     ]
#     response = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         temperature=1,
#         max_tokens=512,
#         frequency_penalty=1.2,
#     )
#     return response.choices[0].message.content
