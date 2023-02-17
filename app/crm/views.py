import uuid

from aiohttp.web_response import json_response

from app.crm.models import User
from app.web.app import View


class AddUserView(View):
    async def post(self):
        data = await self.request.json()
        user = User(email=data['email'], _id=uuid.uuid4())

        await self.request.app.crm_accessor.add_user(user)

        return json_response(data={'status': 'ok'})


class ListUsersView(View):
    async def get(self):
        users = await self.request.app.crm_accessor.list_users()
        raw_users = [{'email': user.email, '_id': str(user._id)} for user in users]
        return json_response(data={'status': 'ok', 'users': raw_users})

