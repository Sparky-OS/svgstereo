from pathlib import Path
import importlib.util
import struct
import zlib
from PIL import Image
import sys
p=Path(__file__).with_name('reader.py')
evidence=Path(sys.argv[1]).resolve()
evidence.mkdir(parents=True, exist_ok=True)
spec=importlib.util.spec_from_file_location('reader',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
out=evidence/'packing-13.png'
left=Image.new('RGBA',(13,3),(255,0,0,255));right=Image.new('RGBA',(13,3),(0,0,255,255))
m.pack_pair(left,right,out)
im=Image.open(out).convert('RGBA')
assert im.size==(29,3)
assert im.crop((0,0,13,3)).tobytes()==left.tobytes()
assert im.crop((16,0,29,3)).tobytes()==right.tobytes()
data=out.read_bytes();pos=8;chunks=[]
while pos<len(data):
 n=struct.unpack('>I',data[pos:pos+4])[0];tag=data[pos+4:pos+8];value=data[pos+8:pos+8+n]
 chunks.append(tag)
 if tag==b'sTER':
  assert value==b'\x01'
  assert struct.unpack('>I',data[pos+8+n:pos+12+n])[0]==zlib.crc32(tag+value)
 pos+=12+n
assert chunks.index(b'sTER')<chunks.index(b'IDAT')
for case in ('default','internal12','all12','off'):
 d=evidence/'proof'/case
 expected=Image.open(d/'pair.png').convert('RGBA').tobytes()
 m.pack_pair(Image.open(d/'left.png').convert('RGBA'),Image.open(d/'right.png').convert('RGBA'),d/'pair.png')
 assert Image.open(d/'pair.png').convert('RGBA').tobytes()==expected
 assert (d/'pair.png').read_bytes()[37:42] == b'sTER\x01'
print('PASS: 13-pixel views keep 13 pixels each, 3 padding columns, right starts at 16; sTER=1 before IDAT')
print('PASS: all four existing 1920-wide proof pairs unchanged after packing fix')
