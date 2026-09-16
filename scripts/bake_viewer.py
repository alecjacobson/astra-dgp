"""Bake Cycles diffuse illumination into portable, unlit glTF atlas materials.

Usage (operate on an already saved native scene, never modify that source):
  blender -b bahen-centre.blend -P scripts/bake_viewer.py -- \
    --scope central --output /tmp/bahen-baked.glb --size 2048 --samples 32

The baked colors use the scene's AgX view transform at --exposure. In Three.js,
set material.toneMapped = false for materials whose name starts 'Baked /'.
Glass and metallic materials remain ordinary PBR; lighting is view-independent.
"""
import argparse, json, math, sys, time, struct, hashlib
from pathlib import Path
import bpy
import bmesh
import numpy as np
from mathutils import Vector

ap = argparse.ArgumentParser()
ap.add_argument('--scope', choices=['central', 'full'], default='central')
ap.add_argument('--work-dir', default=None)
ap.add_argument('--output', default='/tmp/bahen-baked.glb')
ap.add_argument('--size', type=int, default=2048)
ap.add_argument('--hero-size', type=int, default=4096)
ap.add_argument('--exposure-map', default='{}', help='JSON map of two-digit layer prefixes to stops; defaults to uniform exposure')
ap.add_argument('--texture-format', choices=['PNG','JPEG'], default='JPEG')
ap.add_argument('--samples', type=int, default=32)
ap.add_argument('--exposure', type=float, default=-1.1)
ap.add_argument('--only-layer', default=None, help='Bake only this layer prefix into the shared cache')
ap.add_argument('--bake-only', action='store_true', help='Write atlas cache and report without replacing/exporting materials')
ap.add_argument('--resume', action='store_true')
ap.add_argument('--preview', action='store_true')
ap.add_argument('--save-blend', action='store_true')
args = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
out = Path(args.output).resolve(); out.parent.mkdir(parents=True, exist_ok=True)
work = Path(args.work_dir) if args.work_dir else out.parent / (out.stem + '-textures'); work.mkdir(parents=True, exist_ok=True)
exposure_map = json.loads(args.exposure_map)
start = time.monotonic(); scene = bpy.context.scene
manifest = {'source_sha256': hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),
            'normal_repair_version': 1, 'preserve_theatre_seat_pbr': True, 'scope': args.scope, 'samples': args.samples, 'texture_format': args.texture_format,
            'exposure': args.exposure, 'exposure_map': exposure_map}
manifest_path = work / 'bake-manifest.json'
if args.resume:
    old = json.loads(manifest_path.read_text())
    assert all(old.get(k) == v for k,v in manifest.items()), 'Atlas cache differs from source or lighting settings'
manifest_path.write_text(json.dumps(manifest, indent=2))
scene.render.engine = 'CYCLES'; scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'; prefs.get_devices()
    for d in prefs.devices: d.use = d.type == 'OPTIX'
    scene.cycles.device = 'GPU' if any(d.type == 'OPTIX' for d in prefs.devices) else 'CPU'
except Exception: scene.cycles.device = 'CPU'
scene.render.bake.use_pass_direct = True
scene.render.bake.use_pass_indirect = True
scene.render.bake.use_pass_color = True
scene.render.bake.use_pass_diffuse = True
scene.render.bake.use_pass_glossy = False
scene.render.bake.use_pass_transmission = False
scene.render.bake.use_pass_emit = True
scene.render.bake.use_selected_to_active = False
scene.render.bake.margin = 8
scene.render.bake.use_clear = True
scene.view_settings.exposure = args.exposure

shell_prefixes = ('Theatre ceiling', 'Theatre side wall', 'Theatre front wall',
                  'Theatre back wall', 'Video gallery low ceiling',
                  'Video upper corridor ceiling', 'Video central low ceiling')
def shell(o): return bool(o.get('cutaway_shell', False) or o.name.startswith(shell_prefixes) or o.name.startswith('Koffler'))
def layer(o):
    return next((c.name for c in o.users_collection if c.name[:2].isdigit()), '01 Architecture')
