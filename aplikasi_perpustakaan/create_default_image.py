import shutil, os
from PIL import Image
src = os.path.join('images','c8f5a905d349aebbc29804f76413a6d6.jpg')
dst = os.path.join('images','default.png')
if os.path.exists(src):
    shutil.copy(src,dst)
    print('✓ default image created:', dst)
else:
    img = Image.new('RGBA',(200,300),(200,200,200,255))
    img.save(dst)
    print('✓ default image generated:', dst)
