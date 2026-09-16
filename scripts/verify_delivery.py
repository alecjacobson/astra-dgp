"""Load exact final files offline and the public GitHub Pages deployment."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os,shutil,json,hashlib
P=Path(__file__).resolve().parents[1];r={};errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.getenv('BAHEN_CHROME') or shutil.which('google-chrome') or '/opt/google/chrome/chrome',headless=True,args=['--no-sandbox','--use-angle=swiftshader','--enable-webgl'])
 for name,url in [('offline',(P/'bahen-centre-viewer.html').as_uri()),('public','https://alecjacobson.github.io/astra-dgp/viewer/')]:
  page=b.new_page(viewport={'width':1200,'height':900});page.on('pageerror',lambda e:errors.append(str(e)))
  if name=='offline':page.route('http**://**/*',lambda route:route.abort())
  response=page.goto(url,wait_until='load',timeout=90000)
  assert response is None or response.status==200, f'{name} HTTP {response.status}'
  page.wait_for_function('window.bahen?.state.loaded',timeout=120000);page.wait_for_timeout(1000);r[name]={'status':response.status if response else None,'state':page.evaluate('window.bahen.state')}
  assert r[name]['state']['meshes']>0
  assert page.locator('[data-view="room2133"]').count()==1
  assert page.locator('[data-view="theatre"]').count()==1
  expected=json.loads((P/'review/glb-audit.json').read_text())['meshes']
  assert f'{expected:,}' in page.locator('#modelstats').inner_text(),'Stale or different model loaded'
  page.locator('[data-view="room2133"]').click();page.wait_for_timeout(1000);assert page.evaluate('window.bahen.state.view')=='room2133'
  page.locator('[data-view="landing"]').click();page.wait_for_timeout(1000);r[name]['landing']=page.evaluate('window.bahen.state');assert r[name]['landing']['view']=='landing'
  if name=='public':page.screenshot(path=str(P/'renders/public-viewer.png'),timeout=90000)
  page.close();print(name,'passed',flush=True);(P/'review/delivery-check.json').write_text(json.dumps(r,indent=2))
 b.close()
r['sha256']={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['bahen-centre.blend','bahen-centre.glb','bahen-centre-viewer.html']};r['page_errors']=errors;r['passed']=not errors;(P/'review/delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));assert not errors
