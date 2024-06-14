from fastapi import FastAPI
import api.routes.user as user
import api.routes.contact as contact

app = FastAPI()

app.include_router(user.router,tags=["Users"])
app.include_router(contact.router,tags=["Contacts"])