def is_pbr(o):
    if o.get('source_kind') == 'FONT' or o.get('preserve_uv'): return True
    for mat in o.data.materials:
        if not mat: continue
        # Plain white molded chairs need clean edges and live highlights, not
        # tiny disconnected lightmap islands with dark border contamination.
        if mat.get('source_texture') or mat.name == 'Theatre seat': return True
        p = mat.node_tree.nodes.get('Principled BSDF') if mat.use_nodes else None
        if p and (p.inputs['Metallic'].default_value >= .5 or p.inputs['Transmission Weight'].default_value > .05): return True
    return False

deps = bpy.context.evaluated_depsgraph_get()
# Evaluate modifiers and text with source transforms and local bounds intact.
prepared = []; normal_repairs = []; closed_count = 0; open_count = 0
for o in list(scene.objects):
    if o.type not in {'MESH', 'FONT', 'CURVE'}: continue
    ev = o.evaluated_get(deps)
    me = bpy.data.meshes.new_from_object(ev, preserve_all_data_layers=True, depsgraph=deps)
    if not me.polygons: bpy.data.meshes.remove(me); continue
    # Cycles renders reverse faces two-sided, but a diffuse bake launches rays
    # from the stored normal. Closed inside-out meshes therefore bake black.
    # Repair only proven negative signed volumes; never alter open surfaces.
    bm = bmesh.new(); bm.from_mesh(me)
    if bm.faces and all(edge.is_manifold for edge in bm.edges):
        closed_count += 1; volume = bm.calc_volume(signed=True)
        if volume < -1e-9:
            bmesh.ops.reverse_faces(bm, faces=list(bm.faces)); bm.normal_update()
            assert bm.calc_volume(signed=True) > 0
            bm.to_mesh(me); me.update(); normal_repairs.append({'name': o.name, 'original_volume': volume})
    else: open_count += 1
    bm.free()
    prepared.append((o, me))
# Complete dependency-graph evaluation before mutating scene membership.
# Otherwise each next object can trigger another full scene evaluation.
for o, me in prepared:
    no = bpy.data.objects.new(o.name + ' evaluated', me)
    no.matrix_world = o.matrix_world.copy()
    for prop in o.keys(): no[prop] = o[prop]
    no['source_kind'] = o.type
    no['component_count'] = 1
    no['source_name'] = o.name; no['cutaway_shell'] = shell(o)
    no['layer'] = layer(o)
    for c in o.users_collection: c.objects.link(no)
    bpy.data.objects.remove(o, do_unlink=True)
print('EVALUATION_DONE', len(prepared), round(time.monotonic()-start, 2), flush=True)

meshes = [o for o in scene.objects if o.type == 'MESH']
groups = {}
for o in meshes:
    if is_pbr(o): continue
    center = o.matrix_world @ (sum((Vector(v) for v in o.bound_box), Vector()) / 8)
    lay = o['layer']
    if args.scope == 'central':
        if not lay.startswith('11') or not (-19 < center.x < 9 and -17 < center.y < 0 and 3.8 < center.z < 8.7): continue
        region = 'central'
    else:
        # Four-metre floors and 20-metre wings keep fine interior components
        # from sharing an atlas with the complete building envelope.
        region = f'z{max(-1, math.floor(center.z / 4.2)):02d}'
        if lay.startswith(('01', '02', '03', '04', '05')): region += f'_x{math.floor(center.x / 20):02d}'
    key = (lay, region, shell(o))
    groups.setdefault(key, []).append(o)
print('BAKE_GROUPS', [(k, len(v)) for k,v in groups.items()], flush=True)
report = {'source_revision': scene.get('revision', 'unknown'), 'source_sha256': manifest['source_sha256'], 'scope': args.scope, 'size': args.size, 'samples': args.samples,
          'exposure': args.exposure, 'device': scene.cycles.device,
          'source_components': len(meshes), 'normal_repairs': normal_repairs, 'closed_meshes_checked': closed_count, 'open_meshes_untouched': open_count, 'groups': []}
