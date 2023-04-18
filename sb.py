import pysubs2
import os
import subprocess
import re


with open('sb.srt', 'r',encoding="UTF-8") as f:
    srt = f.read()

# 使用正则表达式匹配时间标记
pattern = r'\d{2}:\d{2}:\d{2},\d{3}'
matches = re.findall(pattern, srt)

# 获取最后一个时间标记
last_match = matches[-1]
h, m, s_ms = last_match.split(':')
s, ms = s_ms.split(',')
total_seconds = int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

# 取整数
integer_val = int(total_seconds)
str_val = str(integer_val)

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.realpath(__file__))

# 构造FFmpeg可执行文件的路径
ffmpeg_path = os.path.join(script_dir, "ffmpeg.exe")

# 打开SRT文件
subs = pysubs2.load('sb.srt')

my_style = subs.styles["Default"].copy()
my_style.fontsize = "155"
my_style.alignment = 5
my_style.fontname = "SimHei"

subs.styles["Default"] = my_style

# 保存为新的ASS文件
subs.save('sb.ass')


command1 = ffmpeg_path+" -f lavfi -i color=c=black:s=1500x100:d="+str_val+" -t "+str_val+" bg.mp4"
subprocess.call(command1, shell=True)

command2 = ffmpeg_path+" -i bg.mp4 -vf ass=sb.ass -y sb.mp4"
subprocess.call(command2, shell=True)

os.remove("bg.mp4")
os.remove("sb.ass")
