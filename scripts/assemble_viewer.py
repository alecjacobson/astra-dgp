from pathlib import Path
import base64
P=Path(__file__).resolve().parents[1];template=(P/'viewer/template.html').read_text();bundle=(P/'viewer/bundle.js').read_text();data=base64.b64encode((P/'bahen-centre.glb').read_bytes()).decode()
(P/'bahen-centre-viewer.html').write_text(template.replace('<!--SCRIPTS-->',f'<script>window.MODEL_BASE64="{data}";</script><script>{bundle}</script>'))
(P/'viewer/index.html').write_text(template.replace('<!--SCRIPTS-->','<script src="bundle.js"></script>'))
print('Standalone viewer assembled')