# Cycles re-synchronizes the complete scene per bake target, so atlas groups
# must be joined first. Preserve original per-object coordinates as interpolated
# point attributes before joining; otherwise procedural wood and masonry stretch
# across the complete joined object's bounding box.
for o in meshes:
    co = np.empty(len(o.data.vertices) * 3, dtype=np.float32)
    o.data.vertices.foreach_get('co', co); co = co.reshape((-1, 3))
    bbox = np.asarray(o.bound_box); low = bbox.min(axis=0); span = bbox.max(axis=0)-low
    generated = (co-low) / np.where(span > 1e-8, span, 1)
    for name, values in [('bake_object_position', co), ('bake_generated', generated)]:
        attr = o.data.attributes.new(name, 'FLOAT_VECTOR', 'POINT')
        attr.data.foreach_set('vector', np.asarray(values, dtype=np.float32).ravel())
for mat in bpy.data.materials:
    if not mat.use_nodes: continue
    nodes = mat.node_tree.nodes; links = mat.node_tree.links
    for tc in list(nodes):
        if tc.type != 'TEX_COORD': continue
        for output, attribute in [('Object', 'bake_object_position'), ('Generated', 'bake_generated')]:
            if not tc.outputs[output].links: continue
            node = nodes.new('ShaderNodeAttribute'); node.attribute_name = attribute
            for link in list(tc.outputs[output].links): links.new(node.outputs['Vector'], link.to_socket)
# Batch before the first bake to avoid thousands of scene synchronizations
# per atlas. Shared material groups outside the bake preserve PBR/image shaders.
def join_objects(objects, name):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects: obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    count = sum(obj.get('component_count', 1) for obj in objects)
    bpy.ops.object.join(); obj = bpy.context.object; obj.name = name
    obj['component_count'] = count
    return obj
selected = {o for group in groups.values() for o in group}
remaining = {}
for o in meshes:
    if o in selected: continue
    k = (o['layer'], shell(o), tuple(m.name if m else '' for m in o.data.materials))
    remaining.setdefault(k, []).append(o)
print('PREBATCH_START', len(remaining), len(groups), round(time.monotonic()-start, 2), flush=True)
for batch_index, (k, objects) in enumerate(sorted(remaining.items(), key=lambda pair: len(pair[1]), reverse=True)):
    obj = join_objects(objects, 'Portable ' + k[0] + ' ' + (k[2][0] if k[2] else 'none'))
    obj['cutaway_shell'] = k[1]
    if batch_index % 10 == 0: print('PREBATCH_PROGRESS', batch_index, round(time.monotonic()-start, 2), flush=True)
for key, objects in sorted(groups.items(), key=lambda pair: len(pair[1]), reverse=True):
    groups[key] = [join_objects(objects, 'Atlas source ' + str(key))]
