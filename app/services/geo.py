import httpx, os
from app.core.config import settings
async def _get(url,ip):
    async with httpx.AsyncClient(timeout=2) as c:
        r=await c.get(url.format(ip=ip)); r.raise_for_status(); return r.json()
async def enrich(ip):
    if os.getenv('MOCK_GEO_A_DOWN')!='1':
        try:
            x=await _get(settings.geo_provider_a_url,ip)
            if x.get('status','success')=='success' or x.get('country'):
                return {'provider':'A','country':x.get('country'),'city':x.get('city'),'lat':x.get('lat'),'lon':x.get('lon')}
        except Exception: pass
    if os.getenv('MOCK_GEO_B_DOWN')!='1':
        try:
            x=await _get(settings.geo_provider_b_url,ip)
            return {'provider':'B','country':x.get('country_name'),'city':x.get('city'),'lat':x.get('latitude'),'lon':x.get('longitude')}
        except Exception: pass
    return None
