from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.models.model_receive import GetReceives, PostReceive
from app.models.model_expense import GetExpenses, PostExpense
from app.dependencies.database_requests import get_user_database_connection, insert_log
from app.dependencies.data_verification import verify_session
from fastapi import APIRouter

router = APIRouter()

@router.get("/api/receives")
def load_receives(request: GetReceives):
    if verify_session(request.username, request.session_id):
        
        user_db = get_user_database_connection(request.username)
        
        receives = list(user_db['receitas'].find({}, {'_id': 0}))
        for receive in receives:
            if 'date' in receive:
                receive['date'] = receive['date'].strftime('%Y-%m-%d %H:%M:%S')
        
        return JSONResponse(content={"Content": receives})
    else:
        raise HTTPException(status_code=401, detail="Operation not permitted: Expired Session.")

@router.post("/api/receives")
def post_data_receives(request: PostReceive):
    if verify_session(request.username, request.session_id):
        user_db = get_user_database_connection(request.username)
        
        receive = {
            'value':int(request.value), 
            'received': int(request.received), 
            'fixed': int(request.fixed), 
            'date': request.date,
            'category': request.category, 
            'description': request.description
        }
               
        try:
            user_db['receitas'].insert_one(receive)
            insert_log(f'Inserted receive', 'log_operations', f'mb_{request.username}')
            
            return JSONResponse(content={"Content": "Success: Receive successfully added."})
        except Exception as error:
            raise HTTPException(status_code=500, detail="Internal error: The record could not be inserted into the database") 
        
    else:
        raise HTTPException(status_code=401, detail="Operation not permitted: Expired Session.")


@router.get("/api/expenses")
def load_expenses(request: GetExpenses):
    if verify_session(request.username, request.session_id):
        
        user_db = get_user_database_connection(request.username)
        
        expenses = list(user_db['despesas'].find({}, {'_id': 0}))
        for expense in expenses:
            if 'date' in expense:
                expense['date'] = expense['date'].strftime('%Y-%m-%d %H:%M:%S')
        
        return JSONResponse(content={"Content": expenses})
    else:
        raise HTTPException(status_code=401, detail="Operation not permitted: Expired Session.")

@router.post("/api/expenses")
def post_data_expenses(request: PostExpense):
    if verify_session(request.username, request.session_id):
        user_db = get_user_database_connection(request.username)

        expense = {
            'value':int(request.value), 
            'received': int(request.received), 
            'fixed': int(request.fixed), 
            'date': request.date,
            'category': request.category, 
            'description': request.description
        }
        
        try:
            user_db['despesas'].insert_one(expense)
            insert_log(f'Inserted expense', 'log_operations', f'mb_{request.username}')
            
            return JSONResponse(content={"Content": "Success: Expense successfully added."})
        except Exception as error:
            raise HTTPException(status_code=500, detail="Internal error: The record could not be inserted into the database.") 
        
    else:
        raise HTTPException(status_code=401, detail="Operation not permitted: Expired Session.")