import struct
_T=[]
for i in range(256):
    c=i
    for _ in range(8): c=(c>>1)^0x82F63B78 if c&1 else c>>1
    _T.append(c)
def crc32c(b, crc=0):
    crc^=0xffffffff
    for x in b: crc=_T[(crc^x)&0xff]^(crc>>8)
    return crc^0xffffffff
def mask(c): return (((c>>15)|(c<<17))+0xa282ead8)&0xffffffff
def varint(n):
    out=b''
    while True:
        b=n&0x7f; n>>=7
        if n: out+=bytes([b|0x80])
        else: return out+bytes([b])
def read_varint(b,i):
    r=s=0
    while True:
        x=b[i]; i+=1; r|=(x&0x7f)<<s; s+=7
        if not x&0x80: return r,i
BLOCK=32768
def read_log(path):
    data=open(path,'rb').read(); recs=[]; buf=b''; i=0
    while i+7<=len(data):
        off=i%BLOCK
        if BLOCK-off<7: i+=BLOCK-off; continue
        crc,ln,typ=struct.unpack('<IHB',data[i:i+7]); payload=data[i+7:i+7+ln]; i+=7+ln
        if typ==0 and ln==0: continue
        if typ in (1,): recs.append(payload)
        elif typ==2: buf=payload
        elif typ==3: buf+=payload
        elif typ==4: recs.append(buf+payload); buf=b''
    out={}
    for r in recs:
        seq,cnt=struct.unpack('<QI',r[:12]); j=12
        for _ in range(cnt):
            tag=r[j]; j+=1
            kl,j=read_varint(r,j); k=r[j:j+kl]; j+=kl
            if tag==1:
                vl,j=read_varint(r,j); v=r[j:j+vl]; j+=vl; out[k]=v
            else: out.pop(k,None)
    return out
def write_log(path, kv, seq=1):
    # one write batch per record to keep records small
    out=bytearray()
    def emit(payload):
        nonlocal out
        first=True
        while True:
            off=len(out)%BLOCK; left=BLOCK-off
            if left<7:
                out+=b'\x00'*left; continue
            avail=left-7; frag=payload[:avail]; payload=payload[avail:]
            end=not payload
            typ=1 if first and end else 2 if first else 4 if end else 3
            c=mask(crc32c(bytes([typ])+frag))
            out+=struct.pack('<IHB',c,len(frag),typ)+frag
            first=False
            if end: break
    for k,v in kv:
        if isinstance(k,str): k=k.encode()
        if isinstance(v,str): v=v.encode()
        batch=struct.pack('<QI',seq,1)+b'\x01'+varint(len(k))+k+varint(len(v))+v
        emit(batch); seq+=1
    open(path,'wb').write(bytes(out))
    return seq

def snappy_decompress(b):
    n,i=read_varint(b,0); out=bytearray()
    while i<len(b):
        t=b[i]; i+=1; kind=t&3
        if kind==0:
            ln=t>>2
            if ln>=60:
                nb=ln-59; ln=int.from_bytes(b[i:i+nb],'little'); i+=nb
            ln+=1; out+=b[i:i+ln]; i+=ln; continue
        if kind==1:
            ln=((t>>2)&7)+4; off=((t>>5)<<8)|b[i]; i+=1
        elif kind==2:
            ln=(t>>2)+1; off=int.from_bytes(b[i:i+2],'little'); i+=2
        else:
            ln=(t>>2)+1; off=int.from_bytes(b[i:i+4],'little'); i+=4
        for _ in range(ln): out.append(out[-off])
    return bytes(out)
def _block(data, off, size):
    raw=data[off:off+size]; typ=data[off+size]
    return snappy_decompress(raw) if typ==1 else raw
def _entries(blk):
    nrest=struct.unpack('<I',blk[-4:])[0]; end=len(blk)-4-4*nrest; i=0; key=b''; out=[]
    while i<end:
        sh,i=read_varint(blk,i); ns,i=read_varint(blk,i); vl,i=read_varint(blk,i)
        key=key[:sh]+blk[i:i+ns]; i+=ns; v=blk[i:i+vl]; i+=vl; out.append((key,v))
    return out
def read_sst(path):
    data=open(path,'rb').read(); f=data[-48:]
    j=0; mo,j=read_varint(f,j); ms,j=read_varint(f,j); io,j=read_varint(f,j); isz,j=read_varint(f,j)
    idx=_block(data,io,isz); res={}
    for k,h in _entries(idx):
        o,p=read_varint(h,0); s,p=read_varint(h,p)
        for ik,v in _entries(_block(data,o,s)):
            uk=ik[:-8]; tag=struct.unpack('<Q',ik[-8:])[0]; typ=tag&0xff; seq=tag>>8
            if uk not in res or res[uk][0]<seq: res[uk]=(seq,typ,v)
    return {k:v for k,(s,t,v) in res.items() if t==1}
def read_db(folder):
    import os,glob
    res={}
    for f in sorted(glob.glob(os.path.join(folder,'*.ldb'))): res.update(read_sst(f))
    for f in sorted(glob.glob(os.path.join(folder,'*.log'))): res.update(read_log(f))
    return res
