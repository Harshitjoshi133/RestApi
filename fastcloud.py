from fastapi import FastAPI,Body
import httpx
import firebase_admin
from firebase_admin import credentials,firestore

app = FastAPI()


cred = credentials.Certificate("pit-sandpit-key.json")
firebase_admin.initialize_app(cred)

CLOUD_FUNCTION_URL="https://us-central1-pit-sandpit-innovation.cloudfunctions.net/publish-message"

#CLOUD_FUNCTION_URL="https://us-central1-cloud-functions-398ae.cloudfunctions.net/publish_message"
db=firestore.client()



@app.get("/")
async def start():
    return {"message":"Hello"}


@app.get("/get_all_docs")
def get_all_docs():
    try:
        docs=db.collection("Published-Message").stream()
    
        docs_list=[]

        for doc in docs:
            doc_data=doc.to_dict()
            
            doc_data["id"]=doc.id
            doc_data["docData"]=doc._data
            print(doc_data)
            docs_list.append(doc_data)
        # for doc_data in docs_list:
            # print(f'DocumentID:{doc_data["id"]}')
            # print(f'DocumentID:{doc_data["docData"]}')
        return {"document id":doc_data["id"],"document data name":doc_data["docData"]["name"]}
    except Exception as e:
        return {"error",str(e)}

@app.get("/get_document/")
def get_doc_by_id(request):
    document_id=request
    doc_ref=db.collection("Published-Message").document(document_id)  
    respnse=doc_ref.get()
    if(respnse.exists):
        doc=respnse.to_dict()
    
        return {"response":doc};
    else:
        return{"error":"doc does not exist"}




@app.post("/create_task")
async def create_task(data=Body()):
    try:
        doc_ref=db.collection("Published-Message").document()
        async with httpx.AsyncClient() as client:
            response = await client.post(CLOUD_FUNCTION_URL, json={"message": doc_ref.id})
        
        doc_ref.set(data)
        return {"response id":response.text, "response status":response.status_code}
        #return {"responded text":response.text,"response status":response.status_code}
    except Exception as e:
        return {"Error":str(e)}
