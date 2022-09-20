'''
### Tarea 3
Crear una nueva API, la cuál contenga cuatro endpoints con las siguientes consideraciones:

1. Un endpoint para crear un diccionario en donde las llaves de dicho diccionario sea un id de tipo entero como identificador único para una lista de usuarios. El valor de dicha llave será otro diccionario con la siguiente estructura:
    ```
    {"user_name": "name",
    "user_id": id,
    "user_email": "email",
    "age" (optiona): age,
    "recommendations": list[str],
    "ZIP" (optional): ZIP
    }
    ```
    Cada vez que se haga un request a este endpoint, se debe actualizar el diccionario. Hint: Definir un diccionario vacío fuera del endpoint.
    La respuesta de este endpoint debe enviar el id del usuario creado y una descripción de usuario creado exitosamente.

2. Si se envía datos con un id ya repetido, se debe regresar un mensaje de error que mencione este hecho.
3. Un endpoint para actualizar la información de un usuario específico buscándolo por id. Si el id no existe, debe regresar un mensaje de error que mencione este hecho.
4. Un endpoint para obtener la información de un usuario específico buscándolo por id. Si el id no existe, debe regresar un mensaje de error que mencione este hecho.
5. Un endpoint para eliminar la información de un usuario específico buscándolo por id. Si el id no existe, debe regresar un mensaje de error que mencione este hecho.
'''

import uvicorn
from fastapi import FastAPI
from typing import Union, List, Dict
from pydantic import BaseModel

app = FastAPI()


class Users(BaseModel):
    user_name: str
    user_id: int
    user_email: str
    age: Union[int, None] = None
    recommendations: List[str]
    ZIP: Union[int, None] = None


users_dict = {}


@app.put('/user')
def create_user(user: Users):
    user = user.dict()
    if user['user_id'] in users_dict:
        return {'error':f'User ID {user["user_id"]} ya está registrado.'}
    else:
        users_dict[user['user_id']] = user
        return {'description':f'User {user["user_id"]} con email {user["user_email"]} fue agregado correctamente.'}


@app.post('/user/{user_id}/{user_name}')
def update_user(user_id: int):
    if user_id not in users_dict:
        return {'error': f'El usuario {user_id} no existe.'}
    else:
        user_to_update = users_dict[user_id]
        users_dict[user_id]['user_name'] = user_to_update
        return {'Description': f"El nombre del usuario {user_id} fue actualizado correctamente."}


@app.get('/user/{user_id}')
def get_user(user_id: int):
    if user_id not in users_dict:
        return {'error': f'El usuario {user_id} no existe.'}
    else:
        user_info = users_dict[user_id]
        return user_info


@app.delete('/user/{user_id}')
def delete_user(user_id: str):
    if user_id not in users_dict:
        return {'Description': f'El usuario {user_id} no existe.'}
    else:
        usert = users_dict[user_id]
        del usert[Users]
        return {'description':f'User {usert} fue eliminado exitosamente.'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=False)
