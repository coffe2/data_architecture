## login

* 기능: 사용자 로그인

* URI
   - IP:port/login

* Client --> Server
  - Format: JSON
  - Example

```python
{
   "user_id": "...",
   "passwd": "..."
}
```

* Server --> Client
  - Format: JSON
  - Example
  
```python
* Success case
{"msg":"","result":true,"session_id":"..."}

* Fail case
{"msg":"...", result":false, "session_id":none}
```


## calendar

* 기능: 스케줄 추가 및 확인

* URI
   - IP:port/favorite

* Client --> Server
  - Format: JSON
  - Example
  
```python
* 스케줄 추가하기
{
   "request_type": "add",
   "session_id": "...",
   "schedule": ["...", "...", ...]
}

* 스케줄 확인하기
{
   "request_type": "show",
   "session_id": "...",
   "date": "..."
}
```

* Server --> Client
  - Format: JSON
  - Example
  
```python
* 스케줄 추가
{
   "session_id": "...",
   "result": true,
   "msg": ""
}

* 스케줄 확인
{
   "session_id": "...",
   "schedule": ["...", "...", ...]
}
```
