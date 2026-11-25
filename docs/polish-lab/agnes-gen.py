import os, subprocess, sys
key = open(os.path.expanduser('~/.creds/kv/AGNES_API_KEY.txt')).read().strip()
env = dict(os.environ, AGNES_API_KEY=key)
name, size, prompt = sys.argv[1], sys.argv[2], sys.argv[3]
out = f'/tmp/agnes/out/{name}'
os.makedirs(out, exist_ok=True)
r = subprocess.run(['python3', '/tmp/agnes/repo/agnes-free-image/scripts/agnes_image.py', 'generate', '--size', size, '--output-dir', out, '--prompt', prompt], env=env, capture_output=True, text=True)
txt = (r.stdout + r.stderr).replace(key, '***')
print('rc', r.returncode); print(txt[-1500:]); print(os.listdir(out))
