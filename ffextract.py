import os
import sys
import traceback
from io import BytesIO
from PIL.ImageOps import flip
from collections import OrderedDict
from unitypack.export import OBJMesh
from dankware import clr, white, green
from unitypack.object import ObjectPointer
from unitypack.environment import UnityEnvironment

def fixext(name):
    tab = {'dds': 'png', 'nif': 'obj', 'kfm': 'obj', 'wav': 'ogg',
        'mp3': 'ogg', 'jpg': 'png', 'psd': 'png', 'dds.asset': 'png',
        'tga': 'png', 'tif': 'png', 'dds.mat': 'png', 'asset': 'png'}
    for ext in tab.keys():
        if name.endswith(ext): outname = name[:-len(ext)]; outname += tab[ext]; return outname
    return name

def write_to_file(path, contents, mode="w"):
    #print('would have written to', path); return
    if os.path.exists(path):
        #print('*** WARNING: {} already exists; skipping...'.format(path))
        return
    with open(path, mode) as f: written = f.write(contents)
    #print("Wrote %i bytes to %r" % (written, path))

def handle_texture(d, outpath):
    try: image = d.image
    except NotImplementedError: print("WARNING: Texture format not implemented. Skipping %r." % (filename)); return
    if image is None: print("WARNING: %s is an empty image" % (filename)); return
    img = flip(image); output = BytesIO(); img.save(output, format="png")
    write_to_file(outpath, output.getvalue(), mode="wb")

def handle_material(d, outpath):
    texture_ref = d._obj['m_SavedProperties']['m_TexEnvs'][0][1]['m_Texture']
    if texture_ref is not None: handle_texture(texture_ref.resolve(), outpath)

def handle_mesh(d, outpath):
    try: mesh_data = OBJMesh(d).export(); write_to_file(outpath, mesh_data, mode="w")
    except NotImplementedError as e: print("WARNING: Could not extract %r (%s)" % (d, e))

class GameobjectSearch:
    #seen = set()
    def __init__(self):
        self.seen = set()
        self.meshes = []

#def gameobject_recurse(obj, srch):
#    if isinstance(obj, ObjectPointer) and obj.object not in srch.seen:
#        #if obj.object.type == 'Mesh': srch.meshes.append(obj.resolve())
#        if obj.object.type == 'SkinnedMeshRenderer': d = obj.resolve(); srch.meshes.append(d['m_Mesh'].resolve()); return
#        elif obj.object.type == 'MeshFilter': d = obj.resolve()._obj; srch.meshes.append(d['m_Mesh'].resolve()); return
#        srch.seen.add(obj.object); gameobject_recurse(obj.resolve(), srch)

def gameobject_recurse(obj, srch):
    # NOTE: uncomment if re-enabling MeshFilter to...
    # limit the number of meshes per object to 2 for now; to work around
    # the problem of countless garbage meshes being ripped
    #if len(srch.meshes) >= 2: return
    #print('recursing into', obj, 'type', type(obj))
    if isinstance(obj, ObjectPointer) and obj.object not in srch.seen:
        if obj.object.type == 'Mesh': srch.meshes.append(obj.resolve())
        if obj.object.type == 'SkinnedMeshRenderer':
          #if obj.object.type.endswith('MeshRenderer'):
            d = obj.resolve()
            if d['m_Mesh'] is not None: srch.meshes.append(d['m_Mesh'].resolve())
            return
        elif obj.object.type == 'MeshFilter':
            #d = obj.resolve()._obj
            #if d['m_Mesh'] is not None: srch.meshes.append(d['m_Mesh'].resolve())
            return
        srch.seen.add(obj.object); gameobject_recurse(obj.resolve(), srch)
    #if not isinstance(obj, Transform) and not isinstance(obj, GameObject): return
    d = obj
    if not isinstance(d, OrderedDict):
        try: d = obj._obj
        except: pass
    if not isinstance(d, OrderedDict) and not isinstance(d, list) and not isinstance(d, tuple): return
    if type(d) == list:
        for ent in d: gameobject_recurse(ent, srch)
    elif type(d) == tuple:
        for ent in d: gameobject_recurse(ent, srch)
    else:
        for k, v in d.items(): gameobject_recurse(v, srch)

