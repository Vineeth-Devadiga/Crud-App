from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from newapp.models import KeyValue

class KeyValueInput(BaseModel):
    key: str
    value: str

app = FastAPI()

@app.post("/key-value/")
async def create_key_value_pair(kv: KeyValueInput):
    instance, created = KeyValue.objects.get_or_create(key=kv.key)
    instance.value = kv.value
    instance.save()
    return {"key": kv.key, "value": kv.value}

@app.get("/key-value/{key}")
async def read_key_value_pair(key: str):
    try:
        instance = KeyValue.objects.get(key=key)
    except KeyValue.DoesNotExist:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": instance.key, "value": instance.value}

@app.put("/key-value/{key}")
async def update_key_value_pair(key: str, value: str):
    try:
        instance = KeyValue.objects.get(key=key)
    except KeyValue.DoesNotExist:
        raise HTTPException(status_code=404, detail="Key not found")
    instance.value = value
    instance.save()
    return {"key": key, "value": value}

@app.delete("/key-value/{key}")
async def delete_key_value_pair(key: str):
    try:
        instance = KeyValue.objects.get(key=key)
    except KeyValue.DoesNotExist:
        raise HTTPException(status_code=404, detail="Key not found")
    instance.delete()
    return {"message": "Key deleted successfully"}
