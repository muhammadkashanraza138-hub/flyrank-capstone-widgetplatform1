from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.core.config import settings
from app.routers import auth,widgets,public,dashboard
app=FastAPI(title='FlyRank Widget Platform',version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.cors_allow_origins.split(',')],allow_credentials=False,allow_methods=['*'],allow_headers=['*'])
app.include_router(auth.router); app.include_router(widgets.router); app.include_router(public.router); app.include_router(dashboard.router)
@app.get('/health')
def health(): return {'status':'ok'}
@app.get('/widget.js')
def widget_js(): return FileResponse('static/widget.js',media_type='application/javascript',headers={'Cache-Control':'public, max-age=31536000, immutable'})