print('BATCHED_SCENE', sum(o.type == 'MESH' for o in scene.objects), flush=True)
finished = []
for index, (key, objects) in enumerate(groups.items()):
    if args.only_layer and not key[0].startswith(args.only_layer): continue
    hero = args.scope == 'full' and (key[0].startswith('13') or (key[0].startswith('11') and key[1] in {'z00', 'z01', 'z02'}))
    area = sum(p.area for o in objects for p in o.data.polygons)
    size = args.hero_size if hero else (512 if area <= 2 else args.size)
    scene.render.bake.margin = max(2, size // 512)
    scene.view_settings.exposure = float(exposure_map.get(key[0][:2], args.exposure))
    gstart = time.monotonic(); name = f'{index:02d}_{key[0][:2]}_{key[1]}_shell{int(key[2])}'
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects: o.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    # The original map remains available for existing paper/image textures;
    # the explicitly named atlas is only the active bake UV set.
    for o in objects:
        uv = o.data.uv_layers.new(name='BakeUV')
        o.data.uv_layers.active = uv
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=.004,
                             area_weight=1, correct_aspect=True, scale_to_bounds=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    source_count = sum(o.get('component_count', 1) for o in objects)
    bpy.ops.object.join(); joined = bpy.context.object
    joined.name = 'Atlas source ' + name
    objects = [joined]
    path = work / (name + ('.jpg' if args.texture_format == 'JPEG' else '.png'))
    if args.resume and path.exists():
        saved = bpy.data.images.load(str(path), check_existing=False)
        if min(saved.size) >= size:
            saved.pack(); finished.append((key, objects, saved))
            item = {'name': name, 'objects': source_count, 'polygons': sum(len(o.data.polygons) for o in objects),
                    'size': saved.size[0], 'exposure': scene.view_settings.exposure, 'cached': True,
                    'seconds': round(time.monotonic()-gstart, 2), 'texture_bytes': path.stat().st_size}
            report['groups'].append(item); print('BAKE_DONE', json.dumps(item), flush=True)
            continue
        bpy.data.images.remove(saved)
    image = bpy.data.images.new(name, width=size, height=size, alpha=False, float_buffer=True)
    image.generated_color = (0, 0, 0, 1)
    materials = set(mat for o in objects for mat in o.data.materials if mat)
    for mat in materials:
        mat.use_nodes = True
        n = mat.node_tree.nodes.new('ShaderNodeTexImage'); n.name = 'Bake destination'; n.image = image
        for node in mat.node_tree.nodes: node.select = False
        n.select = True; mat.node_tree.nodes.active = n
    bpy.context.view_layer.objects.active = objects[0]
    print('BAKE_START', name, len(objects), round(time.monotonic()-start, 2), flush=True)
    bpy.ops.object.bake(type='COMBINED')
    scene.render.image_settings.file_format = args.texture_format; scene.render.image_settings.quality = 95; scene.render.image_settings.color_mode = 'RGB'
    scene.render.image_settings.color_depth = '8'
    path = work / (name + ('.jpg' if args.texture_format == 'JPEG' else '.png'))
    temporary = path.with_name(path.stem + '.writing' + path.suffix)
    image.save_render(str(temporary), scene=scene); temporary.replace(path)
    saved = bpy.data.images.load(str(path), check_existing=False); saved.pack()
    finished.append((key, objects, saved))
    item = {'name': name, 'objects': source_count, 'polygons': sum(len(o.data.polygons) for o in objects),
            'size': size, 'exposure': scene.view_settings.exposure, 'seconds': round(time.monotonic()-gstart, 2), 'texture_bytes': path.stat().st_size}
    report['groups'].append(item); print('BAKE_DONE', json.dumps(item), flush=True)
    # Free the full-float atlas; the packed image remains available for export.
    for mat in materials:
        for node in list(mat.node_tree.nodes):
            if node.type == 'TEX_IMAGE' and node.image == image: mat.node_tree.nodes.remove(node)
    bpy.data.images.remove(image)

if args.bake_only:
    report['seconds'] = round(time.monotonic()-start, 2)
    out.with_suffix('.json').write_text(json.dumps(report, indent=2))
    print('BAKE_CACHE_COMPLETE', json.dumps(report), flush=True)
    sys.exit(0)

# Replace only after every group is baked: subsequent bakes must see original
# surface reflectance, not previously baked illumination fed back into the GI.
for key, objects, image in finished:
    mat = bpy.data.materials.new('Baked / ' + image.name); mat.use_nodes = True
    nodes = mat.node_tree.nodes; links = mat.node_tree.links; nodes.clear()
    output = nodes.new('ShaderNodeOutputMaterial'); emission = nodes.new('ShaderNodeEmission')
    tex = nodes.new('ShaderNodeTexImage'); tex.image = image
    uv = nodes.new('ShaderNodeUVMap'); uv.uv_map = 'BakeUV'
    links.new(uv.outputs[0], tex.inputs['Vector']); links.new(tex.outputs['Color'], emission.inputs['Color'])
    links.new(emission.outputs[0], output.inputs['Surface'])
    for o in objects:
        o.data.materials.clear(); o.data.materials.append(mat)
        for poly in o.data.polygons: poly.material_index = 0
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects: o.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join(); joined = bpy.context.object
    joined.name = 'Baked ' + key[0] + ' ' + key[1]
    joined['cutaway_shell'] = key[2]; joined['baked_illumination'] = True
    # Remove unused source UV layers to prevent the atlas landing in TEXCOORD_1.
    for uv in list(joined.data.uv_layers):
        if uv.name != 'BakeUV': joined.data.uv_layers.remove(uv)

if args.preview:
    scene.camera = bpy.data.objects.get('video_1430', scene.camera)
    scene.render.resolution_x = 1280; scene.render.resolution_y = 720; scene.render.resolution_percentage = 100
    # The atlases are already display-transformed: Standard/exposure zero is
    # the correct debug display, corresponding to unlit toneMapped=false.
    scene.view_settings.view_transform = 'Standard'; scene.view_settings.look = 'None'; scene.view_settings.exposure = 0
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = str(out.with_suffix('.png')); bpy.ops.render.render(write_still=True)
if args.save_blend: bpy.ops.wm.save_as_mainfile(filepath=str(out.with_suffix('.blend')))

# Maintain the layer parents used by the existing browser cutaway controls.
for c in bpy.data.collections:
    if c.name == 'Collection': continue
    parent = bpy.data.objects.new(c.name, None); scene.collection.objects.link(parent)
    for o in list(c.objects):
        mw = o.matrix_world.copy(); o.parent = parent; o.matrix_world = mw
for o in list(scene.objects):
    if o.type in {'LIGHT','CAMERA'}: bpy.data.objects.remove(o, do_unlink=True)
# Preserve supported image maps, while unsupported procedural PBR colors use
# authored palette colors instead of the exporter's white fallback.
for mat in bpy.data.materials:
    if mat.name.startswith('Baked / ') or not mat.use_nodes: continue
    p = mat.node_tree.nodes.get('Principled BSDF')
    if not p: continue
    sock = p.inputs['Base Color']
    if sock.links and sock.links[0].from_node.type != 'TEX_IMAGE':
        for link in list(sock.links): mat.node_tree.links.remove(link)
        sock.default_value = mat.diffuse_color
    for link in list(p.inputs['Normal'].links): mat.node_tree.links.remove(link)
bpy.ops.export_scene.gltf(filepath=str(out), export_format='GLB', export_apply=False,
                          export_cameras=False, export_lights=False, export_extras=True, export_yup=True)
# Blender exports an Emission shader as black PBR + emissive texture. Convert
# this well-defined material subset to KHR_materials_unlit so all glTF viewers
# understand that the atlas is final lighting rather than a physical lamp.
raw = out.read_bytes(); json_size = struct.unpack_from('<I', raw, 12)[0]
doc = json.loads(raw[20:20+json_size]); binary_chunks = raw[20+json_size:]
for material in doc.get('materials', []):
    if not (material.get('name', '').startswith('Baked / ') or material.get('name') == 'Source monitor'): continue
    texture = material.pop('emissiveTexture', None)
    material.pop('emissiveFactor', None)
    material['pbrMetallicRoughness'] = {'baseColorFactor': [1,1,1,1], 'metallicFactor': 0, 'roughnessFactor': 1}
    if texture: material['pbrMetallicRoughness']['baseColorTexture'] = texture
    material['extensions'] = {'KHR_materials_unlit': {}}
if 'KHR_materials_unlit' not in doc.setdefault('extensionsUsed', []): doc['extensionsUsed'].append('KHR_materials_unlit')
identity = doc.setdefault('asset', {}).setdefault('extras', {})
identity['source_components'] = report['source_components']
identity['source_revision'] = report['source_revision']
identity['source_blend_sha256'] = report['source_sha256']
blob = json.dumps(doc, separators=(',', ':')).encode(); blob += b' ' * ((-len(blob)) % 4)
rebuilt = struct.pack('<III', 0x46546c67, 2, 20+len(blob)+len(binary_chunks)) + struct.pack('<II', len(blob), 0x4e4f534a) + blob + binary_chunks
out.write_bytes(rebuilt)
report['seconds'] = round(time.monotonic()-start, 2); report['glb_bytes'] = out.stat().st_size
report['output'] = str(out)
report['glb_sha256'] = hashlib.sha256(out.read_bytes()).hexdigest()
out.with_suffix('.json').write_text(json.dumps(report, indent=2))
print('BAKE_REPORT', json.dumps(report), flush=True)
