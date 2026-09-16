"""Real browser smoke check for exported geometry and interactive controls."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json,time
P=Path(__file__).resolve().parents[1];errors=[];result={}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/opt/google/chrome/chrome',headless=True,args=['--no-sandbox','--use-angle=swiftshader','--enable-webgl','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
 page.on('console',lambda m:print(m.type,m.text,flush=True) if m.type=='error' else None)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8766/viewer/index.html',wait_until='load');page.wait_for_function('window.bahen?.state.loaded',timeout=120000);page.wait_for_timeout(2500)
 result['initial']=page.evaluate('window.bahen.state');print(result['initial'],flush=True);page.screenshot(path=str(P/'renders/browser-exterior.png'))
 for name in ['east','landing','cutaway','west']:
  page.locator(f'[data-view="{name}"]').click();page.wait_for_timeout(1500);state=page.evaluate('window.bahen.state');assert state['view']==name;result[name]=state
  if name=='cutaway':assert state['visibleMeshes']<result['initial']['visibleMeshes'], 'Cutaway did not change visibility'
  if name in ['east','cutaway','landing']:page.screenshot(path=str(P/f'renders/browser-{name}.png'))
 page.locator('[data-view="exterior"]').click();visible_before=page.evaluate('window.bahen.state.visibleMeshes');page.locator('#trees').uncheck();assert page.evaluate('window.bahen.state.visibleMeshes')<visible_before;page.locator('#cut').check();assert page.evaluate('window.bahen.state.cutaway');result['controls']='view presets, landscape checkbox and cutaway checkbox respond'
 page.locator('#info').click();assert page.locator('#about').is_visible();page.locator('#close').click()
 page.locator('#hide').click();assert page.locator('#panel').get_attribute('class')=='collapsed';page.locator('#hide').click()
 page.locator('[data-view="exterior"]').click();before=page.evaluate('window.bahen.state.camera');page.locator('canvas').click(position={'x':1000,'y':600});page.keyboard.down('w');page.wait_for_function('(before)=>JSON.stringify(window.bahen.state.camera)!==JSON.stringify(before)',arg=before,timeout=15000);page.keyboard.up('w');after=page.evaluate('window.bahen.state.camera');assert before!=after;result['keyboard_navigation']=True
 with page.expect_download() as download:page.locator('#snapshot').click()
 d=download.value;d.save_as(str(P/'review/browser-snapshot.png'));result['screenshot_download_bytes']=(P/'review/browser-snapshot.png').stat().st_size
 # Portability: open standalone HTML via file URI with external network blocked.
 offline=browser.new_page(viewport={'width':1000,'height':800});offline.on('pageerror',lambda e:errors.append(str(e)));offline.route('http**://**/*',lambda route:route.abort());offline.goto((P/'bahen-centre-viewer.html').as_uri(),wait_until='load');offline.wait_for_function('window.bahen?.state.loaded',timeout=120000);result['standalone_offline_load']=offline.evaluate('window.bahen.state');offline.close()
 page.set_viewport_size({'width':390,'height':844});page.locator('#hide').click();page.screenshot(path=str(P/'review/browser-mobile.png'));result['mobile_resize']=True
 result['page_errors']=errors;browser.close()
(P/'review/viewer-test.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));assert not errors