def handle_gameobject(obj, d, outpath):
    srch = GameobjectSearch(); srch.seen.add(obj); gameobject_recurse(d, srch)
    if len(srch.meshes) == 0: print('found {} meshes for {}'.format(len(srch.meshes), outpath)) #; sys.exit(1)
    i = 0
    for mesh in srch.meshes:
        outname = outpath
        if len(srch.meshes) != 1: outname = outname.replace('.obj', ':{}.obj'.format(i))
        handle_mesh(mesh, outname); i += 1

def handle_object(obj, outpath):
    #print('*** processing {} {}'.format(obj.type, outpath))
    d = obj.read()
    # Expected types:
	# 	AudioClip
	# 	BulletTableScript -
	# 	EnviroSoundScript -
	# 	GameObject
	# 	HNpcTableScript -
	# 	Material
	# 	MiniMapNpc -
	# 	MonoScript -
	# 	Shader
	# 	TerrainData TODO?
	# 	Texture2D
	# 	WorldNameScript -
	# 	XdtTableScript -
    if obj.type == "GameObject": handle_gameobject(obj, d, outpath)
    elif obj.type == "Material": handle_material(d, outpath)
    elif obj.type == "AudioClip": write_to_file(outpath, d.audio_data, mode="wb")
    elif obj.type == "MovieTexture": write_to_file(outpath, d.movie_data, mode="wb")
    elif obj.type == "Shader": write_to_file(outpath, d.script)
    elif obj.type == "Font": write_to_file(outpath, d.data, mode="wb")
    elif obj.type == "TextAsset": write_to_file(outpath, d.script, mode=mode)
    elif obj.type == "Texture2D": handle_texture(d, outpath)
    else: print('*** unhandled type', obj.type)

def handle_assetbundle(asset, outdir):
    if asset.objects[1].type_id != 142: return
    cont = asset.objects[1].read()['m_Container']
    for path, mtdt in cont:
        os.makedirs(os.path.join(outdir, os.path.dirname(path)), mode=0o755, exist_ok=True)
        outname = fixext(os.path.basename(path))
        outpath = os.path.join(outdir, os.path.dirname(path), outname)
        if os.path.exists(outpath): print('** {} exists, skipping...'.format(outpath)); continue
        #print('{} assetbundles open'.format(len(environment.files)))
        try: handle_object(mtdt['asset'].object, outpath); ###print("  {0}> {1}{2}{0}".format(white, green, outpath.split('\\')[-1]))
        except Exception as e:
            if isinstance(e, KeyboardInterrupt): raise e
            print(clr("  > Error: {}".format(outpath.split('\\')[-1]),2))
            ###print('** error while handling object {}'.format(outpath))
            ###traceback.print_exc(file=sys.stdout)

def ff_main(path, outdir):
    environment = UnityEnvironment()
    environment.base_path = path; files = os.listdir(path)
    for ent in os.listdir(path):
        abspath = os.path.join(path, ent)
        if os.path.isdir(abspath): files.remove(ent); files.extend([os.path.join(ent, f) for f in os.listdir(abspath)])
    for cas in files:
        name = os.path.basename(cas).lower()
        if not (name.startswith('customassetbundle') or name.startswith('buildplayer')): continue
        # TODO: apply heuristics?
		#if len(environment.files) > 64:
		#	for f in environment.files[:32]: f.close()
        print('* opening', name); print('* {} assetbundles open'.format(len(environment.files)))
        try: asset = environment.get_asset_by_filename(cas); handle_assetbundle(asset, outdir)
        except Exception as e:
            if isinstance(e, KeyboardInterrupt): break
            print('* error while handling assetbundle {}'.format(cas)); traceback.print_exc(file=sys.stdout)

if __name__ == '__main__':
    if len(sys.argv) != 3: print('usage: ffextract.py indir outdir'); sys.exit(1)
    ff_main(sys.argv[1], sys.argv[2])