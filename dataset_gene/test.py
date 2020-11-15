import re
import json
from util import Extractor, outputPath
string = '{"code":0,"message":"0","ttl":1,"data":{"mid":31374926,"name":"23456五羟基己醛","sex":"男","face":"http://i2.hdslb.com/bfs/face/0f1a2f761f861451c15ab2603dc465e8d9942c95.jpg","sign":"狗狗摸余我也摸鱼，懂？","rank":10000,"level":6,"jointime":0,"moral":0,"silence":0,"birthday":"08-15","coins":152.4,"fans_badge":false,"official":{"role":0,"title":"","desc":"","type":-1},"vip":{"type":2,"status":1,"theme_type":0,"label":{"path":"","text":"年度大会员","label_theme":"annual_vip"},"avatar_subscript":1,"nickname_color":"#FB7299"},"pendant":{"pid":18325,"name":"NAKIRI","image":"http://i2.hdslb.com/bfs/garb/86ee9c59ffeec205229c0e9bfd0f6982032203ac.png","expire":0,"image_enhance":"http://i2.hdslb.com/bfs/garb/86ee9c59ffeec205229c0e9bfd0f6982032203ac.png"},"nameplate":{"nid":61,"name":"饭圈楷模","image":"http://i1.hdslb.com/bfs/face/5a90f715451325c642a6ac39e01195cb6d075734.png","image_small":"http://i2.hdslb.com/bfs/face/5bfc1b4fb3f4b411495dddb0b2127ad80f6fbcac.png","level":"普通勋章","condition":"当前持有粉丝勋章最高等级\u003e=10级"},"is_followed":false,"top_photo":"http://i0.hdslb.com/bfs/space/cb1c3ef50e22b6096fde67febe863494caefebad.png","theme":{},"sys_notice":{},"live_room":{"roomStatus":1,"liveStatus":0,"url":"https://live.bilibili.com/5011686","title":"试一试","cover":"","online":0,"roomid":5011686,"roundStatus":0,"broadcast_type":0}}}'

outputfile = outputPath + "test.txt"
with open(outputfile, 'w') as f:
    json.dump(string, f)
